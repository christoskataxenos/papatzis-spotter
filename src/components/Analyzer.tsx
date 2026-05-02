import React, { useState, useRef, useEffect, useCallback } from 'react';
import Editor, { OnMount } from '@monaco-editor/react';
import { invoke } from '@tauri-apps/api/core';
import { useAppStore } from '../store/useAppStore';
import { Finding } from '../types/analysis';
import { AEGEAN_DARK_THEME, AEGEAN_LIGHT_THEME, AEGEAN_EDITOR_OPTIONS } from '../lib/monacoTheme';
import { 
  Play, 
  AlertCircle,
  FileCode,
  CheckCircle2,
  ShieldAlert,
  Loader2,
  Sparkles,
  Search,
  ArrowRight,
  Zap,
  AlignLeft,
  MessageSquare,
  BarChart3,
  RotateCcw,
  LayoutTemplate,
  RefreshCcw,
} from 'lucide-react';

import { Language, translations } from '../lib/i18n';

/* ─── Pillar Icon Helper ─── */
const PillarIcon = ({ name }: { name: string }) => {
  const size = 14;
  const strokeWidth = 1.75;
  switch (name) {
    case 'AST_UNIFORMITY': return <AlignLeft size={size} strokeWidth={strokeWidth} />;
    case 'NAMING': return <Zap size={size} strokeWidth={strokeWidth} />;
    case 'STATISTICAL': return <BarChart3 size={size} strokeWidth={strokeWidth} />;
    case 'COMMENTS': return <MessageSquare size={size} strokeWidth={strokeWidth} />;
    case 'DRIFT': return <RotateCcw size={size} strokeWidth={strokeWidth} />;
    case 'INTEGRITY': return <LayoutTemplate size={size} strokeWidth={strokeWidth} />;
    default: return <Zap size={size} strokeWidth={strokeWidth} />;
  }
};

const getPillarColorVar = (name: string) => {
  switch (name) {
    case 'AST_UNIFORMITY': return 'var(--pillar-structure)';
    case 'NAMING': return 'var(--pillar-naming)';
    case 'STATISTICAL': return 'var(--pillar-stat)';
    case 'COMMENTS': return 'var(--pillar-gpt)';
    case 'DRIFT': return 'var(--pillar-drift)';
    case 'INTEGRITY': return 'var(--pillar-template)';
    default: return 'var(--accent-primary)';
  }
};

/* ─── Finding Grouping Helper ─── */
interface GroupedFinding {
  type: string;
  displayType: string;
  messages: Array<{
    text: string;
    findings: Finding[];
  }>;
}

const groupFindingsIntelligently = (findings: Finding[]): GroupedFinding[] => {
  const groups: Record<string, GroupedFinding> = {};
  
  findings.forEach(f => {
    // Determine the main type (e.g. 'naming' from 'naming.lazy')
    const mainType = f.type.split('.')[0] || 'other';
    const displayType = mainType.charAt(0).toUpperCase() + mainType.slice(1);
    
    if (!groups[mainType]) {
      groups[mainType] = { type: mainType, displayType, messages: [] };
    }
    
    const group = groups[mainType];
    const message = f.message;
    
    let existingMessage = group.messages.find(m => m.text === message);
    if (!existingMessage) {
      existingMessage = { text: message, findings: [] };
      group.messages.push(existingMessage);
    }
    existingMessage.findings.push(f);
  });

  return Object.values(groups).sort((a, b) => {
    if (a.type === 'engine' || a.type === 'info') return -1;
    if (b.type === 'engine' || b.type === 'info') return -1;
    
    // Sort groups by their maximum severity finding
    const maxSevA = Math.max(...a.messages.flatMap(m => m.findings.map(f => f.severity)));
    const maxSevB = Math.max(...b.messages.flatMap(m => m.findings.map(f => f.severity)));
    return maxSevB - maxSevA;
  });
};

