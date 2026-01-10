import { create } from "zustand";

export type ChancellorEvent = {
  at: number;
  type: string;
  data: unknown;
};

type State = {
  connected: boolean;
  trinityScore: number | null;
  activePillar: string | null;
  thoughts: string[];
  lastEventAt: number | null;
  events: ChancellorEvent[];

  setConnected: (v: boolean) => void;
  setTrinityScore: (v: number | null) => void;
  setActivePillar: (v: string | null) => void;
  pushThought: (t: string) => void;
  pushEvent: (e: ChancellorEvent) => void;
};

export const useChancellorStore = create<State>((set) => ({
  connected: false,
  trinityScore: null,
  activePillar: null,
  thoughts: [],
  lastEventAt: null,
  events: [],

  setConnected: (v) => set({ connected: v }),
  setTrinityScore: (v) => set({ trinityScore: v, lastEventAt: Date.now() }),
  setActivePillar: (v) => set({ activePillar: v, lastEventAt: Date.now() }),
  pushThought: (t) =>
    set((s) => ({
      thoughts: [t, ...s.thoughts].slice(0, 50),
      lastEventAt: Date.now(),
    })),
  pushEvent: (e) =>
    set((s) => ({ events: [e, ...s.events].slice(0, 200) })),
}));
