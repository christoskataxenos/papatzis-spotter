import React, { useEffect, useState } from 'react';
import { useAppStore } from '../store/useAppStore';
import { Language, translations } from '../lib/i18n';
import { 
  Zap, 
  AlignLeft, 
  MessageSquare, 
  ShieldAlert,
  ArrowRight,
  CheckCircle2,
  Copy,
  RotateCcw,
  Trophy,
  BarChart3,
  FileText,
  Code2,
  Eye
} from 'lucide-react';
import { save } from '@tauri-apps/plugin-dialog';
import { writeTextFile } from '@tauri-apps/plugin-fs';

import { RadarScore } from './RadarScore';
import { Finding } from '../types/analysis';

/* ─── Pillar Icon Helper ─── */
const PillarIcon = ({ name }: { name: string }) => {
  const size = 18;
  const strokeWidth = 1.75;
  /* Match Greek names from engine */
  switch (name) {
    case 'AST_UNIFORMITY': return <AlignLeft size={size} strokeWidth={strokeWidth} />;
    case 'NAMING': return <Zap size={size} strokeWidth={strokeWidth} />;
    case 'STATISTICAL': return <BarChart3 size={size} strokeWidth={strokeWidth} />;
    case 'COMMENTS': return <MessageSquare size={size} strokeWidth={strokeWidth} />;
    case 'DRIFT': return <RotateCcw size={size} strokeWidth={strokeWidth} />;
    case 'INTEGRITY': return <FileText size={size} strokeWidth={strokeWidth} />;
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

/* ─── Animated Score Counter ─── */
const AnimatedScore = ({ target, color }: { target: number; color: string }) => {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    let frame: number;
    const duration = 1200;
    const start = performance.now();

    const animate = (now: number) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      /* ease-out-expo */
      const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      setCurrent(Math.round(eased * target));

      if (progress < 1) {
        frame = requestAnimationFrame(animate);
      }
    };

    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [target]);

  return (
    <span 
      className="text-5xl md:text-6xl font-black tracking-tighter tabular-nums" 
      style={{ color }}
    >
      {current}
    </span>
  );
};



