import { create } from 'zustand';
import { AnalysisResult } from '../types/analysis';

export type View = 'wizard' | 'dashboard' | 'analyzer' | 'audit' | 'config' | 'help';

interface Toast {
    message: string;
    type: 'success' | 'error' | 'info';
    id: number;
}

export interface AuditResult {
  path: string;
  name: string;
  result: AnalysisResult | null;
  status: 'pending' | 'analyzing' | 'done' | 'error';
  error?: string;
  code?: string;
}

interface AppState {
    currentView: View;
    analysisResult: AnalysisResult | null;
    isAnalyzing: boolean;
    analyzedCode: string;
    templateCode: string;
    isTemplateMode: boolean;
    targetLine: number | null;
    toasts: Toast[];
    
    // Audit State
    auditResults: AuditResult[];
    isAuditing: boolean;
    theme: 'dark' | 'light';
    lang: 'EL' | 'EN';
    
    // Actions
    setView: (view: View) => void;
    setTheme: (theme: 'dark' | 'light') => void;
    setLang: (lang: 'EL' | 'EN') => void;
    setAnalysisResult: (result: AnalysisResult | null) => void;
    setAnalyzing: (loading: boolean | ((prev: boolean) => boolean)) => void;
    setAnalyzedCode: (code: string) => void;
    setTemplateCode: (code: string) => void;
    setTemplateMode: (active: boolean | ((prev: boolean) => boolean)) => void;
    setTargetLine: (line: number | null) => void;
    setAuditResults: (results: AuditResult[] | ((prev: AuditResult[]) => AuditResult[])) => void;
    setIsAuditing: (active: boolean | ((prev: boolean) => boolean)) => void;
    addToast: (message: string, type?: 'success' | 'error' | 'info') => void;
    removeToast: (id: number) => void;
    clearAnalysis: () => void;
}

export const useAppStore = create<AppState>((set) => ({
    currentView: 'wizard',
    analysisResult: null,
    isAnalyzing: false,
    analyzedCode: '',
    templateCode: '',
    isTemplateMode: false,
    targetLine: null,
    toasts: [],
    auditResults: [],
    isAuditing: false,
    theme: 'dark',
    lang: 'EL',

    setView: (view) => set({ currentView: view }),
    setTheme: (theme) => set({ theme }),
    setLang: (lang) => set({ lang }),
    setAnalysisResult: (result) => set({ analysisResult: result }),
    setAnalyzing: (loading) => set((state) => ({ 
        isAnalyzing: typeof loading === 'function' ? loading(state.isAnalyzing) : loading 
    })),
    setAnalyzedCode: (code) => set({ analyzedCode: code }),
    setTemplateCode: (code) => set({ templateCode: code }),
    setTemplateMode: (active) => set((state) => ({ 
        isTemplateMode: typeof active === 'function' ? active(state.isTemplateMode) : active 
    })),
    setTargetLine: (line) => set({ targetLine: line }),
    setAuditResults: (results) => set((state) => ({ 
        auditResults: typeof results === 'function' ? results(state.auditResults) : results 
    })),
    setIsAuditing: (active) => set((state) => ({ 
        isAuditing: typeof active === 'function' ? active(state.isAuditing) : active 
    })),
    
    addToast: (message, type = 'info') => {
        const id = Date.now();
        set((state) => ({ toasts: [...state.toasts, { message, type, id }] }));
        setTimeout(() => {
            set((state) => ({ toasts: state.toasts.filter(t => t.id !== id) }));
        }, 3000);
    },
    removeToast: (id) => set((state) => ({ toasts: state.toasts.filter(t => t.id !== id) })),
    clearAnalysis: () => set({ 
        analysisResult: null, 
        analyzedCode: '', 
        templateCode: '',
        targetLine: null,
        isAnalyzing: false 
    }),
}));
