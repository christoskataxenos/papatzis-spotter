import React from 'react';
import { Info, BookOpen, Heart, Zap, AlignLeft, BarChart3, MessageSquare, RotateCcw, LayoutTemplate } from 'lucide-react';
import { Language, translations } from '../lib/i18n';

export const Help: React.FC<{ lang: Language }> = ({ lang }) => {
  const t = translations[lang];
  
  /* Pillar info data — Synced with Engine */
  const helpPillars = [
    { icon: AlignLeft, ...t.helpPillars[0] },
    { icon: BarChart3, ...t.helpPillars[1] },
    { icon: Zap, ...t.helpPillars[2] },
    { icon: MessageSquare, ...t.helpPillars[3] },
    { icon: RotateCcw, ...t.helpPillars[4] },
    { icon: LayoutTemplate, ...t.helpPillars[5] },
  ];

  return (
    <div className="p-6 md:p-12 max-w-[1400px] mx-auto w-full space-y-12 pb-24 anim-fade-in">
      
      {/* ═══ Header ═══ */}
      <header className="flex items-center space-x-5 anim-scale-in">
        <div className="p-4 bg-accent-primary/[0.08] rounded-2xl border border-accent-primary/[0.12]">
          <BookOpen className="text-accent-primary" size={28} strokeWidth={1.75} />
        </div>
        <div className="text-left space-y-0.5">
          <h1 className="text-2xl md:text-3xl font-bold text-text-primary">{t.helpTitle}</h1>
          <p className="text-accent-primary uppercase tracking-[0.2em] text-[10px] font-black opacity-80">Forensic Knowledge Base</p>
        </div>
      </header>

      {/* ═══ Info Cards ═══ */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 anim-slide-up anim-delay-200">
        
        {/* Τι είναι το AI Slop */}
        <div className="bg-surface p-6 rounded-2xl border border-border-subtle space-y-4 hover:border-border-default transition-all duration-300">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-accent-primary/[0.08] rounded-lg">
              <Info size={18} className="text-accent-primary" />
            </div>
            <h3 className="text-lg font-bold text-text-primary">{t.whatIsSlopTitle}</h3>
          </div>
          <p className="text-[12px] text-text-secondary leading-relaxed">
            {t.whatIsSlopDesc1}
          </p>
          <p className="text-[12px] text-text-secondary leading-relaxed">
            {t.whatIsSlopDesc2}
          </p>
        </div>

        {/* Πώς λειτουργεί */}
        <div className="bg-surface p-6 rounded-2xl border border-border-subtle space-y-4 hover:border-border-default transition-all duration-300">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-accent-primary/[0.08] rounded-lg">
              <BookOpen size={18} className="text-accent-primary" />
            </div>
            <h3 className="text-lg font-bold text-text-primary">{t.howItWorksTitle}</h3>
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

      {/* ═══ 6 Pillars ═══ */}
      <div className="space-y-5 anim-slide-up anim-delay-300">
        <h2 className="text-lg font-bold text-text-primary">{t.fivePillarsTitle}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {helpPillars.map((p, idx) => (
            <div 
              key={p.name}
              className="bg-surface p-3.5 rounded-xl border border-border-subtle hover:border-border-default transition-all duration-300 text-center space-y-2.5 group"
              style={{ animationDelay: `${idx * 60}ms` }}
            >
              <div className="p-2.5 bg-accent-primary/[0.06] rounded-xl mx-auto w-fit group-hover:scale-110 transition-transform duration-300">
                <p.icon size={20} strokeWidth={1.75} className="text-accent-primary" />
              </div>
              <h4 className="text-xs font-bold text-text-primary">{p.name}</h4>
              <p className="text-[10px] text-text-secondary leading-relaxed">{p.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* ═══ Color Coding ═══ */}
      <div className="space-y-5 anim-slide-up anim-delay-400">
        <h2 className="text-lg font-bold text-text-primary">{t.colorCodeTitle}</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-surface p-5 rounded-2xl border border-slop/20 space-y-3 relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-1 h-full bg-slop" />
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 rounded-full bg-slop shadow-[0_0_10px_rgba(239,68,68,0.4)] animate-pulse" />
              <h4 className="text-xs font-bold text-slop uppercase tracking-wider">{t.colorRedName}</h4>
            </div>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              {t.colorRedDesc}
            </p>
          </div>

          <div className="bg-surface p-5 rounded-2xl border border-accent-primary/20 space-y-3 relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-1 h-full bg-accent-primary" />
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 rounded-full bg-accent-primary shadow-[0_0_10px_rgba(59,130,246,0.4)]" />
              <h4 className="text-xs font-bold text-accent-primary uppercase tracking-wider">{t.colorBlueName}</h4>
            </div>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              {t.colorBlueDesc}
            </p>
          </div>

          <div className="bg-surface p-5 rounded-2xl border border-human/20 space-y-3 relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-1 h-full bg-human" />
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 rounded-full bg-human shadow-[0_0_10px_rgba(34,197,94,0.4)]" />
              <h4 className="text-xs font-bold text-human uppercase tracking-wider">{t.colorGreenName}</h4>
            </div>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              {t.colorGreenDesc}
            </p>
          </div>
        </div>
      </div>

      {/* ═══ Keyboard Shortcuts ═══ */}
      <div className="bg-surface p-5 rounded-2xl border border-border-subtle space-y-3.5 anim-slide-up anim-delay-500">
        <h3 className="text-sm font-bold text-text-primary">{t.shortcutsTitle}</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
          {[
            { keys: 'Ctrl+N', action: t.shortcutNewAnalysis },
            { keys: 'Ctrl+Enter', action: t.shortcutExecute },
            { keys: 'Ctrl+1', action: t.shortcutHome },
            { keys: 'Esc', action: t.shortcutBack },
          ].map(s => (
            <div key={s.keys} className="flex items-center space-x-3 bg-white/[0.02] rounded-lg p-3 border border-border-subtle">
              <kbd className="px-2 py-1 bg-surface-elevated rounded-md border border-border-default font-mono text-[10px] text-text-secondary">{s.keys}</kbd>
              <span className="text-[11px] text-text-secondary font-medium">{s.action}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ═══ Footer ═══ */}
      <footer className="text-center py-6 border-t border-border-subtle">
        <div className="flex flex-col items-center space-y-2.5 opacity-40">
          <div className="p-2.5 bg-surface-elevated rounded-full">
            <Heart size={16} className="text-human" />
          </div>
          <p className="text-[11px] text-text-primary font-bold tracking-[0.2em] uppercase opacity-60">
            {t.builtByHumans}
          </p>
        </div>
      </footer>
    </div>
  );
};
