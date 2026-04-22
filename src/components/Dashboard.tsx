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
  FileText
} from 'lucide-react';
import { save } from '@tauri-apps/plugin-dialog';
import { writeTextFile } from '@tauri-apps/plugin-fs';

import { RadarScore } from './RadarScore';
import { Finding } from '../types/analysis';

/* ─── Pillar Icon Helper ─── */
const PillarIcon = ({ name }: { name: string }) => {
  /* Match Greek names from engine */
  switch (name) {
    case 'Βαφτιστικό Slop': return <Zap size={18} />;
    case 'Ρομποτική Ομοιομορφία': return <AlignLeft size={18} />;
    case 'Στατιστική Φλυαρία': return <BarChart3 size={18} />;
    case 'GPT-Style Παπατζιλίκι': return <MessageSquare size={18} />;
    case 'Ύποπτο Drift Κώδικα': return <RotateCcw size={18} />;
    default: return <Zap size={18} />;
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
      className="text-7xl md:text-8xl font-black tracking-tighter tabular-nums" 
      style={{ color }}
    >
      {current}
    </span>
  );
};



/* ─── Main Dashboard ─── */
export const Dashboard: React.FC<{ lang?: Language }> = ({ lang = 'EL' }) => {
  const { analysisResult, setView, addToast } = useAppStore();
  const t = translations[lang];

  const handleCopyJSON = () => {
    if (analysisResult) {
      navigator.clipboard.writeText(JSON.stringify(analysisResult, null, 2));
      addToast(lang === 'EL' ? 'Το JSON αντιγράφηκε στο πρόχειρο!' : 'JSON copied to clipboard!', 'success');
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
      const verdict = analysisResult.interpretation;
      
      let report = `# 📁 CASE FILE: PAPATZIS SPOTTER VERDICT\n`;
      report += `**STATUS:** [CONFIDENTIAL]\n`;
      report += `**DATE:** ${now.toLocaleString()}\n`;
      report += `**SUBJECT:** AI Slop Forensic Analysis\n\n`;
      report += `---\n\n`;
      report += `## ⚖️ THE VERDICT: ${verdict}\n`;
      report += `**FINAL SCORE:** ${score} / 100\n`;
      report += `**CONFIDENCE:** ${Math.round(analysisResult.confidence_score * 100)}%\n\n`;
      
      report += `### 🔎 EXECUTIVE SUMMARY\n`;
      if (score > 70) {
        report += `The code exhibits high statistical uniformity and structural symmetry. It is a hollow shell, likely prompt-engineered with zero human intentionality. Human edge: Lost.\n\n`;
      } else if (score > 30) {
        report += `Suspicious patterns detected. The logic feels "too clean," suggesting heavy AI assistance or uncurated boilerplate copying. Proceed with caution.\n\n`;
      } else {
        report += `No significant AI signatures found. The code bears the organic marks of human reasoning and intentionality. Integrity: High.\n\n`;
      }

      report += `---\n\n`;
      report += `## 📊 PILLAR BREAKDOWN\n\n`;
      analysisResult.pillars.forEach(p => {
        report += `- **${p.pillar}:** ${Math.round(p.score)}/100 (${p.findings.length} findings)\n`;
      });
      report += `\n---\n\n`;

      report += `## 📝 EVIDENCE LOG (FINDINGS)\n\n`;
      if (analysisResult.pillars.some(p => p.findings.length > 0)) {
        analysisResult.pillars.forEach(p => {
          if (p.findings.length > 0) {
            report += `### 🏗️ ${p.pillar}\n`;
            p.findings.forEach((f, i) => {
              report += `#### Finding #${i+1}: ${f.message}\n`;
              report += `- **Location:** Line ${f.line}\n`;
              report += `- **Rationale:** ${f.rationale}\n`;
              report += `- **Human Fix:** ${f.human_alternative}\n\n`;
            });
          }
        });
      } else {
        report += `*No incriminating evidence found. Subject is clean.*\n\n`;
      }

      report += `---\n`;
      report += `*Verified by Papatzis Spotter. Built for humans, by humans. 🦀🐍*\n`;

      await writeTextFile(path, report);
      addToast(lang === 'EL' ? 'Ο φάκελος εξήχθη επιτυχώς!' : 'Case file exported successfully!', 'success');
    } catch (error) {
      console.error('Export failed:', error);
      addToast(lang === 'EL' ? 'Η εξαγωγή απέτυχε' : 'Export failed', 'error');
    }
  };

  /* Empty state */
  if (!analysisResult) {
    return (
      <div className="flex flex-col items-center justify-center h-[calc(100vh-100px)] space-y-6 anim-fade-in">
        <div className="p-6 bg-surface-elevated rounded-3xl border border-white/[0.04]">
          <ShieldAlert size={48} className="text-text-disabled" strokeWidth={1.5} />
        </div>
        <h2 className="text-2xl font-bold text-text-secondary">{lang === 'EL' ? 'Δεν βρέθηκε ανάλυση' : 'No analysis found'}</h2>
        <button 
          onClick={() => setView('analyzer')}
          className="flex items-center space-x-3 px-8 py-3.5 bg-surface-elevated border border-white/[0.06] rounded-xl hover:bg-white/[0.04] transition-all duration-300 group"
        >
          <span className="font-semibold text-accent-primary text-sm">{lang === 'EL' ? 'Μετάβαση στον Analyzer' : 'Go to Analyzer'}</span>
          <ArrowRight size={18} className="text-accent-primary group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    );
  }

  const getScoreColor = (score: number) => {
    if (score < 20) return 'var(--human)';
    if (score < 60) return 'var(--accent-primary)';
    return 'var(--slop)';
  };

  const getScoreLabel = () => {
    const rawLabel = analysisResult.interpretation;
    const localizedLabel = t.tiers[rawLabel as keyof typeof t.tiers] || rawLabel;
    
    // Add icon prefix back
    if (rawLabel.includes('Τίμιος')) return `🏆 ${localizedLabel}`;
    if (rawLabel.includes('Επαγγελματίας')) return `⚠️ ${localizedLabel}`;
    if (rawLabel.includes('Ψιλικατζής')) return `🔴 ${localizedLabel}`;
    if (rawLabel.includes('Ερασιτέχνης')) return `💀 ${localizedLabel}`;
    return localizedLabel;
  };

  const totalFindings = analysisResult.pillars.reduce((acc, p) => acc + p.findings.length, 0);

  return (
    <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-10 pb-20">

      {/* ═══ Hero Score Section ═══ */}
      <section className="flex flex-col items-center text-center space-y-8 py-12 md:py-16 bg-surface rounded-[2rem] border border-white/[0.04] shadow-strong relative anim-scale-in">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-b from-accent-primary/[0.03] via-transparent to-transparent" />
        <div className="absolute inset-0 bg-noise" />
        
        {/* Export Actions */}
        <div className="absolute top-5 right-6 flex items-center space-x-2 z-20">
          <button 
            onClick={handleExportCaseFile}
            className="flex items-center space-x-2 px-3 py-1.5 bg-white/[0.03] border border-white/[0.04] rounded-xl hover:bg-white/[0.06] transition-all duration-200 text-text-secondary hover:text-white group"
            title={t.exportCaseFile}
          >
            <FileText size={14} className="group-hover:scale-110 transition-transform" />
            <span className="text-[10px] font-bold uppercase tracking-widest hidden md:inline">Case File</span>
          </button>

          <button 
            onClick={handleCopyJSON}
            className="p-2.5 bg-white/[0.03] border border-white/[0.04] rounded-xl hover:bg-white/[0.06] transition-all duration-200 text-text-secondary hover:text-white group"
            title={t.copyJson}
          >
            <Copy size={14} className="group-hover:scale-110 transition-transform" />
          </button>
        </div>

        {/* Score & Radar Section */}
        <div className="flex flex-col md:flex-row items-center justify-center gap-12 w-full max-w-4xl px-8 z-10">
          
          {/* Main Score Display */}
          <div className="flex flex-col items-center justify-center space-y-1">
            <AnimatedScore target={Math.round(analysisResult.final_score)} color={getScoreColor(analysisResult.final_score)} />
            <p className="text-[10px] text-white uppercase tracking-[0.4em] font-black opacity-60">PapatzisScore</p>
          </div>

          {/* Radar Visualization */}
          <div className="w-full max-w-[320px] h-[320px] md:max-w-[450px] md:h-[450px] xl:max-w-[500px] xl:h-[500px] relative anim-scale-in anim-delay-100">
            <RadarScore pillars={analysisResult.pillars} lang={lang} />
          </div>
        </div>
        
        {/* Interpretation */}
        <div className="space-y-3 z-10 px-6 anim-slide-up anim-delay-200">
          <div className="inline-block px-4 py-1.5 bg-white/[0.03] rounded-full border border-white/[0.06] backdrop-blur-sm">
            <span className="text-base md:text-lg font-bold text-white">{getScoreLabel()}</span>
          </div>
          <div className="flex items-center justify-center space-x-4 pt-2">
            <span className="text-[10px] text-text-disabled font-mono">{totalFindings} {t.findings}</span>
            <span className="text-text-disabled">·</span>
            <span className="text-[10px] text-text-disabled font-mono">Confidence: {Math.round(analysisResult.confidence_score * 100)}%</span>
            <span className="text-text-disabled">·</span>
            <span className="text-[10px] text-text-disabled font-mono">{analysisResult.pillars.length} {t.pillars}</span>
          </div>
        </div>
      </section>

      {/* ═══ Pillar Cards ═══ */}
      <section className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {analysisResult.pillars.map((p, idx) => (
          <div 
            key={p.pillar} 
            className={`bg-surface border border-white/[0.04] p-5 rounded-2xl flex flex-col items-center space-y-3 transition-all duration-300 hover:border-white/[0.08] hover:shadow-soft hover:bg-surface-elevated group cursor-default anim-slide-up`}
            style={{ animationDelay: `${idx * 80}ms` }}
          >
            <div className={`p-2.5 rounded-xl transition-all duration-300
              ${p.score > 10 ? 'bg-slop/[0.08] text-slop' : p.score > 0 ? 'bg-warning/[0.08] text-warning' : 'bg-human/[0.08] text-human'}
              group-hover:scale-110
            `}>
              <PillarIcon name={p.pillar} />
            </div>
            <div className="text-center space-y-1">
              <h3 className="text-[9px] uppercase tracking-[0.2em] text-white font-black opacity-60">
                {t.pillarNames[p.pillar as keyof typeof t.pillarNames] || p.pillar}
              </h3>
              <p className="text-2xl font-mono font-bold leading-none tabular-nums text-white">{Math.round(p.score)}</p>
            </div>
            {/* Mini progress */}
            <div className="w-full h-1 bg-white/[0.04] rounded-full overflow-hidden">
              <div 
                className="h-full rounded-full transition-all duration-1000 ease-out"
                style={{ 
                  width: `${Math.min((p.score / 20) * 100, 100)}%`,
                  backgroundColor: p.score > 10 ? 'var(--slop)' : (p.score > 0 ? 'var(--warning)' : 'var(--human)')
                }}
              />
            </div>
          </div>
        ))}
      </section>

      {/* ═══ Findings Detail ═══ */}
      <section className="space-y-6 anim-slide-up anim-delay-300">
        <div className="flex items-center justify-between border-b border-white/[0.04] pb-5">
          <div className="flex items-center space-x-3">
            <h2 className="text-xl font-bold">{t.findingsAnalysis}</h2>
            {totalFindings > 0 && (
              <span className="text-[10px] bg-slop/[0.08] text-slop px-2.5 py-1 rounded-full uppercase font-bold tracking-[0.1em] border border-slop/[0.12]">
                {totalFindings} issues
              </span>
            )}
          </div>
        </div>

        <div className="space-y-8">
          {analysisResult.pillars.some(p => p.findings.length > 0) ? (
            analysisResult.pillars.map(p => p.findings.length > 0 && (
              <div key={p.pillar} className="space-y-3">
                <div className="flex items-center space-x-2 text-text-secondary opacity-70">
                  <PillarIcon name={p.pillar} />
                  <span className="text-[10px] uppercase font-bold tracking-[0.15em]">
                    {t.pillarNames[p.pillar as keyof typeof t.pillarNames] || p.pillar}
                  </span>
                  <span className="text-[10px] font-mono text-text-disabled">({p.findings.length})</span>
                </div>
                <div className="grid grid-cols-1 gap-3">
                  {p.findings.map((f: Finding, i: number) => (
                    <div 
                      key={i} 
                      className="bg-surface p-5 rounded-2xl flex flex-col space-y-3 border border-white/[0.04] hover:border-white/[0.06] transition-all duration-200 group"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <h4 className="text-sm font-bold text-slop leading-snug">{f.message}</h4>
                        <span className="text-[10px] bg-white/[0.03] px-2 py-0.5 rounded-md font-mono text-text-disabled border border-white/[0.04] shrink-0">
                          L{f.line}
                        </span>
                      </div>
                      <p className="text-[12px] text-text-secondary leading-relaxed">{f.rationale}</p>
                      
                      {/* Πρόταση βελτίωσης */}
                      <div className="bg-human/[0.03] rounded-xl p-3 border border-human/[0.06] flex items-start space-x-2.5">
                        <CheckCircle2 size={14} className="text-human mt-0.5 shrink-0" />
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
              <div className="absolute inset-0 bg-gradient-to-b from-human/[0.03] to-transparent" />
              <div className="flex justify-center relative">
                <div className="p-5 bg-human/[0.08] rounded-full border border-human/[0.12]">
                  <Trophy size={44} className="text-human" strokeWidth={1.5} />
                </div>
              </div>
              <div className="space-y-2 relative">
                <h3 className="text-2xl font-bold text-white">Pure Human Integrity</h3>
                <p className="text-text-secondary text-sm max-w-sm mx-auto">
                  {t.noIssuesText}
                </p>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* ═══ Footer Action ═══ */}
      <footer className="flex justify-center pt-6 pb-8">
        <button 
          onClick={() => setView('analyzer')}
          className="flex items-center space-x-3 px-8 py-4 bg-accent-primary text-bg font-bold rounded-2xl hover:scale-[1.03] active:scale-95 transition-all duration-300 shadow-lg shadow-accent-primary/15 hover:shadow-accent-primary/30"
        >
          <RotateCcw size={18} />
          <span className="uppercase tracking-[0.15em] text-[11px]">{t.analyzeNewCode}</span>
        </button>
      </footer>
    </div>
  );
};
