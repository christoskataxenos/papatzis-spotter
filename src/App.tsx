import React, { useEffect, useCallback, useState } from 'react';
import { useAppStore } from './store/useAppStore';
import { Dashboard } from './components/Dashboard';
import { Analyzer } from './components/Analyzer';
import { Audit } from './components/Audit';
import { Config } from './components/Config';
import { Help } from './components/Help';
import { ToastContainer } from './components/ToastContainer';
import { Language, translations } from './lib/i18n';
import { 
  Home, 
  Code2, 
  HelpCircle,
  Settings as SettingsIcon,
  Search,
  Globe
} from 'lucide-react';


/* ─── Sidebar Navigation Item ─── */
interface SidebarItemProps {
    icon: React.ElementType;
    label: string;
    active: boolean;
    onClick: () => void;
    shortcut?: string;
}

const SidebarItem = ({ icon: Icon, label, active, onClick, shortcut }: SidebarItemProps) => (
  <button 
    onClick={onClick}
    title={`${label}${shortcut ? ` (${shortcut})` : ''}`}
    className={`
      relative flex flex-col items-center justify-center w-full py-3 space-y-1 
      transition-all duration-300 group focus-ring outline-none
      ${active 
        ? 'text-accent-primary' 
        : 'text-text-disabled hover:text-text-secondary'
      }
    `}
  >
    <div className={`
      p-2.5 rounded-xl transition-all duration-300
      ${active 
        ? 'bg-accent-primary/10' 
        : 'group-hover:bg-white/[0.04]'
      }
    `}>
      <Icon 
        size={22} 
        strokeWidth={active ? 2.2 : 1.8}
        className={`transition-all duration-300`} 
      />
    </div>

    <span className={`
      text-[9px] uppercase font-bold tracking-[0.15em] transition-all duration-300
      ${active ? 'opacity-100' : 'text-text-secondary opacity-90 group-hover:opacity-100'}
    `}>
      {label}
    </span>

    <div className={`
      absolute right-0 w-[3px] rounded-l-full transition-all duration-500 ease-out-expo
      ${active 
        ? 'h-10 bg-accent-primary' 
        : 'h-0 bg-transparent'
      }
    `} />
  </button>
);

/* ─── Wizard Landing Page ─── */
const WizardView: React.FC<{ lang: Language }> = ({ lang }) => {
  const { setView } = useAppStore();
  const t = translations[lang];
  
  return (
    <div className="flex-1 flex items-center justify-center p-8 h-full">
      <div className="max-w-2xl text-center space-y-10 anim-scale-in">
        <div className="flex justify-center mb-6 anim-scale-in">
          <img src="/logo.png" alt="Papatzis Spotter" className="w-32 h-32" />
        </div>
        
        <div className="space-y-4 relative anim-slide-up anim-delay-200">
          <h1 className="text-6xl md:text-7xl font-black tracking-tight text-white leading-tight flex flex-col md:flex-row items-center justify-center md:space-x-4">
            <span>PAPATZIS</span>
            <span className="px-3 py-1 bg-accent-primary/10 border border-accent-primary/20 text-accent-primary text-xl font-mono tracking-[0.2em] rounded-lg uppercase">Spotter</span>
          </h1>
          <div className="flex flex-col items-center space-y-2">
            <p className="text-text-secondary text-sm md:text-base max-w-md font-medium leading-relaxed">
              {t.tagline}
            </p>
            <div className="h-px w-12 bg-accent-primary/20" />
            <span className="text-accent-primary/50 text-[10px] uppercase font-black tracking-[0.3em]">v1.4.0 — Diagnostic Engine</span>
          </div>
        </div>

        <div className="pt-2 anim-slide-up anim-delay-400">
          <button 
            onClick={() => setView('analyzer')}
            className="group relative px-12 py-5 bg-accent-primary text-bg rounded-2xl font-black text-base transition-all duration-300 hover:scale-[1.03] active:scale-95 shadow-xl shadow-accent-primary/20"
          >
            <span className="relative uppercase tracking-[0.2em] text-sm">{t.startNow}</span>
          </button>
          <p className="mt-4 text-text-secondary text-xs tracking-wider opacity-80">
            {t.press} <kbd className="px-1.5 py-0.5 bg-white/10 rounded border border-white/20 font-mono text-[10px] text-white">Ctrl+N</kbd> {t.forQuickStart}
          </p>
        </div>
      </div>
    </div>
  );
};

