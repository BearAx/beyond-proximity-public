# Auto-run query pipeline from UI Ask button

## What was done

- Added `POST /api/query-log/{scene_id}/sessions/run` — creates a session and runs `run_query_session_safe` in a FastAPI background task.
- UI **Ask** now calls `runSession` instead of empty `createSession`; no manual session ID copy into Cursor chat.
- Query Flow auto-opens the new session; ControlPanel polls until `finished_at` and shows result in status bar.

## Why

Manual flow (create session → paste ID into Cursor → agent runs pipeline) was awkward for live demos and daily use.

## Files changed

- `backend/query/live_session.py` — `run_query_session_safe`
- `backend/api/routes/query_log.py` — `/sessions/run` endpoint
- `frontend/src/api/client.ts` — `runSession`
- `frontend/src/components/ControlPanel/ControlPanel.tsx` — auto-run + poll
- `frontend/src/components/QueryFlow/QueryFlow.tsx` — consume `pendingOpenSessionId`

## Verified

- TestClient: `POST .../sessions/run` → session completes with 9 steps, `found: true` for "Find the sofa".

## Next steps

- Restart backend if already running (new route).
- Optional: wire 3D bbox highlight in Navigator when result arrives.
