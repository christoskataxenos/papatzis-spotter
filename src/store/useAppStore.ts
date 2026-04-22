import { create } from 'zustand';
import { AnalysisResult } from '../types/analysis';

export type View = 'wizard' | 'dashboard' | 'analyzer' | 'audit' | 'config' | 'help';

interface Toast {
    message: string;
    type: 'success' | 'error' | 'info';
    id: number;
}

interface AppState {
    currentView: View;
    analysisResult: AnalysisResult | null;
    isAnalyzing: boolean;
    toasts: Toast[];
    
    // Actions
    setView: (view: View) => void;
    setAnalysisResult: (result: AnalysisResult | null) => void;
    setAnalyzing: (loading: boolean) => void;
    addToast: (message: string, type?: 'success' | 'error' | 'info') => void;
    removeToast: (id: number) => void;
}

export const useAppStore = create<AppState>((set) => ({
    currentView: 'wizard',
    analysisResult: null,
    isAnalyzing: false,
    toasts: [],

    setView: (view) => set({ currentView: view }),
    setAnalysisResult: (result) => set({ analysisResult: result }),
    setAnalyzing: (loading) => set({ isAnalyzing: loading }),
    
    addToast: (message, type = 'info') => {
        const id = Date.now();
        set((state) => ({ toasts: [...state.toasts, { message, type, id }] }));
        setTimeout(() => {
            set((state) => ({ toasts: state.toasts.filter(t => t.id !== id) }));
        }, 3000);
    },
    removeToast: (id) => set((state) => ({ toasts: state.toasts.filter(t => t.id !== id) })),
}));
