import { create } from 'zustand'
import type { QuerySession, QuerySessionHeader } from '../types'

interface QueryLogState {
  sessions: QuerySessionHeader[]
  activeSession: QuerySession | null
  pollingSessionId: string | null

  setSessions: (s: QuerySessionHeader[]) => void
  setActiveSession: (s: QuerySession | null) => void
  setPollingSessionId: (id: string | null) => void
  updateActiveSession: (s: QuerySession) => void
}

export const useQueryLogStore = create<QueryLogState>((set) => ({
  sessions: [],
  activeSession: null,
  pollingSessionId: null,

  setSessions: (sessions) => set({ sessions }),
  setActiveSession: (activeSession) => set({ activeSession }),
  setPollingSessionId: (pollingSessionId) => set({ pollingSessionId }),
  updateActiveSession: (s) => set({ activeSession: s }),
}))
