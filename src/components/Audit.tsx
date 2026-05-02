import React from 'react';
import { Search, FolderOpen, FileCode, CheckCircle2, AlertCircle, ArrowRight, Loader2, BarChart3 } from 'lucide-react';
import { open } from '@tauri-apps/plugin-dialog';
import { readDir, readTextFile } from '@tauri-apps/plugin-fs';
import { invoke } from '@tauri-apps/api/core';
import { useAppStore } from '../store/useAppStore';
import { AnalysisResult } from '../types/analysis';

interface AuditResult {
  path: string;
  name: string;
  result: AnalysisResult | null;
  status: 'pending' | 'analyzing' | 'done' | 'error';
  error?: string;
  code?: string;
}

import { Language, translations } from '../lib/i18n';

export const Audit: React.FC<{ lang: Language }> = ({ lang }) => {
  const t = translations[lang];
  const { 
    setAnalysisResult, 
    setView, 
    addToast, 
    setAnalyzedCode,
    auditResults: results,
    setAuditResults: setResults,
    isAuditing,
    setIsAuditing
  } = useAppStore();

  /* Αναδρομική σάρωση φακέλου */
  const scanDirectory = async (path: string): Promise<string[]> => {
    const entries = await readDir(path);
    let files: string[] = [];

    for (const entry of entries) {
      const entryPath = `${path}/${entry.name}`;
      if (entry.isDirectory) {
        files = [...files, ...(await scanDirectory(entryPath))];
      } else if (entry.isFile) {
        if (entry.name.endsWith('.py') || entry.name.endsWith('.c')) {
          files.push(entryPath);
        }
      }
    }
    return files;
  };

  const handlePickDirectory = async () => {
    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: t.pickFolderTitle
      });

      if (selected && typeof selected === 'string') {
        setIsAuditing(true);
        const filePaths = await scanDirectory(selected);
        
        const initialResults: AuditResult[] = filePaths.map(p => ({
          path: p,
          name: p.split(/[/\\]/).pop() || p,
          result: null,
          status: 'pending'
        }));
        
        setResults(initialResults);
        
        for (let i = 0; i < initialResults.length; i++) {
          setResults(prev => prev.map((r, idx) => i === idx ? { ...r, status: 'analyzing' } : r));
          
          try {
            const content = await readTextFile(initialResults[i].path);
            const lang = initialResults[i].path.toLowerCase().endsWith('.py') ? 'python' : 'c';
            
            // Get settings from localStorage (match Analyzer.tsx)
            const sensitivity = localStorage.getItem('slop_sensitivity') || '50';
            const experimental = localStorage.getItem('slop_experimental') === 'true';
            const humanity_shield = localStorage.getItem('slop_humanity_shield') !== 'false';

            const rawResult: string = await invoke('analyze_code', { 
              code: content, 
              language: lang,
              settings: {
                sensitivity: parseInt(sensitivity),
                experimental,
                humanity_shield,
                ui_lang: lang
              }
            });
            const analysis = JSON.parse(rawResult);
            
            setResults(prev => prev.map((r, idx) => i === idx ? { ...r, status: 'done', result: analysis, code: content } : r));
          } catch (err) {
            console.error(`Audit failed for ${initialResults[i].path}:`, err);
            setResults(prev => prev.map((r, idx) => i === idx ? { ...r, status: 'error', error: String(err) } : r));
          }
        }
        addToast(`${t.batchAuditComplete} (${initialResults.length} ${t.files})`, 'success');
      }
    } catch (error) {
      console.error('Audit failed:', error);
      addToast(t.batchAuditFailed, 'error');
    } finally {
      setIsAuditing(false);
    }
  };

  const viewDetails = (res: AuditResult) => {
    if (res.result) setAnalysisResult(res.result);
    if (res.code) setAnalyzedCode(res.code);
    setView('dashboard');
  };

  const inspectCode = async (res: AuditResult) => {
    // Check if we already have the code in cache
    if (res.code && res.result) {
      setAnalyzedCode(res.code);
      setAnalysisResult(res.result);
      setView('analyzer');
    } else {
      // Fallback: Read from disk if missing
      try {
        const content = await readTextFile(res.path);
        setAnalyzedCode(content);
        if (res.result) setAnalysisResult(res.result);
        setView('analyzer');
      } catch (err) {
        console.error("Failed to read file for inspection:", err);
        addToast(t.failedToLoadFile, 'error');
        // Still go to analyzer to show error state if result exists
        if (res.result) {
          setAnalysisResult(res.result);
          setView('analyzer');
        }
      }
    }
  };

  /* Υπολογισμός μέσου score */
  const resultsArray = Array.isArray(results) ? results : [];
  const doneResults = resultsArray.filter(r => r.status === 'done' && r.result);
  const avgScore = doneResults.length > 0 
    ? Math.round(doneResults.reduce((sum, r) => sum + (r.result?.final_score || 0), 0) / doneResults.length)
    : null;

  return (
    <div className="p-4 md:p-6 max-w-[1400px] mx-auto w-full space-y-8 pb-16">
      
      {/* ═══ Header ═══ */}
      <section className="flex flex-col items-center text-center space-y-5 py-8 md:py-10 bg-surface rounded-[2rem] border border-border-subtle relative overflow-hidden anim-scale-in">
        <div className="absolute inset-0 bg-noise" />
        
        <div className="p-4 bg-accent-primary/[0.08] rounded-2xl border border-accent-primary/[0.12] relative z-10">
          <Search className="text-accent-primary" size={36} strokeWidth={1.75} />
        </div>
        <div className="space-y-2 relative z-10">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-text-primary">{t.audit}</h1>
          <p className="text-text-secondary max-w-md mx-auto text-sm leading-relaxed font-medium">
            {t.auditTagline}
          </p>
        </div>

        {/* CTA ή Progress summary */}
        <div className="pt-1.5 z-10">
          {!isAuditing && resultsArray.length === 0 && (
            <button 
              onClick={handlePickDirectory}
              className="flex items-center space-x-3 px-8 py-3.5 bg-accent-primary text-white font-bold rounded-2xl hover:scale-[1.03] transition-all duration-300 shadow-lg shadow-accent-primary/20"
            >
              <FolderOpen size={18} />
              <span className="uppercase tracking-[0.15em] text-[11px]">{t.pickFolder}</span>
            </button>
          )}
          
          {/* Summary stats */}
          {doneResults.length > 0 && (
            <div className="flex items-center space-x-6 anim-fade-in">
              <div className="flex items-center space-x-2">
                <BarChart3 size={16} className="text-accent-primary" />
                <span className="text-sm font-mono font-bold text-text-primary">{t.avgScore}: {avgScore}</span>
              </div>
              <span className="text-text-disabled">·</span>
              <span className="text-xs text-text-secondary font-medium">{doneResults.length} / {resultsArray.length} {t.files}</span>
            </div>
          )}
        </div>
      </section>

      {/* ═══ Results Table ═══ */}
      {resultsArray.length > 0 && (
        <div className="bg-surface rounded-2xl border border-border-subtle overflow-hidden anim-slide-up anim-delay-200">
          <div className="p-4 border-b border-border-subtle flex items-center justify-between bg-surface-elevated/40">
            <h3 className="text-sm font-bold text-text-primary">{t.results} ({resultsArray.length} {t.files})</h3>
            {isAuditing && (
              <div className="flex items-center space-x-2 text-accent-primary">
                <Loader2 size={14} className="animate-spin" />
                <span className="text-[10px] font-bold uppercase tracking-[0.15em]">{t.analyzingInProgress}</span>
              </div>
            )}
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="text-[9px] uppercase font-bold tracking-[0.2em] text-text-disabled border-b border-border-subtle">
                  <th className="px-5 py-2.5">{t.tableFile}</th>
                  <th className="px-5 py-2.5">{t.tableStatus}</th>
                  <th className="px-5 py-2.5 text-center">{t.tableScore}</th>
                  <th className="px-5 py-2.5 text-center">{t.tableFindings}</th>
                  <th className="px-5 py-2.5 text-right">{t.tableAction}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle/50">
                {resultsArray.map((res, i) => (
                  <tr key={i} className="hover:bg-surface-hover/30 transition-colors duration-200 group">
                    <td className="px-5 py-3">
                      <div className="flex items-center space-x-3">
                        <FileCode size={16} className="text-text-disabled shrink-0" />
                        <div className="min-w-0">
                          <p className="text-sm font-bold text-text-primary truncate">{res.name}</p>
                          <p className="text-[10px] text-text-disabled truncate max-w-xs">{res.path}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-3">
                      {res.status === 'analyzing' && <span className="text-[10px] text-accent-primary font-bold animate-pulse uppercase">{t.statusAnalyzing}</span>}
                      {res.status === 'done' && <CheckCircle2 size={16} className="text-human" />}
                      {res.status === 'error' && <AlertCircle size={16} className="text-slop" />}
                      {res.status === 'pending' && <span className="text-[10px] text-text-disabled font-medium uppercase">{t.statusPending}</span>}
                    </td>
                    <td className="px-5 py-3 text-center">
                      {res.result && (
                        <span className="text-base font-mono font-bold" style={{ color: res.result.final_score > 50 ? 'var(--slop)' : 'var(--human)' }}>
                          {Math.round(res.result.final_score)}
                        </span>
                      )}
                    </td>
                    <td className="px-5 py-3 text-center">
                      {res.result && (
                        <span className="px-2 py-0.5 bg-surface-elevated/60 rounded text-xs font-mono font-bold text-text-secondary border border-border-subtle">
                          {res.result.pillars.reduce((acc, p) => acc + p.findings.length, 0)}
                        </span>
                      )}
                    </td>
                    <td className="px-5 py-3 text-right">
                      {res.result && (
                        <div className="flex items-center justify-end space-x-1">
                          <button 
                            onClick={() => inspectCode(res)}
                            className="p-2 hover:bg-accent-primary/[0.08] rounded-lg text-accent-primary transition-all duration-200 opacity-0 group-hover:opacity-100"
                            title={t.inspectCode}
                          >
                            <FileCode size={16} />
                          </button>
                          <button 
                            onClick={() => viewDetails(res)}
                            className="p-2 hover:bg-accent-primary/[0.08] rounded-lg text-accent-primary transition-all duration-200 opacity-0 group-hover:opacity-100"
                            title={t.viewReport}
                          >
                            <ArrowRight size={16} />
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