export const Analyzer: React.FC<{ lang?: Language }> = ({ lang: propLang }) => {
  const { 
    setAnalysisResult, 
    analysisResult, 
    setAnalyzing, 
    isAnalyzing, 
    setView, 
    addToast,
    analyzedCode,
    setAnalyzedCode,
    targetLine,
    templateCode,
    setTemplateCode,
    isTemplateMode,
    setTemplateMode,
    auditResults,
    theme,
    lang: storeLang
  } = useAppStore();

  const lang = propLang || storeLang;
  const t = translations[lang];

  const [code, setCode] = useState<string>(analyzedCode || t.analyzerPlaceholder);
  const [language, setLanguage] = useState<string>('auto');
  const [lastError, setLastError] = useState<string | null>(null);
  const monacoRef = useRef<any>(null);
  const editorRef = useRef<any>(null);
  const [selectedFinding, setSelectedFinding] = useState<Finding | null>(null);
  const [activeTab, setActiveTab] = useState<'code' | 'template'>('code');
  const [collapsedPillars, setCollapsedPillars] = useState<Record<string, boolean>>({});

  const formatPillarName = (key: string) => {
    if (!key) return '';
    if (t.pillarNames[key as keyof typeof t.pillarNames]) {
      return t.pillarNames[key as keyof typeof t.pillarNames];
    }
    return key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
  };

  const togglePillar = (name: string) => {
    setCollapsedPillars(prev => ({ ...prev, [name]: !prev[name] }));
  };

  useEffect(() => {
    if (analyzedCode !== null && analyzedCode !== undefined) {
      setCode(analyzedCode);
    }
  }, [analyzedCode]);

  const forceRefresh = () => {
    if (analyzedCode) {
      setCode(analyzedCode);
      addToast(t.codeRefreshed, 'info');
    }
  };

  useEffect(() => {
    if (editorRef.current && targetLine) {
      setTimeout(() => {
        editorRef.current.revealLineInCenter(targetLine);
        editorRef.current.setPosition({ lineNumber: targetLine, column: 1 });
        editorRef.current.focus();
        
        if (analysisResult) {
          const findingAtLine = analysisResult.pillars
            .flatMap(p => p.findings)
            .find((f: Finding) => f.line === targetLine);
          setSelectedFinding(findingAtLine || null);
        }
      }, 200); 
    }
  }, [targetLine, analysisResult]);

  const handleEditorDidMount: OnMount = (editor, monaco) => {
    monacoRef.current = monaco;
    editorRef.current = editor;

    monaco.editor.defineTheme('aegean-dark', AEGEAN_DARK_THEME);
    monaco.editor.defineTheme('aegean-light', AEGEAN_LIGHT_THEME);
    monaco.editor.setTheme(theme === 'dark' ? 'aegean-dark' : 'aegean-light');
  };

  useEffect(() => {
    if (monacoRef.current) {
      monacoRef.current.editor.setTheme(theme === 'dark' ? 'aegean-dark' : 'aegean-light');
    }
  }, [theme]);

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

      const decorations = analysisResult.pillars.flatMap(p => 
        p.findings.map((f: Finding) => {
          let severityClass = 'slop-gutter-icon';
          if (f.severity > 0.7) severityClass += ' slop-gutter-icon-high';
          else if (f.severity > 0.4) severityClass += ' slop-gutter-icon-medium';
          else severityClass += ' slop-gutter-icon-low';

          return {
            range: new monacoRef.current.Range(f.line, 1, f.line, 1),
            options: {
              isWholeLine: true,
              glyphMarginClassName: severityClass,
              glyphMarginHoverMessage: { value: f.message }
            }
          };
        })
      );
      
      const oldDecorations = editorRef.current.getModel()._slopDecorations || [];
      editorRef.current.getModel()._slopDecorations = editorRef.current.deltaDecorations(oldDecorations, decorations);

      const disposable = editorRef.current.onDidChangeCursorPosition((e: any) => {
        const findingAtLine = analysisResult.pillars
          .flatMap(p => p.findings)
          .find((f: Finding) => f.line === e.position.lineNumber);
        setSelectedFinding(findingAtLine || null);
      });
      
      return () => disposable.dispose();
    }
  }, [analysisResult]);

  useEffect(() => {
    if (editorRef.current && monacoRef.current) {
      const model = editorRef.current.getModel();
      if (!model) return;

      const newDecorations: any[] = [];
      if (selectedFinding) {
        newDecorations.push({
          range: new monacoRef.current.Range(selectedFinding.line, 1, selectedFinding.line, 1),
          options: {
            isWholeLine: true,
            className: 'active-finding-line',
            marginClassName: 'active-finding-margin'
          }
        });
      }

      const oldDecorations = model._activeFindingDecorations || [];
      model._activeFindingDecorations = editorRef.current.deltaDecorations(oldDecorations, newDecorations);
    }
  }, [selectedFinding]);

  const handleAnalyze = useCallback(async () => {
    if (!code.trim() || isAnalyzing) return;

    setAnalyzing(true);
    setLastError(null);
    try {
      const sensitivity = localStorage.getItem('slop_sensitivity') || '75';
      const humanityShield = localStorage.getItem('slop_humanity_shield') !== 'false';
      const experimental = localStorage.getItem('slop_experimental') !== 'false';

      const rawResult: string = await invoke('analyze_code', { 
        code, 
        language,
        template: isTemplateMode ? templateCode : undefined,
        settings: {
          sensitivity: parseInt(sensitivity),
          experimental,
          humanity_shield: humanityShield,
          ui_lang: lang
        }
      });
      const result = JSON.parse(rawResult);
      
      if (result.error) {
        throw new Error(result.error);
      }
      
      setAnalysisResult(result);
      setAnalyzedCode(code);
      addToast(t.analysisSuccess, 'success');
      setView('dashboard');
    } catch (error) {
      console.error('Analysis failed:', error);
      const errorMsg = String(error);
      setLastError(errorMsg);
      addToast(t.analysisFailed, 'error');
    } finally {
      setAnalyzing(false);
    }
  }, [code, language, isAnalyzing, setAnalyzing, setAnalysisResult, setAnalyzedCode, addToast, setView, isTemplateMode, templateCode, lang]);

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

  const lineCount = code.split('\n').length;
  const auditResultsArray = Array.isArray(auditResults) ? auditResults : [];

  return (
    <div className="flex flex-col h-[calc(100vh-32px)] overflow-hidden bg-bg rounded-3xl border border-border-subtle shadow-strong mx-3 md:mx-6 mb-4 mt-4 anim-scale-in">
      
      <header className="h-[68px] border-b border-border-subtle flex items-center justify-between px-6 bg-surface/40 backdrop-blur-md shrink-0">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-accent-primary/[0.08] rounded-xl border border-accent-primary/[0.12]">
            <FileCode className="text-accent-primary" size={20} strokeWidth={1.75} />
          </div>
          <div>
            <h2 className="text-base font-bold text-text-primary tracking-tight leading-tight">{t.codeAnalyzer}</h2>
            <div className="flex items-center space-x-2">
              <span className="w-1.5 h-1.5 rounded-full bg-human animate-pulse" />
              <p className="text-[9px] text-text-secondary uppercase font-bold tracking-[0.15em] opacity-80">{t.neuralEngine}</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-5">
          {auditResultsArray.length > 0 && (
            <button 
              onClick={() => setView('audit')}
              className="flex items-center space-x-2 px-4 py-2 bg-accent-primary text-white rounded-xl font-bold hover:scale-[1.03] transition-all duration-200 shadow-lg shadow-accent-primary/10"
              title="Back to Batch Audit Results"
            >
              <ArrowRight size={14} strokeWidth={1.75} className="rotate-180" />
              <span className="uppercase tracking-[0.1em] text-[10px]">Back to Audit</span>
            </button>
          )}

          {/* Μετρητής γραμμών */}
          <div className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 bg-surface-elevated rounded-lg border border-border-subtle">
            <Sparkles size={12} strokeWidth={1.75} className="text-text-disabled" />
            <span className="text-[10px] font-mono text-text-secondary">{lineCount} lines</span>
          </div>

          {/* Language Selector */}
          <select 
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="appearance-none bg-surface-elevated border border-border-default rounded-xl px-4 py-2 pr-8 text-xs font-bold text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary/40 hover:bg-surface-hover transition-all duration-200 cursor-pointer"
          >
            <option value="auto">Auto-Detect</option>
            <option value="python">Python 3.x</option>
            <option value="c">C (ANSI/C23)</option>
            <option value="generic">Generic / Other</option>
          </select>

          {/* Template Mode Toggle */}
          <button 
            onClick={() => {
              setTemplateMode(!isTemplateMode);
              if (!isTemplateMode) setActiveTab('template');
              else setActiveTab('code');
            }}
            title={t.templateModeDesc}
            className={`
              flex items-center space-x-2 px-4 py-2 rounded-xl font-bold transition-all duration-200 border
              ${isTemplateMode 
                ? 'bg-human/10 border-human/30 text-human shadow-lg shadow-human/10' 
                : 'bg-surface-elevated border-border-default text-text-disabled hover:bg-surface-hover'
              }
            `}
          >
            <LayoutTemplate size={16} strokeWidth={1.75} />
            <span className="uppercase tracking-[0.1em] text-[10px]">{t.templateMode}</span>
          </button>

          {/* Sync Button */}
          <button 
            onClick={forceRefresh}
            title="Force Sync with Store"
            className="p-2.5 bg-surface-elevated border border-border-default text-text-disabled hover:bg-surface-hover hover:text-accent-primary rounded-xl transition-all duration-200"
          >
            <RefreshCcw size={16} strokeWidth={1.75} />
          </button>

          {/* Analyze Button */}
          <button 
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className={`
              group relative overflow-hidden flex items-center space-x-2.5 px-6 py-2 rounded-xl font-bold transition-all duration-300 active:scale-95
              ${isAnalyzing 
                ? 'bg-surface-elevated text-text-disabled cursor-not-allowed' 
                : 'bg-accent-primary text-white hover:shadow-lg hover:shadow-accent-primary/25 hover:scale-[1.02]'
              }
            `}
          >
            {isAnalyzing ? (
              <Loader2 className="animate-spin" size={16} strokeWidth={1.75} />
            ) : (
              <Play size={16} strokeWidth={1.75} className="fill-current group-hover:translate-x-0.5 transition-transform" />
            )}
            <span className="uppercase tracking-[0.15em] text-[11px]">{isAnalyzing ? t.analyzingBtn : t.analyzeBtn}</span>
            {!isAnalyzing && (
              <kbd className="hidden lg:inline-block ml-1.5 px-1 py-0.5 bg-white/10 rounded text-[9px] font-mono tracking-normal normal-case">⌘↵</kbd>
            )}
          </button>
        </div>
      </header>

      {/* ═══ Editor Tabs (Only in Template Mode) ═══ */}
      {isTemplateMode && (
        <div className="h-10 border-b border-border-subtle bg-surface/20 flex items-center px-6 space-x-6 shrink-0">
          <button 
            onClick={() => setActiveTab('template')}
            className={`
              h-full flex items-center space-x-2 text-[10px] uppercase font-black tracking-widest border-b-2 transition-all
              ${activeTab === 'template' 
                ? 'text-human border-human' 
                : 'text-text-disabled border-transparent hover:text-text-secondary'
              }
            `}
          >
            <LayoutTemplate size={12} strokeWidth={1.75} />
            <span>{t.templateTitle}</span>
          </button>
          <button 
            onClick={() => setActiveTab('code')}
            className={`
              h-full flex items-center space-x-2 text-[10px] uppercase font-black tracking-widest border-b-2 transition-all
              ${activeTab === 'code' 
                ? 'text-accent-primary border-accent-primary' 
                : 'text-text-disabled border-transparent hover:text-text-secondary'
              }
            `}
          >
            <FileCode size={12} strokeWidth={1.75} />
            <span>{t.codeTitle}</span>
          </button>
        </div>
      )}

      {/* ═══ Main content ═══ */}
      <main className="flex-1 flex overflow-x-auto overflow-y-hidden bg-bg">

        {/* Editor Area */}
        <div className="flex-1 relative flex flex-col min-w-[320px] border-r border-border-subtle/50">
          {lastError && (
            <div className="bg-slop/10 border-b border-slop/20 p-4 anim-slide-down">
              <div className="flex items-center space-x-2 text-slop mb-1">
                <AlertCircle size={14} strokeWidth={1.75} />
                <span className="text-[10px] font-bold uppercase tracking-widest">{t.engineErrorDetail}</span>
              </div>
              <code className="text-[11px] text-slop/80 font-mono break-all line-clamp-2 hover:line-clamp-none cursor-pointer decoration-dotted underline">
                {lastError}
              </code>
            </div>
          )}
          <div className="flex-1 relative">
            <Editor
            height="100%"
            language={language}
            theme="aegean-dark"
            value={activeTab === 'code' ? code : templateCode}
            onChange={(v) => activeTab === 'code' ? setCode(v || '') : setTemplateCode(v || '')}
            onMount={handleEditorDidMount}
            options={{
              ...AEGEAN_EDITOR_OPTIONS,
              readOnly: isAnalyzing,
              placeholder: activeTab === 'code' ? t.analyzerPlaceholder : t.templatePlaceholder
            }}
            loading={
              <div className="flex items-center justify-center h-full bg-bg">
                <div className="flex flex-col items-center space-y-3">
                  <Loader2 size={24} strokeWidth={1.75} className="animate-spin text-accent-primary" />
                  <span className="text-xs text-text-secondary font-medium">{t.loadingEditor}</span>
                </div>
              </div>
            }
          />
          </div>
        </div>

        {/* ═══ Info Sidebar / Mentor Panel ═══ */}
        <aside className="w-[380px] shrink-0 border-l border-border-subtle bg-surface/20 backdrop-blur-sm p-6 space-y-8 flex flex-col overflow-y-auto">
          
          {selectedFinding ? (
            /* ─── Detail View: Mentor's Note ─── */
            <div className="space-y-6 anim-slide-up">
              <button 
                onClick={() => setSelectedFinding(null)}
                className="flex items-center space-x-2 text-text-secondary hover:text-text-primary transition-colors text-[10px] uppercase font-black tracking-widest"
              >
                <ArrowRight size={14} strokeWidth={1.75} className="rotate-180" />
                <span>{t.backToList}</span>
              </button>

              <div className="flex items-center space-x-3 text-slop">
                <ShieldAlert size={20} strokeWidth={1.75} />
                <h3 className="text-[10px] uppercase tracking-[0.2em] font-black italic">{t.mentorNote}</h3>
              </div>
              
              <div className="space-y-4">
                <div className="p-4 bg-surface-elevated border border-border-default rounded-2xl space-y-3">
                  <p className="text-xs font-bold text-text-primary leading-tight">{selectedFinding.message}</p>
                  <p className="text-[11px] text-text-secondary leading-loose italic">"{selectedFinding.rationale}"</p>
                </div>

                <div className="p-4 bg-human/[0.05] border border-human/[0.1] rounded-2xl space-y-3">
                  <div className="flex items-center space-x-2 text-human">
                    <Sparkles size={14} strokeWidth={1.75} />
                    <span className="text-[10px] font-black uppercase tracking-widest">{t.humanTouchLabel}</span>
                  </div>
                  <p className="text-xs text-text-primary font-medium leading-loose">
                    {selectedFinding.human_alternative}
                  </p>
                </div>
              </div>
            </div>
          ) : analysisResult ? (
            /* ─── List View: All Findings ─── */
            <div className="space-y-6 anim-slide-up">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3 text-text-primary opacity-90">
                  <Search size={18} strokeWidth={1.75} />
                  <h3 className="text-[10px] uppercase tracking-[0.2em] font-black italic">{t.findingsLabel}</h3>
                </div>
                <div className="flex items-center space-x-2">
                  <button 
                    onClick={() => {
                      const allPillars = analysisResult.pillars.map(p => p.pillar);
                      const areAllCollapsed = allPillars.every(name => collapsedPillars[name]);
                      const next = {} as Record<string, boolean>;
                      allPillars.forEach(n => next[n] = !areAllCollapsed);
                      setCollapsedPillars(next);
                    }}
                    className="text-[9px] uppercase font-black tracking-widest text-text-disabled hover:text-accent-primary transition-colors"
                  >
                    {analysisResult.pillars.map(p => p.pillar).every(n => collapsedPillars[n]) ? t.expandAll : t.collapseAll}
                  </button>
                  <span className="px-2 py-0.5 bg-surface-elevated rounded text-[10px] font-mono text-text-secondary border border-border-default">
                    {analysisResult.pillars.reduce((acc, p) => acc + p.findings.length, 0)} {t.issuesCount}
                  </span>
                </div>
              </div>

              <div className="space-y-6">
                {analysisResult.pillars
                  .filter(p => p.findings.length > 0)
                    .map((p, pIdx) => {
                      const intelligentlyGrouped = groupFindingsIntelligently(p.findings);
                      const isCollapsed = collapsedPillars[p.pillar];

                      return (
                        <div key={pIdx} className="space-y-4">
                          <button 
                            onClick={() => togglePillar(p.pillar)}
                            className="w-full flex items-center justify-between text-text-secondary hover:text-text-primary transition-colors group/pillar"
                          >
                            <div className="flex items-center space-x-2">
                              <div 
                                className="p-1 rounded transition-transform group-hover/pillar:scale-110"
                                style={{ backgroundColor: `${getPillarColorVar(p.pillar)}15`, color: getPillarColorVar(p.pillar) }}
                              >
                                <PillarIcon name={p.pillar} />
                              </div>
                              <h4 className="text-[10px] uppercase font-black tracking-[0.15em] text-text-primary opacity-80">{formatPillarName(p.pillar)}</h4>
                            </div>
                            <span className="text-[10px] font-mono opacity-30">{isCollapsed ? '+' : '−'}</span>
                          </button>
                        
                        {!isCollapsed && (
                          <div className="space-y-6 pl-2 border-l border-border-subtle/30 ml-3 anim-slide-down">
                            {intelligentlyGrouped.map((typeGroup, tIdx) => (
                              <div key={tIdx} className="space-y-3">
                                {/* Type Subheader */}
                                {typeGroup.type !== 'engine' && typeGroup.type !== 'info' && (
                                  <div className="flex items-center space-x-2 opacity-40">
                                    <div className="h-[1px] w-4 bg-current" />
                                    <span className="text-[9px] uppercase font-bold tracking-widest">{typeGroup.displayType}</span>
                                  </div>
                                )}
                                
                                {typeGroup.messages.map((group, mIdx) => {
                                  const avgSeverity = group.findings.reduce((acc, f) => acc + f.severity, 0) / group.findings.length;
                                  const isHighRisk = avgSeverity > 0.8;
                                  const severityColor = avgSeverity > 0.7 ? 'var(--slop)' : avgSeverity > 0.4 ? 'var(--accent-primary)' : 'var(--human)';

                                  return (
                                    <div
                                      key={mIdx}
                                      className={`
                                        w-full p-4 border rounded-2xl transition-all duration-300 group/card relative overflow-hidden
                                        ${isHighRisk 
                                          ? 'bg-slop/[0.04] border-slop/30 shadow-[0_0_15px_-5px_var(--slop)]' 
                                          : 'bg-surface/40 border-border-subtle hover:border-border-default hover:bg-surface/60'
                                        }
                                      `}
                                    >
                                      {/* Severity Indicator Line */}
                                      <div 
                                        className={`absolute left-0 top-0 bottom-0 w-1 transition-opacity ${isHighRisk ? 'opacity-100' : 'opacity-60'}`}
                                        style={{ backgroundColor: severityColor }}
                                      />

                                      <div className="flex items-start justify-between mb-2 pl-1">
                                        <p className={`text-[11px] font-bold leading-snug transition-colors ${isHighRisk ? 'text-slop' : 'text-text-primary group-hover/card:text-accent-primary'}`}>
                                          {group.text}
                                        </p>
                                        {isHighRisk && (
                                          <span className="shrink-0 text-[8px] font-black bg-slop text-white px-1.5 py-0.5 rounded-sm animate-pulse tracking-tighter">
                                            HIGH RISK
                                          </span>
                                        )}
                                      </div>
                                      
                                      <div className="flex flex-wrap gap-1.5 pl-1">
                                        {group.findings.map((f, fIdx) => (
                                          <button
                                            key={fIdx}
                                            onClick={() => {
                                              setSelectedFinding(f);
                                              editorRef.current.revealLineInCenter(f.line);
                                              editorRef.current.setPosition({ lineNumber: f.line, column: 1 });
                                              editorRef.current.focus();
                                            }}
                                            className="px-2 py-1 bg-surface-elevated hover:bg-accent-primary hover:text-white border border-border-subtle rounded-lg text-[9px] font-mono font-bold text-text-secondary transition-all"
                                          >
                                            L{f.line}
                                          </button>
                                        ))}
                                      </div>
                                    </div>
                                  );
                                })}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
              </div>
            </div>
          ) : (
            /* ─── Initial View: How it works ─── */
            <div className="space-y-5 anim-slide-up">
              <h3 className="text-[10px] uppercase tracking-[0.2em] text-text-primary font-black opacity-90">{t.howItWorks}</h3>
              <ul className="space-y-4">
                {t.features.map((item: any, idx: number) => (
                  <li key={item.title} className={`flex items-start space-x-3 group ${idx === 1 ? 'anim-delay-100' : idx === 2 ? 'anim-delay-200' : ''}`}>
                    <div className="p-1.5 bg-human/[0.08] rounded-lg group-hover:bg-human/[0.14] transition-colors duration-300 shrink-0 mt-0.5">
                      <CheckCircle2 size={14} strokeWidth={1.75} className="text-human" />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-text-primary mb-0.5 leading-tight">{item.title}</p>
                      <p className="text-[11px] text-text-secondary leading-relaxed">{item.desc}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Spacer */}
          <div className="flex-1" />

          {/* Privacy notice */}
          {!selectedFinding && (
            <div className="p-5 bg-slop/[0.04] rounded-2xl border border-slop/[0.06] space-y-2.5 relative overflow-hidden group anim-slide-up anim-delay-300">
              <div className="absolute top-0 right-0 p-3 opacity-[0.05] group-hover:rotate-12 transition-transform duration-700">
                <ShieldAlert size={36} strokeWidth={1.75} className="text-slop" />
              </div>
              <div className="flex items-center space-x-2 text-slop">
                <AlertCircle size={14} strokeWidth={1.75} />
                <span className="text-[10px] font-bold uppercase tracking-[0.15em]">{t.privacyTitle}</span>
              </div>
              <p className="text-[11px] text-text-secondary leading-relaxed relative z-10">
                {t.privacyDesc}
              </p>
            </div>
          )}
        </aside>
      </main>
    </div>
  );
};
