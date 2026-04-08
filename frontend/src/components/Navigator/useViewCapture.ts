/**
 * useViewCapture — handles "R" keypress to capture current view.
 *
 * On "R":
 *   1. Take RGB screenshot via canvas.toDataURL
 *   2. Capture linearised depth via DepthCapture
 *   3. Extract 4×4 camera-to-world from camera.matrixWorld
 *   4. POST CapturePayload to /api/captures/save
 *   5. Add thumbnail to scene store
 */
import { useCallback, useEffect, useRef } from 'react'
import * as THREE from 'three'
import { DepthCapture, CAMERA_NEAR, CAMERA_FAR } from './DepthCapture'
import { captureApi } from '../../api/client'
import { useSceneStore } from '../../store/sceneStore'

interface UseViewCaptureOptions {
  renderer: THREE.WebGLRenderer | null
  scene: THREE.Scene | null
  camera: THREE.PerspectiveCamera | null
  canvas: HTMLCanvasElement | null
  enabled?: boolean
}

function getTransformMatrix(camera: THREE.PerspectiveCamera): number[][] {
  camera.updateMatrixWorld()
  const m = camera.matrixWorld.elements  // column-major
  return [
    [m[0], m[4], m[8],  m[12]],
    [m[1], m[5], m[9],  m[13]],
    [m[2], m[6], m[10], m[14]],
    [m[3], m[7], m[11], m[15]],
  ]
}

function canvasToBase64Png(canvas: HTMLCanvasElement): string {
  return canvas.toDataURL('image/png')
}

export function useViewCapture({
  renderer,
  scene,
  camera,
  canvas,
  enabled = true,
}: UseViewCaptureOptions) {
  const depthCaptureRef  = useRef<DepthCapture | null>(null)
  const capturingRef     = useRef(false)           // ref guard — immune to stale closures
  const { sceneId, nextViewId, addCapturedView, setIsCapturing, sceneInfo } = useSceneStore()

  // Lazily create or resize DepthCapture when canvas changes
  useEffect(() => {
    if (!canvas) return
    const w = canvas.width || canvas.clientWidth
    const h = canvas.height || canvas.clientHeight
    depthCaptureRef.current?.dispose()
    depthCaptureRef.current = new DepthCapture(w, h)
    return () => {
      depthCaptureRef.current?.dispose()
    }
  }, [canvas])

  const capture = useCallback(async () => {
    if (!renderer || !scene || !camera || !canvas) return
    if (capturingRef.current) return   // prevent re-entry if R is pressed mid-capture
    capturingRef.current = true
    setIsCapturing(true)

    try {
      const viewId = `v${String(nextViewId).padStart(3, '0')}`
      const w = canvas.width || canvas.clientWidth
      const h = canvas.height || canvas.clientHeight

      // RGB
      const rgb_b64 = canvasToBase64Png(canvas)

      // Depth
      if (!depthCaptureRef.current) {
        depthCaptureRef.current = new DepthCapture(w, h)
      }
      const depthArr = depthCaptureRef.current.capture(renderer, scene, camera)
      const depth_b64 = depthCaptureRef.current.encodeDepth(depthArr)

      // Camera pose
      const transform_matrix = getTransformMatrix(camera)
      const pos = camera.position

      // Intrinsics from scene info or defaults
      const fl_x = sceneInfo?.intrinsics?.fl_x ?? (w / (2 * Math.tan((camera.fov * Math.PI) / 360)))
      const fl_y = fl_x
      const cx = sceneInfo?.intrinsics?.cx ?? w / 2
      const cy = sceneInfo?.intrinsics?.cy ?? h / 2

      await captureApi.save({
        scene_id: sceneId,
        view_id: viewId,
        rgb_b64,
        depth_b64,
        transform_matrix,
        fl_x,
        fl_y,
        cx,
        cy,
        width: w,
        height: h,
      })

      addCapturedView({
        view_id: viewId,
        thumbnail: rgb_b64,
        position: [pos.x, pos.y, pos.z],
        timestamp: Date.now(),
      })
    } catch (err) {
      console.error('Capture failed', err)
    } finally {
      capturingRef.current = false
      setIsCapturing(false)
    }
  }, [renderer, scene, camera, canvas, sceneId, nextViewId, addCapturedView, setIsCapturing, sceneInfo])

  // "R" key handler
  useEffect(() => {
    if (!enabled) return
    const onKey = (e: KeyboardEvent) => {
      if (e.code === 'KeyR' && !e.repeat) capture()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [enabled, capture])

  return { capture }
}