/* ─── Main App ─── */
function App() {
  const { currentView, setView } = useAppStore();
  const [lang, setLang] = useState<Language>('EL');
  const t = translations[lang];

  /* Keyboard shortcuts */
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.ctrlKey || e.metaKey) {
      switch (e.key) {
        case 'n':
        case 'N':
          e.preventDefault();
          setView('analyzer');
          break;
        case '1':
          e.preventDefault();
          setView('wizard');
          break;
        case '2':
          e.preventDefault();
          setView('analyzer');
          break;
        case '3':
          e.preventDefault();
          setView('audit');
          break;
      }
    }
    if (e.key === 'Escape') {
      setView('wizard');
    }
  }, [setView]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  const renderView = () => {
    switch (currentView) {
      case 'dashboard': return <Dashboard lang={lang} />;
      case 'analyzer': return <Analyzer lang={lang} />;
      case 'audit': return <Audit lang={lang} />;
      case 'config': return <Config lang={lang} />;
      case 'help': return <Help lang={lang} />;
      case 'wizard': return <WizardView lang={lang} />;
      default: return <Dashboard lang={lang} />;
    }
  };

  return (
    <div className="flex h-screen bg-bg text-text-primary font-sans antialiased overflow-hidden border border-white/[0.04] bg-noise">
      <ToastContainer />
      
      {/* ═══ Sidebar ═══ */}
      <nav className="w-[76px] border-r border-white/[0.04] flex flex-col items-center py-6 bg-surface shrink-0 z-50 relative">
        
        {/* PS Logo — Integrated Image */}
        <div 
          className="w-12 h-12 bg-surface border border-white/[0.04] rounded-xl flex items-center justify-center shadow-2xl cursor-pointer transition-all duration-300 hover:scale-[1.05] hover:border-accent-primary/30 mb-8 relative z-10 group overflow-hidden"
          onClick={() => setView('wizard')}
          title={`Papatzis Spotter — ${t.home}`}
        >
          <img src="/logo.png" alt="PS" className="w-9 h-9 object-contain" />
        </div>

        <div className="flex-1 flex flex-col space-y-1 w-full relative z-10">
          <SidebarItem 
            icon={Home} 
            label={t.home} 
            active={currentView === 'wizard'} 
            onClick={() => setView('wizard')}
            shortcut="Ctrl+1"
          />
          <SidebarItem 
            icon={Code2} 
            label={t.analyze} 
            active={currentView === 'analyzer' || currentView === 'dashboard'} 
            onClick={() => setView('analyzer')}
            shortcut="Ctrl+2"
          />
          <SidebarItem 
            icon={Search} 
            label={lang === 'EL' ? 'Batch' : 'Batch'} 
            active={currentView === 'audit'} 
            onClick={() => setView('audit')}
            shortcut="Ctrl+3"
          />
        </div>

        <div className="w-8 h-px bg-white/[0.06] my-2" />

        <div className="space-y-1 w-full relative z-10">
          {/* Language Switcher */}
          <button 
            onClick={() => setLang(lang === 'EL' ? 'EN' : 'EL')}
            className="flex flex-col items-center justify-center w-full py-3 space-y-1 text-text-disabled hover:text-text-secondary transition-colors group"
            title={t.language}
          >
            <div className="p-2.5 rounded-xl group-hover:bg-white/[0.04] transition-all">
              <Globe size={22} strokeWidth={1.8} />
            </div>
            <span className="text-[10px] font-black uppercase tracking-widest">{lang}</span>
          </button>

          <SidebarItem 
            icon={SettingsIcon} 
            label={t.settings} 
            active={currentView === 'config'} 
            onClick={() => setView('config')} 
          />
          <SidebarItem 
            icon={HelpCircle} 
            label={t.help} 
            active={currentView === 'help'} 
            onClick={() => setView('help')} 
          />
        </div>
      </nav>

      {/* ═══ Main Content ═══ */}
      <div className="flex-1 flex flex-col overflow-hidden relative">
        <div className="flex-1 relative z-10 overflow-y-auto h-full flex flex-col">
          {renderView()}
        </div>
      </div>
    </div>
  );
}

export default App;