/* ─── Main Dashboard ─── */
export const Dashboard: React.FC<{ lang: Language }> = ({ lang }) => {
  const { analysisResult, setView, addToast, setTargetLine, auditResults } = useAppStore();
  const t = translations[lang];

  const formatPillarName = (key: string) => {
    if (t.pillarNames[key as keyof typeof t.pillarNames]) {
      return t.pillarNames[key as keyof typeof t.pillarNames];
    }
    // Fallback: Replace _ with space and Title Case
    return key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
  };

  const getScoreLabel = () => {
    const rawLabel = analysisResult?.interpretation || "";
    const localizedLabel = t.tiers[rawLabel as keyof typeof t.tiers] || rawLabel;
    
    // Add icon prefix back (Support both Greek and English backend outputs)
    if (rawLabel.includes('Τίμιος') || rawLabel.includes('Honest')) return `🏆 ${localizedLabel}`;
    if (rawLabel.includes('Επαγγελματίας') || rawLabel.includes('Professional')) return `⚠️ ${localizedLabel}`;
    if (rawLabel.includes('Ψιλικατζής') || rawLabel.includes('Petty')) return `🔴 ${localizedLabel}`;
    if (rawLabel.includes('Ερασιτέχνης') || rawLabel.includes('Amateur')) return `💀 ${localizedLabel}`;
    return localizedLabel;
  };

  /* Empty state Check moved up */
  if (!analysisResult) {
    return (
      <div className="flex flex-col items-center justify-center h-[calc(100vh-100px)] space-y-6 anim-fade-in">
        <div className="p-6 bg-surface-elevated rounded-3xl border border-border-subtle">
          <ShieldAlert size={48} className="text-text-disabled" strokeWidth={1.75} />
        </div>
        <h2 className="text-2xl font-bold text-text-secondary">{t.noAnalysisFound}</h2>
        <button 
          onClick={() => setView('analyzer')}
          className="flex items-center space-x-3 px-8 py-3.5 bg-surface-elevated border border-border-default rounded-xl hover:bg-surface-hover transition-all duration-300 group"
        >
          <span className="font-semibold text-accent-primary text-sm">{t.goToAnalyzer}</span>
          <ArrowRight size={18} className="text-accent-primary group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    );
  }

  const handleCopyJSON = () => {
    if (analysisResult) {
      navigator.clipboard.writeText(JSON.stringify(analysisResult, null, 2));
      addToast(t.jsonCopied, 'success');
    }
  };

  const handleExportCaseFile = async () => {
    if (!analysisResult) return;

    try {
      const now = new Date();
      const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, 19);
      const filename = `CASE-FILE-${timestamp}-PAPATZIS.md`;

      const path = await save({
        filters: [{ name: 'Markdown', extensions: ['md'] }],
        defaultPath: filename
      });

      if (!path) return;

      const score = Math.round(analysisResult.final_score);
      const sessionId = Math.random().toString(36).substring(2, 10).toUpperCase();

      // Report Header
      let report = `# 📂 CASE FILE: PAPATZIS SPOTTER VERDICT\n`;
      report += `\`SESSION_ID: ${sessionId}\` | \`CORE_VERSION: 1.5.0-embedded\` | \`TIMESTAMP: ${now.toLocaleString()}\`\n\n`;
      
      report += `## ⚖️ ${t.results}: ${getScoreLabel()}\n`;
      report += `> **${t.papatzisScore.toUpperCase()}:** ${score} / 100\n`;
      report += `> **${t.confidence.toUpperCase()}:** ${Math.round(analysisResult.confidence_score * 100)}%\n\n`;
      
      let summary = '';
      if (analysisResult.final_score >= 60) summary = t.criticalSlopSummary;
      else if (analysisResult.final_score >= 30) summary = t.suspiciousPatternsSummary;
      else summary = t.humanIntegritySummary;

      report += `${summary}\n\n`;
      report += `--- \n\n`;
      report += `## 📊 ${t.pillarAudit}\n\n`;
      report += `| ${t.pillarLabel} | ${t.scoreLabel} |\n`;
      report += `| :--- | :--- |\n`;
      analysisResult.pillars.forEach(p => {
        report += `| ${formatPillarName(p.pillar)} | ${Math.round(p.score)}% |\n`;
      });
      report += `\n\n`;

      report += `## 📝 ${t.evidenceLog}\n\n`;
      
      const allFindings = analysisResult.pillars.flatMap(p => p.findings);
      if (allFindings.length > 0) {
        analysisResult.pillars.forEach(p => {
          if (p.findings.length > 0) {
            report += `### 🏗️ ${formatPillarName(p.pillar)}\n`;
            p.findings.forEach((f, i) => {
              report += `#### Finding #${i+1}: ${f.message}\n`;
              report += `- **Location:** Line ${f.line}\n`;
              report += `- **Rationale:** ${f.rationale}\n`;
              report += `- **Human Fix:** ${f.human_alternative}\n\n`;
            });
            report += `\n`;
          }
        });
      }
      if (allFindings.length === 0) {
        report += `*${t.noEvidenceFound}*\n\n`;
      }

      report += `\n---\n`;
      report += `*${t.verifiedBy} 🦀🐍*\n`;

      await writeTextFile(path, report);
      addToast(t.exportSuccess, 'success');
    } catch (error) {
      console.error('Export failed:', error);
      const errorMsg = error instanceof Error ? error.message : String(error);
      addToast(`${t.exportFailed}: ${errorMsg}`, 'error');
    }
  };

  const pillarsWithFindings = analysisResult.pillars.filter(p => p.findings.length > 0);
  const [activePillar, setActivePillar] = useState<string | null>(
    pillarsWithFindings.length > 0 ? pillarsWithFindings[0].pillar : null
  );


  const getScoreColor = (score: number) => {
    if (score < 20) return 'var(--human)';
    if (score < 60) return 'var(--accent-primary)';
    return 'var(--slop)';
  };



  const totalFindings = analysisResult.pillars.reduce((acc, p) => acc + p.findings.length, 0);
  const resultsArray = Array.isArray(auditResults) ? auditResults : [];

  return (
    <div className="p-4 md:p-6 max-w-[1400px] mx-auto w-full space-y-8 pb-16">

      {/* ═══ Hero Score Section ═══ */}
      <section className="flex flex-col items-center text-center space-y-5 py-6 md:py-8 bg-surface rounded-[2rem] border border-border-subtle shadow-strong relative anim-scale-in">
        <div className="absolute inset-0 bg-noise" />
        
          {/* Export Actions (Right) */}
          <div className="absolute top-5 right-6 flex items-center space-x-2 z-20">
            <button 
              onClick={handleExportCaseFile}
              className="flex items-center space-x-2 px-3 py-1.5 bg-surface-elevated border border-border-default rounded-xl hover:bg-surface-hover transition-all duration-200 text-text-secondary hover:text-text-primary group"
              title={t.exportCaseFile}
            >
              <FileText size={14} strokeWidth={1.75} className="group-hover:scale-110 transition-transform" />
              <span className="text-[10px] font-bold uppercase tracking-widest hidden md:inline">Case File</span>
            </button>

            <button 
              onClick={handleCopyJSON}
              className="p-2.5 bg-surface-elevated border border-border-default rounded-xl hover:bg-surface-hover transition-all duration-200 text-text-secondary hover:text-text-primary group"
              title={t.copyJson}
            >
              <Copy size={14} strokeWidth={1.75} className="group-hover:scale-110 transition-transform" />
            </button>
          </div>

          {/* Back Action (Left) */}
          <div className="absolute top-5 left-6 z-20">
            {resultsArray.length > 0 && (
              <button 
                onClick={() => setView('audit')}
                className="flex items-center space-x-2 px-3 py-1.5 bg-accent-primary text-white rounded-xl hover:scale-[1.03] transition-all duration-200 group"
                title="Back to Audit Results"
              >
                <ArrowRight size={14} strokeWidth={1.75} className="rotate-180" />
                <span className="text-[10px] font-bold uppercase tracking-widest hidden md:inline">{t.backToAudit}</span>
              </button>
            )}
          </div>

        {/* Score & Radar Section */}
        <div className="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-12 w-full max-w-5xl px-8 z-10">
          
          {/* Main Score Display */}
          <div className="flex flex-col items-center justify-center space-y-0 shrink-0">
            <AnimatedScore target={Math.round(analysisResult.final_score)} color={getScoreColor(analysisResult.final_score)} />
            <p className="text-[9px] text-text-secondary uppercase tracking-[0.4em] font-bold opacity-60">{t.papatzisScore}</p>
          </div>

          {/* Radar Visualization — Framed in Glass */}
          <div className="w-full max-w-[160px] h-[160px] md:max-w-[220px] md:h-[220px] xl:max-w-[260px] xl:h-[260px] relative anim-scale-in anim-delay-100 p-6 bg-glass-bg border border-border-subtle rounded-full shadow-inner-glow">
            <RadarScore pillars={analysisResult.pillars} lang={lang} />
          </div>

          {/* Vertical Pillars Legend (Right Side) */}
          <div className="hidden md:flex flex-col items-start gap-3.5 py-1 border-l border-border-default pl-10 min-w-[240px]">
             {analysisResult.pillars.map((p, idx) => (
                <div 
                   key={p.pillar} 
                   className="flex items-center space-x-4 group anim-fade-in-right"
                   style={{ animationDelay: `${200 + idx * 100}ms` }}
                >
                   <div 
                     className="p-2 rounded-xl transition-all duration-300"
                     style={{ 
                       backgroundColor: `${getPillarColorVar(p.pillar)}15`, 
                       color: getPillarColorVar(p.pillar) 
                     }}
                   >
                      <PillarIcon name={p.pillar} />
                   </div>
                   <div className="text-left">
                      <p className="text-[11px] uppercase font-bold tracking-wider leading-none mb-2 text-text-primary opacity-90">
                         {formatPillarName(p.pillar)}
                      </p>
                      <div className="flex items-center space-x-3">
                         <div className="w-24 h-1 bg-surface-hover rounded-full overflow-hidden">
                            <div 
                               className="h-full rounded-full transition-all duration-1000"
                               style={{ 
                                  width: `${p.score}%`,
                                  backgroundColor: getPillarColorVar(p.pillar)
                               }} 
                            />
                         </div>
                         <span className="text-xs font-mono font-bold text-text-primary">{Math.round(p.score)}</span>
                      </div>
                   </div>
                </div>
             ))}
          </div>
        </div>
        
        {/* Interpretation */}
        <div className="space-y-2.5 z-10 px-6 anim-slide-up anim-delay-200">
          <div className="inline-block px-4 py-1 bg-surface-elevated rounded-full border border-border-default backdrop-blur-sm">
            <span className="text-base md:text-lg font-bold text-text-primary">{getScoreLabel()}</span>
          </div>
          <div className="flex items-center justify-center space-x-4 pt-0.5">
            <span className="text-[9px] text-text-disabled font-mono uppercase tracking-wider">{totalFindings} {t.findings}</span>
            <span className="text-text-disabled opacity-30">·</span>
            <span className="text-[9px] text-text-disabled font-mono uppercase tracking-wider">Confidence: {Math.round(analysisResult.confidence_score * 100)}%</span>
            <span className="text-text-disabled opacity-30">·</span>
            <span className="text-[9px] text-text-disabled font-mono uppercase tracking-wider">{analysisResult.pillars.length} {t.pillars}</span>
          </div>
        </div>
      </section>


      {/* ═══ Findings Detail ═══ */}
      <section className="space-y-5 anim-slide-up anim-delay-300">
        
        {/* Header Section */}
        <div className="space-y-5 border-b border-border-subtle pb-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <h2 className="text-3xl font-black tracking-tight text-text-primary">{t.findingsAnalysis}</h2>
              {totalFindings > 0 && (
                <div className="bg-slop/[0.12] text-slop px-3 py-1 rounded-full border border-slop/[0.2]">
                  <span className="text-[10px] font-black uppercase tracking-widest">{totalFindings} issues</span>
                </div>
              )}
            </div>
            <p className="text-xs text-text-disabled font-medium opacity-50 max-w-sm md:text-right">
              {t.caseFileDesc}
            </p>
          </div>

          {/* Pillar Tabs (Responsive wrapping) */}
          <div className="flex flex-wrap items-center gap-2.5">
             {pillarsWithFindings.map((p) => (
                <button
                   key={p.pillar}
                   onClick={() => setActivePillar(p.pillar)}
                   className={`
                      group flex items-center space-x-3 px-4 py-2.5 rounded-2xl transition-all duration-300 border
                      ${activePillar === p.pillar 
                         ? 'bg-accent-primary text-white font-bold border-accent-primary shadow-lg shadow-accent-primary/20 scale-[1.02]' 
                         : 'bg-surface-elevated text-text-secondary border-border-default hover:bg-surface-hover hover:border-border-hover'
                      }
                   `}
                >
                   <div 
                     className={`transition-transform duration-300 group-hover:scale-110 ${activePillar === p.pillar ? 'text-white' : ''}`}
                     style={{ color: activePillar === p.pillar ? undefined : getPillarColorVar(p.pillar) }}
                   >
                      <PillarIcon name={p.pillar} />
                   </div>
                   <span className="text-[11px] uppercase tracking-[0.15em] font-black">
                      {formatPillarName(p.pillar)}
                   </span>
                   <div className={`
                      text-[10px] font-mono font-black px-2 py-0.5 rounded-lg border
                      ${activePillar === p.pillar 
                        ? 'bg-white/20 border-white/10 text-white' 
                        : 'bg-surface border-border-subtle text-text-disabled'
                      }
                   `}>
                      {p.findings.length}
                   </div>
                </button>
             ))}
          </div>
        </div>

        <div className="min-h-[250px]">
          {pillarsWithFindings.length > 0 ? (
            analysisResult.pillars.map(p => (p.pillar === activePillar && p.findings.length > 0) && (
              <div key={p.pillar} className="space-y-3 anim-fade-in">
                <div className="grid grid-cols-1 gap-3">
                  {p.findings.map((f: Finding, i: number) => (
                    <div 
                      key={i} 
                      className="bg-surface p-6 rounded-[2rem] flex flex-col space-y-3.5 border border-border-subtle hover:border-border-default hover:bg-surface-hover transition-all duration-500 group relative overflow-hidden anim-stagger"
                      style={{ animationDelay: `${i * 80}ms` }}
                    >
                      <div className="absolute top-0 right-0 w-32 h-32 opacity-[0.03] -mr-8 -mt-8 rotate-12 transition-transform duration-700 group-hover:rotate-0" style={{ color: getPillarColorVar(p.pillar) }}>
                         <PillarIcon name={p.pillar} />
                      </div>
                      
                      <div className="flex items-start justify-between gap-6 relative z-10">
                        <div className="space-y-1">
                          <h4 className="text-lg font-semibold leading-snug group-hover:translate-x-0.5 transition-transform duration-300 text-text-primary">{f.message}</h4>
                          <p className="text-sm text-text-secondary leading-relaxed opacity-80">{f.rationale}</p>
                        </div>
                        <div className="flex flex-col items-end justify-between gap-4 shrink-0">
                          <span className="text-[10px] bg-surface-elevated px-3 py-1 rounded-lg font-mono text-text-disabled border border-border-default tracking-tighter">
                            LINE {f.line}
                          </span>
                          <button 
                            onClick={() => {
                              setTargetLine(f.line);
                              setView('analyzer');
                            }}
                            className="p-2.5 bg-accent-primary/[0.08] border border-accent-primary/[0.12] rounded-xl text-accent-primary hover:bg-accent-primary hover:text-white transition-all duration-300 group/btn"
                            title="Inspect in Editor"
                          >
                            <Eye size={16} strokeWidth={1.75} className="group-hover/btn:scale-110 transition-transform" />
                          </button>
                        </div>
                      </div>
                      {/* Πρόταση βελτίωσης */}
                      <div className="bg-human/[0.03] rounded-xl p-3 border border-human/[0.06] flex items-start space-x-2.5">
                        <CheckCircle2 size={14} strokeWidth={1.75} className="text-human mt-0.5 shrink-0" />
                        <div className="space-y-0.5">
                          <p className="text-[9px] uppercase font-bold tracking-[0.15em] text-human/70">{t.humanSuggestion}</p>
                          <p className="text-[12px] text-text-primary font-medium leading-snug">{f.human_alternative}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <div className="bg-surface p-16 text-center space-y-6 rounded-3xl border border-human/[0.08] relative overflow-hidden">
              <div className="flex justify-center relative">
                <div className="p-5 bg-human/[0.08] rounded-full border border-human/[0.12]">
                  <Trophy size={44} className="text-human" strokeWidth={1.5} />
                </div>
              </div>
              <div className="space-y-2 relative">
                <h3 className="text-2xl font-bold text-text-primary">Pure Human Integrity</h3>
                <p className="text-text-secondary text-sm max-w-sm mx-auto">
                  {t.noIssuesText}
                </p>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* ═══ Footer Action ═══ */}
      <footer className="flex flex-col md:flex-row items-center justify-center gap-4 pt-4 pb-6">
        <button 
          onClick={() => setView('analyzer')}
          className="flex items-center space-x-3 px-8 py-3.5 bg-accent-primary text-white font-bold rounded-2xl hover:scale-[1.03] active:scale-95 transition-all duration-300 shadow-lg shadow-accent-primary/15 hover:shadow-accent-primary/30"
        >
          <Code2 size={18} strokeWidth={1.75} />
          <span className="uppercase tracking-[0.15em] text-[11px]">{t.viewInEditor}</span>
        </button>

        <button 
          onClick={handleExportCaseFile}
          className="flex items-center space-x-3 px-8 py-3.5 bg-surface-elevated border border-border-default text-text-secondary font-bold rounded-2xl hover:bg-surface-hover hover:border-border-hover transition-all duration-300"
        >
          <FileText size={18} strokeWidth={1.75} />
          <span className="uppercase tracking-[0.15em] text-[11px]">{t.exportCaseFile}</span>
        </button>
      </footer>
    </div>
  );
};
