import React, { useEffect } from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  /* ESC to close */
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-8 anim-fade-in">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/80 backdrop-blur-md cursor-pointer" 
        onClick={onClose}
      />
      
      {/* Modal Container */}
      <div className="relative w-full max-w-5xl max-h-[90vh] bg-bg border border-border-subtle rounded-[2rem] shadow-strong overflow-hidden flex flex-col anim-scale-in">
        
        {/* Header */}
        <div className="flex items-center justify-between px-8 py-6 border-b border-border-subtle shrink-0 bg-surface/40 backdrop-blur-md">
          <h2 className="text-sm font-black uppercase tracking-[0.2em] text-text-secondary">
            {title}
          </h2>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-white/5 rounded-xl transition-all text-text-disabled hover:text-text-primary"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          {children}
        </div>
      </div>
    </div>
  );
};
