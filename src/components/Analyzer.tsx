import React, { useState, useRef, useEffect, useCallback } from 'react';
import Editor, { OnMount } from '@monaco-editor/react';
import { invoke } from '@tauri-apps/api/core';
import { useAppStore } from '../store/useAppStore';
import { Finding } from '../types/analysis';
import { AEGEAN_DARK_THEME, AEGEAN_EDITOR_OPTIONS } from '../lib/monacoTheme';
import { 
  Play, 
  AlertCircle,
  FileCode,
  CheckCircle2,
  ShieldAlert,
  Loader2,
  Sparkles
} from 'lucide-react';

import { Language, translations } from '../lib/i18n';

export const Analyzer: React.FC<{ lang?: Language }> = ({ lang = 'EL' }) => {
  const t = translations[lang];
  const [code, setCode] = useState<string>(t.analyzerPlaceholder);
  const [language, setLanguage] = useState<string>('python');
  const [lastError, setLastError] = useState<string | null>(null);
  const { setAnalysisResult, analysisResult, setAnalyzing, isAnalyzing, setView, addToast } = useAppStore();
  const monacoRef = useRef<any>(null);
  const editorRef = useRef<any>(null);

  /* Monaco setup — custom Aegean theme */
  const handleEditorDidMount: OnMount = (editor, monaco) => {
    monacoRef.current = monaco;
    editorRef.current = editor;

    /* Register η custom Aegean θεματική */
    monaco.editor.defineTheme('aegean-dark', AEGEAN_DARK_THEME);
    monaco.editor.setTheme('aegean-dark');
  };

  /* Τοποθέτηση markers όταν αλλάζουν τα αποτελέσματα */
  useEffect(() => {
    if (monacoRef.current && editorRef.current && analysisResult) {
      const markers = analysisResult.pillars.flatMap(p => 
        p.findings.map((f: Finding) => ({
          startLineNumber: f.line,
          startColumn: 1,
          endLineNumber: f.line,
          endColumn: 1000,
          message: `${f.message}\n\nRationale: ${f.rationale}\nAlternative: ${f.human_alternative}`,
          severity: monacoRef.current.MarkerSeverity.Warning
        }))
      );
      monacoRef.current.editor.setModelMarkers(editorRef.current.getModel(), 'owner', markers);

      /* Gutter decorations */
      const decorations = analysisResult.pillars.flatMap(p => 
        p.findings.map((f: Finding) => ({
          range: new monacoRef.current.Range(f.line, 1, f.line, 1),
          options: {
            isWholeLine: true,
            glyphMarginClassName: 'slop-gutter-icon',
            glyphMarginHoverMessage: { value: f.message }
          }
        }))
      );
      
      const oldDecorations = editorRef.current.getModel()._slopDecorations || [];
      editorRef.current.getModel()._slopDecorations = editorRef.current.deltaDecorations(oldDecorations, decorations);
    }
  }, [analysisResult]);

  /* Εκτέλεση ανάλυσης */
  const handleAnalyze = useCallback(async () => {
    if (!code.trim() || isAnalyzing) return;

    setAnalyzing(true);
    setLastError(null);
    try {
      const sensitivity = localStorage.getItem('slop_sensitivity') || '50';
      const experimental = localStorage.getItem('slop_experimental') === 'true';
      const humanity_shield = localStorage.getItem('slop_humanity_shield') !== 'false'; // Default to true

      const rawResult: string = await invoke('analyze_code', { 
        code, 
        language,
        settings: {
          sensitivity: parseInt(sensitivity),
          experimental,
          humanity_shield
        }
      });
      const result = JSON.parse(rawResult);
      
      if (result.error) {
        throw new Error(result.error);
      }
      
      setAnalysisResult(result);
      addToast('Η ανάλυση ολοκληρώθηκε με επιτυχία', 'success');
      setView('dashboard');
    } catch (error) {
      console.error('Analysis failed:', error);
      const errorMsg = String(error);
      setLastError(errorMsg);
      addToast('Η ανάλυση απέτυχε', 'error');
    } finally {
      setAnalyzing(false);
    }
  }, [code, language, isAnalyzing, setAnalyzing, setAnalysisResult, addToast, setView]);

  /* Ctrl+Enter shortcut */
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        handleAnalyze();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [handleAnalyze]);

  /* Μέτρηση γραμμών */
  const lineCount = code.split('\n').length;

  return (
    <div className="flex flex-col h-[calc(100vh-32px)] overflow-hidden bg-bg rounded-3xl border border-white/[0.04] shadow-strong mx-3 md:mx-6 mb-4 mt-4 anim-scale-in">
      
      {/* ═══ Toolbar ═══ */}
      <header className="h-[68px] border-b border-white/[0.04] flex items-center justify-between px-6 bg-surface/40 backdrop-blur-md shrink-0">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-accent-primary/[0.08] rounded-xl border border-accent-primary/[0.12]">
            <FileCode className="text-accent-primary" size={20} />
          </div>
          <div>
            <h2 className="text-base font-bold text-white tracking-tight leading-tight">Code Analyzer</h2>
            <div className="flex items-center space-x-2">
              <span className="w-1.5 h-1.5 rounded-full bg-human animate-pulse" />
              <p className="text-[9px] text-text-secondary uppercase font-bold tracking-[0.15em]">Neural Engine Active</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          {/* Μετρητής γραμμών */}
          <div className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 bg-white/[0.03] rounded-lg border border-white/[0.04]">
            <Sparkles size={12} className="text-text-disabled" />
            <span className="text-[10px] font-mono text-text-secondary">{lineCount} lines</span>
          </div>

          {/* Language Selector */}
          <select 
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="appearance-none bg-white/[0.04] border border-white/[0.06] rounded-xl px-4 py-2 pr-8 text-xs font-bold text-white focus:outline-none focus:ring-2 focus:ring-accent-primary/40 hover:bg-white/[0.07] transition-all duration-200 cursor-pointer"
          >
            <option value="python">Python 3.x</option>
            <option value="c">C (ANSI/C23)</option>
            <option value="generic">Generic / Other</option>
          </select>

          {/* Analyze Button */}
          <button 
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className={`
              group relative overflow-hidden flex items-center space-x-2.5 px-6 py-2 rounded-xl font-bold transition-all duration-300 active:scale-95
              ${isAnalyzing 
                ? 'bg-white/[0.04] text-text-disabled cursor-not-allowed' 
                : 'bg-accent-primary text-bg hover:shadow-lg hover:shadow-accent-primary/25 hover:scale-[1.02]'
              }
            `}
          >
            {isAnalyzing ? (
              <Loader2 className="animate-spin" size={16} />
            ) : (
              <Play size={16} className="fill-current group-hover:translate-x-0.5 transition-transform" />
            )}
            <span className="uppercase tracking-[0.15em] text-[11px]">{isAnalyzing ? t.analyzingBtn : t.analyzeBtn}</span>
            {!isAnalyzing && (
              <kbd className="hidden lg:inline-block ml-1.5 px-1 py-0.5 bg-white/10 rounded text-[9px] font-mono tracking-normal normal-case">⌘↵</kbd>
            )}
          </button>
        </div>
      </header>

      {/* ═══ Main content ═══ */}
      <main className="flex-1 flex overflow-hidden">

        {/* Editor */}
        <div className="flex-1 relative flex flex-col">
          {lastError && (
            <div className="bg-red-500/10 border-b border-red-500/20 p-4 anim-slide-down">
              <div className="flex items-center space-x-2 text-red-500 mb-1">
                <AlertCircle size={14} />
                <span className="text-[10px] font-bold uppercase tracking-widest">Engine Error Detail</span>
              </div>
              <code className="text-[11px] text-red-400/80 font-mono break-all line-clamp-2 hover:line-clamp-none cursor-pointer decoration-dotted underline">
                {lastError}
              </code>
            </div>
          )}
          <div className="flex-1 relative">
            <Editor
            height="100%"
            language={language}
            theme="aegean-dark"
            value={code}
            onChange={(v) => setCode(v || '')}
            onMount={handleEditorDidMount}
            options={AEGEAN_EDITOR_OPTIONS}
            loading={
              <div className="flex items-center justify-center h-full bg-bg">
                <div className="flex flex-col items-center space-y-3">
                  <Loader2 size={24} className="animate-spin text-accent-primary" />
                  <span className="text-xs text-text-secondary font-medium">{t.loadingEditor}</span>
                </div>
              </div>
            }
          />
          </div>
        </div>

        {/* ═══ Info Sidebar ═══ */}
        <aside className="w-80 border-l border-white/[0.04] bg-surface/20 backdrop-blur-sm p-6 space-y-8 hidden lg:flex flex-col overflow-y-auto">
          
          {/* How it works */}
          <div className="space-y-5 anim-slide-up">
            <h3 className="text-[10px] uppercase tracking-[0.2em] text-white font-black opacity-90">{t.howItWorks}</h3>
            <ul className="space-y-4">
              {t.features.map((item: any, idx: number) => (
                <li key={item.title} className={`flex items-start space-x-3 group ${idx === 1 ? 'anim-delay-100' : idx === 2 ? 'anim-delay-200' : ''}`}>
                  <div className="p-1.5 bg-human/[0.08] rounded-lg group-hover:bg-human/[0.14] transition-colors duration-300 shrink-0 mt-0.5">
                    <CheckCircle2 size={14} className="text-human" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-white mb-0.5 leading-tight">{item.title}</p>
                    <p className="text-[11px] text-text-secondary leading-relaxed">{item.desc}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          {/* Spacer */}
          <div className="flex-1" />

          {/* Privacy notice */}
          <div className="p-5 bg-slop/[0.04] rounded-2xl border border-slop/[0.06] space-y-2.5 relative overflow-hidden group anim-slide-up anim-delay-300">
            <div className="absolute top-0 right-0 p-3 opacity-[0.05] group-hover:rotate-12 transition-transform duration-500">
              <ShieldAlert size={36} className="text-slop" />
            </div>
            <div className="flex items-center space-x-2 text-slop">
              <AlertCircle size={14} />
              <span className="text-[10px] font-bold uppercase tracking-[0.15em]">{t.privacyTitle}</span>
            </div>
            <p className="text-[11px] text-text-secondary leading-relaxed relative z-10">
              {t.privacyDesc}
            </p>
          </div>
        </aside>
      </main>
    </div>
  );
};
