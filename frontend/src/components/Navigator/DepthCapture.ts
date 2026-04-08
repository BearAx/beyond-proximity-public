/**
 * DepthCapture — WebGL depth render target utilities.
 *
 * Captures linearised depth in metres from the THREE.js WebGL context,
 * matching the Python backend's DEPTH_NEAR / DEPTH_FAR constants.
 */
import * as THREE from 'three'

export const CAMERA_NEAR = 0.1
export const CAMERA_FAR  = 100.0

/**
 * Convert a non-linear NDC depth value (0→1 from the depth buffer) to
 * a linear depth in metres using the standard perspective linearisation.
 */
function linearizeDepth(depthNdc: number, near: number, far: number): number {
  // Reconstruct from OpenGL clip-space depth
  const z_ndc = depthNdc * 2.0 - 1.0
  return (2.0 * near * far) / (far + near - z_ndc * (far - near))
}

export class DepthCapture {
  private renderTarget: THREE.WebGLRenderTarget
  private readonly width: number
  private readonly height: number

  constructor(width: number, height: number) {
    this.width  = width
    this.height = height
    this.renderTarget = new THREE.WebGLRenderTarget(width, height, {
      depthBuffer: true,
      depthTexture: new THREE.DepthTexture(width, height),
    })
  }

  /**
   * Render the scene from the given camera into the depth render target,
   * read back the depth buffer, and return a Float32Array of linear depths
   * in metres (row-major, top-left origin).
   */
  capture(
    renderer: THREE.WebGLRenderer,
    scene: THREE.Scene,
    camera: THREE.PerspectiveCamera,
  ): Float32Array {
    const savedTarget = renderer.getRenderTarget()

    renderer.setRenderTarget(this.renderTarget)
    renderer.render(scene, camera)
    renderer.setRenderTarget(savedTarget)

    const buf = new Float32Array(this.width * this.height * 4)
    renderer.readRenderTargetPixels(this.renderTarget, 0, 0, this.width, this.height, buf)

    // Packed RGBA with depth in the R channel (THREE encodes DepthTexture this way)
    const depths = new Float32Array(this.width * this.height)
    for (let i = 0; i < depths.length; i++) {
      const raw = buf[i * 4] / 255.0
      depths[i] = linearizeDepth(raw, CAMERA_NEAR, CAMERA_FAR)
    }
    return depths
  }

  /**
   * Base64-encode raw float32 depth data (little-endian) for transmission.
   */
  encodeDepth(depthData: Float32Array): string {
    const bytes = new Uint8Array(depthData.buffer)
    let binary = ''
    bytes.forEach((b) => (binary += String.fromCharCode(b)))
    return btoa(binary)
  }

  dispose(): void {
    this.renderTarget.dispose()
  }
}
