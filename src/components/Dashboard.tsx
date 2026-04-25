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
      className="text-5xl md:text-6xl font-black tracking-tighter tabular-nums" 
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

  /* Empty state Check moved up */
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
      const sessionId = Math.random().toString(36).substring(2, 10).toUpperCase();

      // Report Header
      let report = `# 📂 CASE FILE: PAPATZIS SPOTTER VERDICT\n`;
      report += `\`SESSION_ID: ${sessionId}\` | \`CORE_VERSION: 1.4.1-embedded\` | \`TIMESTAMP: ${now.toLocaleString()}\`\n\n`;
      
      report += `## ⚖️ ${lang === 'EL' ? 'ΤΟ ΠΟΡΙΣΜΑ' : 'THE VERDICT'}: ${getScoreLabel()}\n`;
      report += `> **${lang === 'EL' ? 'ΣΥΝΟΛΙΚΟ SCORE' : 'FINAL SCORE'}:** ${score} / 100\n`;
      report += `> **${lang === 'EL' ? 'ΒΑΘΜΟΣ ΣΙΓΟΥΡΙΑΣ' : 'CONFIDENCE'}:** ${Math.round(analysisResult.confidence_score * 100)}%\n\n`;
      
      report += `### 🔎 ${lang === 'EL' ? 'ΣΥΝΟΠΤΙΚΗ ΑΞΙΟΛΟΓΗΣΗ' : 'FORENSIC SUMMARY'}\n`;
      if (score > 70) {
        report += lang === 'EL' 
          ? `🚨 **ΚΡΙΣΙΜΟ SLOP.** Ο κώδικας εμφανίζει ακραία δομική συμμετρία και στατιστική προβλεψιμότητα. Στερείται οργανικής πολυπλοκότητας και ανθρώπινης πρόθεσης. Η χρήση του ως έχει ενέχει ρίσκο "ψηφιακής παπάτζας".\n\n`
          : `🚨 **CRITICAL SLOP DETECTED.** The code exhibits extreme structural symmetry and statistical predictability. It lacks organic complexity and human intentionality. Use as-is is highly suspicious.\n\n`;
      } else if (score > 30) {
        report += lang === 'EL'
          ? `⚠️ **ΥΠΟΠΤΑ ΜΟΤΙΒΑ.** Εντοπίστηκαν μοτίβα που παραπέμπουν σε βαριά χρήση AI χωρίς επιμέλεια. Ο κώδικας μοιάζει "υπερβολικά καθαρός" για να είναι 100% χειροποίητος. Συνιστάται έλεγχος.\n\n`
          : `⚠️ **SUSPICIOUS PATTERNS.** Detected patterns characteristic of heavy AI assistance. The structure feels "too clean" to be purely organic. Verification of architectural intent is recommended.\n\n`;
      } else {
        report += lang === 'EL'
          ? `✅ **ΑΝΘΡΩΠΙΝΗ ΑΚΕΡΑΙΟΤΗΤΑ.** Δεν ανιχνεύθηκαν σημαντικά AI αποτυπώματα. Ο κώδικας φέρει τα οργανικά σημάδια της ανθρώπινης λογικής, με απρόβλεπτη αλλά στοχευμένη δομή.\n\n`
          : `✅ **HUMAN INTEGRITY VERIFIED.** No meaningful AI signatures detected. The code displays organic reasoning and intentional complexity consistent with human craftsmanship.\n\n`;
      }

      report += `---\n\n`;
      report += `## 📊 ${lang === 'EL' ? 'ΑΝΑΛΥΣΗ ΑΝΑ ΠΥΛΩΝΑ' : 'PILLAR-BY-PILLAR AUDIT'}\n\n`;
      
      const pillarDescs: Record<string, { el: string, en: string }> = {
        'Ρομποτική Ομοιομορφία': {
          el: 'Έλεγχος δομικής συμμετρίας και "τέλειων" αποστάσεων που σπάνια διατηρεί άνθρωπος.',
          en: 'Structural symmetry and textbook-perfect spacing that humans rarely maintain.'
        },
        'Βαφτιστικό Slop': {
          el: 'Εντοπισμός γενόσημων ονομάτων (data, list, item) που χρησιμοποιούν τα LLMs.',
          en: 'Generic naming patterns often used by AI to fill architectural gaps.'
        },
        'Στατιστική Φλυαρία': {
          el: 'Μέτρηση περιττών σχολίων και πλεονασματικού κώδικα (boilerplate).',
          en: 'Excessive verbosity and redundant comments that explain the obvious.'
        },
        'GPT-Style Παπατζιλίκι': {
          el: 'Ανίχνευση συγκεκριμένων εκφράσεων και "ευγενικών" δομών τυπικών για AI.',
          en: 'Specific catchphrases and "polite" structural markers common in AI outputs.'
        },
        'Ύποπτο Drift Κώδικα': {
          el: 'Απότομες αλλαγές στο στυλ γραφής μέσα στο ίδιο αρχείο.',
          en: 'Sudden shifts in coding style or mental model within the same file.'
        }
      };

      analysisResult.pillars.forEach(p => {
        const info = pillarDescs[p.pillar] || { el: 'Ανάλυση στατικών μοτίβων.', en: 'Static pattern analysis.' };
        const desc = lang === 'EL' ? info.el : info.en;
        report += `#### 🔹 ${t.pillarNames[p.pillar as keyof typeof t.pillarNames] || p.pillar}\n`;
        report += `- **Score:** ${Math.round(p.score)}/100\n`;
        report += `- **Findings:** ${p.findings.length}\n`;
        report += `- **Focus:** ${desc}\n\n`;
      });

      report += `---\n\n`;
      report += `## 📝 ${lang === 'EL' ? 'ΑΡΧΕΙΟ ΑΠΟΔΕΙΞΕΩΝ (FINDINGS)' : 'EVIDENCE LOG (FINDINGS)'}\n\n`;
      
      if (analysisResult.pillars.some(p => p.findings.length > 0)) {
        analysisResult.pillars.forEach(p => {
          if (p.findings.length > 0) {
            report += `### 🏗️ ${t.pillarNames[p.pillar as keyof typeof t.pillarNames] || p.pillar}\n`;
            p.findings.forEach((f, i) => {
              report += `#### Finding #${i+1}: ${f.message}\n`;
              report += `- **Location:** Line ${f.line}\n`;
              report += `- **Rationale:** ${f.rationale}\n`;
              report += `- **Human Fix:** ${f.human_alternative}\n\n`;
            });
            report += `\n`;
          }
        });
      } else {
        report += `*${lang === 'EL' ? 'Δεν βρέθηκαν επιβαρυντικά στοιχεία. Το υποκείμενο είναι καθαρό.' : 'No incriminating evidence found. Subject is clean.'}*\n\n`;
      }

      report += `---\n`;
      report += `*${lang === 'EL' ? 'Πιστοποιήθηκε από το Papatzis Spotter. Φτιαγμένο για ανθρώπους, από ανθρώπους.' : 'Verified by Papatzis Spotter. Built for humans, by humans.'} 🦀🐍*\n`;

      await writeTextFile(path, report);
      addToast(lang === 'EL' ? 'Ο φάκελος εξήχθη επιτυχώς!' : 'Case file exported successfully!', 'success');
    } catch (error) {
      console.error('Export failed:', error);
      const errorMsg = error instanceof Error ? error.message : String(error);
      addToast(lang === 'EL' ? `Η εξαγωγή απέτυχε: ${errorMsg}` : `Export failed: ${errorMsg}`, 'error');
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
      <section className="flex flex-col items-center text-center space-y-6 py-8 md:py-10 bg-surface rounded-[2rem] border border-white/[0.04] shadow-strong relative anim-scale-in">
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
        <div className="flex flex-col md:flex-row items-center justify-center gap-10 md:gap-16 w-full max-w-5xl px-8 z-10">
          
          {/* Main Score Display */}
          <div className="flex flex-col items-center justify-center space-y-0.5 shrink-0">
            <AnimatedScore target={Math.round(analysisResult.final_score)} color={getScoreColor(analysisResult.final_score)} />
            <p className="text-[9px] text-white uppercase tracking-[0.4em] font-black opacity-60">PapatzisScore</p>
          </div>

          {/* Radar Visualization */}
          <div className="w-full max-w-[180px] h-[180px] md:max-w-[240px] md:h-[240px] xl:max-w-[280px] xl:h-[280px] relative anim-scale-in anim-delay-100">
            <RadarScore pillars={analysisResult.pillars} lang={lang} />
          </div>

          {/* Vertical Pillars Legend (Right Side) */}
          <div className="hidden md:flex flex-col items-start gap-4 py-2 border-l border-white/10 pl-10 min-w-[240px]">
             {analysisResult.pillars.map((p, idx) => (
                <div 
                   key={p.pillar} 
                   className="flex items-center space-x-4 group anim-fade-in-right"
                   style={{ animationDelay: `${200 + idx * 100}ms` }}
                >
                   <div className={`p-2 rounded-xl transition-all duration-300
                      ${p.score > 10 ? 'bg-slop/[0.08] text-slop' : p.score > 0 ? 'bg-warning/[0.08] text-warning' : 'bg-human/[0.08] text-human'}
                   `}>
                      <PillarIcon name={p.pillar} />
                   </div>
                   <div className="text-left">
                      <p className="text-[10px] uppercase tracking-[0.15em] text-white/50 font-black leading-none mb-1.5">
                         {t.pillarNames[p.pillar as keyof typeof t.pillarNames] || p.pillar}
                      </p>
                      <div className="flex items-center space-x-3">
                         <div className="w-24 h-1 bg-white/[0.06] rounded-full overflow-hidden">
                            <div 
                               className="h-full rounded-full transition-all duration-1000"
                               style={{ 
                                  width: `${p.score}%`,
                                  backgroundColor: p.score > 10 ? 'var(--slop)' : (p.score > 0 ? 'var(--warning)' : 'var(--human)')
                               }} 
                            />
                         </div>
                         <span className="text-xs font-mono font-bold text-white/90">{Math.round(p.score)}</span>
                      </div>
                   </div>
                </div>
             ))}
          </div>
        </div>
        
        {/* Interpretation */}
        <div className="space-y-3 z-10 px-6 anim-slide-up anim-delay-200">
          <div className="inline-block px-4 py-1.5 bg-white/[0.03] rounded-full border border-white/[0.06] backdrop-blur-sm">
            <span className="text-base md:text-lg font-bold text-white">{getScoreLabel()}</span>
          </div>
          <div className="flex items-center justify-center space-x-4 pt-1">
            <span className="text-[9px] text-text-disabled font-mono uppercase tracking-wider">{totalFindings} {t.findings}</span>
            <span className="text-text-disabled opacity-30">·</span>
            <span className="text-[9px] text-text-disabled font-mono uppercase tracking-wider">Confidence: {Math.round(analysisResult.confidence_score * 100)}%</span>
            <span className="text-text-disabled opacity-30">·</span>
            <span className="text-[9px] text-text-disabled font-mono uppercase tracking-wider">{analysisResult.pillars.length} {t.pillars}</span>
          </div>
        </div>
      </section>


      {/* ═══ Findings Detail ═══ */}
      <section className="space-y-6 anim-slide-up anim-delay-300">
        
        {/* Header Section */}
        <div className="space-y-6 border-b border-white/[0.04] pb-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <h2 className="text-3xl font-black tracking-tight text-white">{t.findingsAnalysis}</h2>
              {totalFindings > 0 && (
                <div className="bg-slop/[0.12] text-slop px-3 py-1 rounded-full border border-slop/[0.2]">
                  <span className="text-[10px] font-black uppercase tracking-widest">{totalFindings} issues</span>
                </div>
              )}
            </div>
            <p className="text-xs text-text-disabled font-medium opacity-50 max-w-sm md:text-right">
              Αναλυτικό αρχείο καταγραφής AI μοτίβων και προτάσεις βελτίωσης από τη μηχανή του Papatzis Spotter.
            </p>
          </div>

          {/* Pillar Tabs (Responsive wrapping) */}
          <div className="flex flex-wrap items-center gap-3">
             {pillarsWithFindings.map((p) => (
                <button
                   key={p.pillar}
                   onClick={() => setActivePillar(p.pillar)}
                   className={`
                      group flex items-center space-x-3 px-5 py-3 rounded-2xl transition-all duration-300 border
                      ${activePillar === p.pillar 
                         ? 'bg-accent-primary text-bg font-bold border-accent-primary shadow-lg shadow-accent-primary/20 scale-[1.02]' 
                         : 'bg-white/[0.03] text-text-secondary border-white/[0.04] hover:bg-white/[0.07] hover:border-white/[0.1]'
                      }
                   `}
                >
                   <div className={`transition-transform duration-300 group-hover:scale-110 ${activePillar === p.pillar ? 'text-bg' : 'text-accent-primary/80'}`}>
                      <PillarIcon name={p.pillar} />
                   </div>
                   <span className="text-[11px] uppercase tracking-[0.15em] font-black">
                      {t.pillarNames[p.pillar as keyof typeof t.pillarNames] || p.pillar}
                   </span>
                   <div className={`
                      text-[10px] font-mono font-black px-2 py-0.5 rounded-lg border
                      ${activePillar === p.pillar 
                        ? 'bg-bg/20 border-bg/10 text-bg' 
                        : 'bg-white/5 border-white/5 text-text-disabled'
                      }
                   `}>
                      {p.findings.length}
                   </div>
                </button>
             ))}
          </div>
        </div>

        <div className="min-h-[300px]">
          {pillarsWithFindings.length > 0 ? (
            analysisResult.pillars.map(p => (p.pillar === activePillar && p.findings.length > 0) && (
              <div key={p.pillar} className="space-y-5 anim-fade-in">
                <div className="grid grid-cols-1 gap-4">
                  {p.findings.map((f: Finding, i: number) => (
                    <div 
                      key={i} 
                      className="bg-surface p-7 rounded-[2rem] flex flex-col space-y-4 border border-white/[0.04] hover:border-white/[0.08] hover:bg-white/[0.01] transition-all duration-500 group relative overflow-hidden"
                    >
                      
                      <div className="flex items-start justify-between gap-6 relative z-10">
                        <div className="space-y-1">
                          <h4 className="text-base font-bold text-slop leading-snug group-hover:translate-x-0.5 transition-transform duration-300">{f.message}</h4>
                          <p className="text-sm text-text-secondary leading-relaxed opacity-80">{f.rationale}</p>
                        </div>
                        <span className="text-[10px] bg-white/[0.05] px-3 py-1 rounded-lg font-mono text-text-disabled border border-white/[0.06] shrink-0 tracking-tighter">
                          LINE {f.line}
                        </span>
                      </div>
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
