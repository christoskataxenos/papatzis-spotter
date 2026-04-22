import React from 'react';
import { HelpCircle, Info, BookOpen, Heart, Zap, AlignLeft, MessageSquare, Repeat, ShieldAlert } from 'lucide-react';
import { Language, translations } from '../lib/i18n';

export const Help: React.FC<{ lang?: Language }> = ({ lang = 'EL' }) => {
  const t = translations[lang];
  
  /* Pillar info data */
  const helpPillars = [
    { icon: Zap, ...t.helpPillars[0] },
    { icon: AlignLeft, ...t.helpPillars[1] },
    { icon: MessageSquare, ...t.helpPillars[2] },
    { icon: Repeat, ...t.helpPillars[3] },
    { icon: ShieldAlert, ...t.helpPillars[4] },
  ];

  return (
    <div className="p-4 md:p-8 max-w-5xl mx-auto space-y-10 pb-20">
      
      {/* ═══ Header ═══ */}
      <header className="flex flex-col items-center text-center space-y-5 anim-scale-in">
        <div className="p-4 bg-accent-primary/[0.08] rounded-2xl border border-accent-primary/[0.12]">
          <HelpCircle className="text-accent-primary" size={28} strokeWidth={1.8} />
        </div>
        <div className="space-y-1">
          <h1 className="text-2xl md:text-3xl font-bold text-white">{t.helpTitle}</h1>
          <p className="text-accent-primary uppercase tracking-[0.2em] text-[10px] font-black opacity-80">Knowledge Base</p>
        </div>
      </header>

      {/* ═══ Info Cards ═══ */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 anim-slide-up anim-delay-200">
        
        {/* Τι είναι το AI Slop */}
        <div className="bg-surface p-6 rounded-2xl border border-white/[0.04] space-y-4 hover:border-white/[0.06] transition-all duration-300">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-accent-primary/[0.08] rounded-lg">
              <Info size={18} className="text-accent-primary" />
            </div>
            <h3 className="text-lg font-bold text-white">{t.whatIsSlopTitle}</h3>
          </div>
          <p className="text-[12px] text-text-secondary leading-relaxed">
            {t.whatIsSlopDesc1}
          </p>
          <p className="text-[12px] text-text-secondary leading-relaxed">
            {t.whatIsSlopDesc2}
          </p>
        </div>

        {/* Πώς λειτουργεί */}
        <div className="bg-surface p-6 rounded-2xl border border-white/[0.04] space-y-4 hover:border-white/[0.06] transition-all duration-300">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-accent-primary/[0.08] rounded-lg">
              <BookOpen size={18} className="text-accent-primary" />
            </div>
            <h3 className="text-lg font-bold text-white">{t.howItWorksTitle}</h3>
          </div>
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <span className="text-[10px] font-mono font-bold text-accent-primary bg-accent-primary/[0.08] w-5 h-5 rounded-md flex items-center justify-center shrink-0 mt-0.5">1</span>
              <p className="text-[12px] text-text-secondary leading-relaxed">{t.step1}</p>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-[10px] font-mono font-bold text-accent-primary bg-accent-primary/[0.08] w-5 h-5 rounded-md flex items-center justify-center shrink-0 mt-0.5">2</span>
              <p className="text-[12px] text-text-secondary leading-relaxed">{t.step2}</p>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-[10px] font-mono font-bold text-accent-primary bg-accent-primary/[0.08] w-5 h-5 rounded-md flex items-center justify-center shrink-0 mt-0.5">3</span>
              <p className="text-[12px] text-text-secondary leading-relaxed">{t.step3}</p>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-[10px] font-mono font-bold text-accent-primary bg-accent-primary/[0.08] w-5 h-5 rounded-md flex items-center justify-center shrink-0 mt-0.5">4</span>
              <p className="text-[12px] text-text-secondary leading-relaxed">{t.step4}</p>
            </div>
          </div>
        </div>
      </div>

      {/* ═══ 5 Pillars ═══ */}
      <div className="space-y-4 anim-slide-up anim-delay-300">
        <h2 className="text-lg font-bold text-white text-center">{t.fivePillarsTitle}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {helpPillars.map((p, idx) => (
            <div 
              key={p.name}
              className="bg-surface p-4 rounded-xl border border-white/[0.04] hover:border-white/[0.06] transition-all duration-300 text-center space-y-3 group"
              style={{ animationDelay: `${idx * 60}ms` }}
            >
              <div className="p-2.5 bg-accent-primary/[0.06] rounded-xl mx-auto w-fit group-hover:scale-110 transition-transform duration-300">
                <p.icon size={20} className="text-accent-primary" />
              </div>
              <h4 className="text-xs font-bold text-white">{p.name}</h4>
              <p className="text-[10px] text-text-secondary leading-relaxed">{p.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* ═══ Keyboard Shortcuts ═══ */}
      <div className="bg-surface p-6 rounded-2xl border border-white/[0.04] space-y-4 anim-slide-up anim-delay-400">
        <h3 className="text-sm font-bold text-white">{t.shortcutsTitle}</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { keys: 'Ctrl+N', action: t.shortcutNewAnalysis },
            { keys: 'Ctrl+Enter', action: t.shortcutExecute },
            { keys: 'Ctrl+1', action: t.shortcutHome },
            { keys: 'Esc', action: t.shortcutBack },
          ].map(s => (
            <div key={s.keys} className="flex items-center space-x-3 bg-white/[0.02] rounded-lg p-3 border border-white/[0.03]">
              <kbd className="px-2 py-1 bg-white/[0.05] rounded-md border border-white/[0.08] font-mono text-[10px] text-text-secondary">{s.keys}</kbd>
              <span className="text-[11px] text-text-secondary font-medium">{s.action}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ═══ Footer ═══ */}
      <footer className="text-center py-8 border-t border-white/[0.04]">
        <div className="flex flex-col items-center space-y-3 opacity-40">
          <div className="p-2.5 bg-white/[0.03] rounded-full">
            <Heart size={16} className="text-human" />
          </div>
          <p className="text-[11px] text-white font-bold tracking-[0.2em] uppercase opacity-60">
            {t.builtByHumans}
          </p>
        </div>
      </footer>
    </div>
  );
};
