import React, { useState, useEffect } from 'react';
import { Settings, Shield, Zap, Sliders, Save, CheckCircle2, RotateCcw } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';

import { Language, translations } from '../lib/i18n';

/* ─── Toggle Switch Component ─── */
interface ToggleProps {
  enabled: boolean;
  onToggle: () => void;
  activeColor?: string;
  lang?: Language;
}

const Toggle = ({ enabled, onToggle, activeColor = 'bg-human', lang = 'EL' }: ToggleProps) => {
  const t = translations[lang];
  return (
    <button 
      onClick={onToggle}
      className="flex items-center space-x-3 group"
      role="switch"
      aria-checked={enabled}
    >
      <div className={`w-11 h-6 rounded-full relative transition-colors duration-300 ${enabled ? activeColor : 'bg-white/[0.06]'}`}>
        <div className={`absolute top-1 w-4 h-4 bg-white rounded-full shadow-md transition-all duration-300 ${enabled ? 'right-1' : 'left-1'}`} />
      </div>
      <span className={`text-xs font-bold transition-colors duration-200 ${enabled ? 'text-white' : 'text-text-disabled'}`}>
        {enabled ? t.active : t.inactive}
      </span>
    </button>
  );
};

export const Config: React.FC<{ lang?: Language }> = ({ lang = 'EL' }) => {
  const t = translations[lang];
  const [sensitivity, setSensitivity] = useState(50);
  const [humanityShield, setHumanityShield] = useState(true);
  const [experimental, setExperimental] = useState(false);
  const [showSaved, setShowSaved] = useState(false);
  const { addToast } = useAppStore();

  useEffect(() => {
    const savedSensitivity = localStorage.getItem('slop_sensitivity');
    const savedShield = localStorage.getItem('slop_humanity_shield');
    const savedExperimental = localStorage.getItem('slop_experimental');

    if (savedSensitivity) setSensitivity(parseInt(savedSensitivity));
    if (savedShield) setHumanityShield(savedShield === 'true');
    if (savedExperimental) setExperimental(savedExperimental === 'true');
  }, []);

  const handleSave = () => {
    localStorage.setItem('slop_sensitivity', sensitivity.toString());
    localStorage.setItem('slop_humanity_shield', humanityShield.toString());
    localStorage.setItem('slop_experimental', experimental.toString());
    
    setShowSaved(true);
    addToast(t.settingsSaved, 'success');
    setTimeout(() => setShowSaved(false), 2000);
  };

  const handleReset = () => {
    setSensitivity(50);
    setHumanityShield(true);
    setExperimental(false);
    addToast(t.settingsReset, 'info');
  };

  /* Χρώμα sensitivity indicator */
  const getSensitivityColor = () => {
    if (sensitivity < 30) return 'text-human';
    if (sensitivity < 70) return 'text-accent-primary';
    return 'text-slop';
  };

  /* Text label for heat */
  const getHeatLabel = () => {
    if (sensitivity < 30) return t.lenient;
    if (sensitivity < 70) return t.normal;
    return t.strict;
  };

  return (
    <div className="p-4 md:p-8 max-w-4xl mx-auto space-y-10 pb-20">
      
      {/* ═══ Header ═══ */}
      <header className="flex flex-col items-center text-center space-y-5 anim-scale-in">
        <div className="p-4 bg-accent-primary/[0.08] rounded-2xl border border-accent-primary/[0.12]">
          <Settings className="text-accent-primary" size={28} strokeWidth={1.8} />
        </div>
        <div className="space-y-1">
          <h1 className="text-2xl md:text-3xl font-bold text-white">{t.settings}</h1>
          <p className="text-accent-primary uppercase tracking-[0.2em] text-[10px] font-black opacity-80">Papatzis Engine Config</p>
        </div>
      </header>

      {/* ═══ Settings Card ═══ */}
      <div className="bg-surface p-6 md:p-8 rounded-[1.5rem] border border-white/[0.04] space-y-8 shadow-strong anim-slide-up anim-delay-200">
        
        {/* Sensitivity (Heat) Slider */}
        <section className="space-y-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-accent-primary/[0.08] rounded-lg">
                <Sliders size={18} className="text-accent-primary" />
              </div>
              <h3 className="text-base font-bold text-white">{t.sensitivityLabel}</h3>
            </div>
            <div className="flex items-center space-x-3">
                <span className={`text-[10px] uppercase font-black px-2 py-1 rounded bg-white/[0.03] border border-white/[0.06] ${getSensitivityColor()}`}>
                    {getHeatLabel()}
                </span>
                <span className={`font-mono font-bold text-lg tabular-nums ${getSensitivityColor()}`}>{sensitivity}%</span>
            </div>
          </div>
          <div className="space-y-3 pl-11">
            <input 
              type="range" 
              min="0"
              max="100"
              value={sensitivity}
              onChange={(e) => setSensitivity(parseInt(e.target.value))}
              className="w-full h-1.5 bg-white/[0.06] rounded-full appearance-none cursor-pointer accent-accent-primary"
            />
            <div className="flex justify-between text-[9px] uppercase font-black text-white/40 tracking-[0.2em]">
              <span className={sensitivity < 30 ? 'text-human' : ''}>{t.lenient}</span>
              <span className={sensitivity >= 30 && sensitivity < 70 ? 'text-accent-primary' : ''}>{t.normal}</span>
              <span className={sensitivity >= 70 ? 'text-slop' : ''}>{t.strict}</span>
            </div>
          </div>
        </section>

        {/* Separator */}
        <div className="border-t border-white/[0.04]" />

        {/* Toggle settings */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <section className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-human/[0.08] rounded-lg">
                <Shield size={16} className="text-human" />
              </div>
              <h3 className="font-bold text-white text-sm">{t.humanityShieldTitle}</h3>
            </div>
            <p className="text-[11px] text-text-secondary leading-relaxed pl-11">
              {t.humanityShieldDesc}
            </p>
            <div className="pl-11">
              <Toggle enabled={humanityShield} onToggle={() => setHumanityShield(!humanityShield)} lang={lang} />
            </div>
          </section>

          <section className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-warning/[0.08] rounded-lg">
                <Zap size={16} className="text-warning" />
              </div>
              <h3 className="font-bold text-white text-sm">{t.experimentalTitle}</h3>
            </div>
            <p className="text-[11px] text-text-secondary leading-relaxed pl-11">
              {t.experimentalDesc}
            </p>
            <div className="pl-11">
              <Toggle enabled={experimental} onToggle={() => setExperimental(!experimental)} activeColor="bg-warning" lang={lang} />
            </div>
          </section>
        </div>

        {/* Separator */}
        <div className="border-t border-white/[0.04]" />

        {/* Action buttons */}
        <div className="flex items-center justify-between">
          <button 
            onClick={handleReset}
            className="flex items-center space-x-2 px-4 py-2.5 bg-white/[0.03] border border-white/[0.04] rounded-xl hover:bg-white/[0.05] transition-all duration-200 text-text-secondary hover:text-white text-xs font-bold"
          >
            <RotateCcw size={14} />
            <span>{t.reset}</span>
          </button>
          
          <button 
            onClick={handleSave}
            className="flex items-center space-x-2 px-6 py-2.5 bg-accent-primary text-bg font-bold rounded-xl hover:scale-[1.03] active:scale-95 transition-all duration-300 shadow-lg shadow-accent-primary/15"
          >
            {showSaved ? <CheckCircle2 size={16} /> : <Save size={16} />}
            <span className="uppercase tracking-[0.12em] text-[11px]">{showSaved ? t.saved : t.save}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
