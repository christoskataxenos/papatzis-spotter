import React from 'react';
import { useAppStore } from '../store/useAppStore';
import { X, CheckCircle2, AlertCircle, Info } from 'lucide-react';

export const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useAppStore();

  return (
    <div className="fixed bottom-6 right-6 z-[100] flex flex-col space-y-2.5">
      {toasts.map((toast) => (
        <div 
          key={toast.id}
          className={`
            flex items-center space-x-3 px-5 py-3.5 rounded-xl border backdrop-blur-xl shadow-strong
            anim-slide-up
            ${toast.type === 'success' 
              ? 'bg-human/[0.08] border-human/[0.12] text-human' 
              : toast.type === 'error' 
                ? 'bg-slop/[0.08] border-slop/[0.12] text-slop' 
                : 'bg-accent-primary/[0.08] border-accent-primary/[0.12] text-accent-primary'
            }
          `}
        >
          {toast.type === 'success' && <CheckCircle2 size={16} />}
          {toast.type === 'error' && <AlertCircle size={16} />}
          {toast.type === 'info' && <Info size={16} />}
          
          <p className="text-sm font-medium text-white">{toast.message}</p>
          
          <button 
            onClick={() => removeToast(toast.id)}
            className="p-1 hover:bg-white/[0.05] rounded-lg transition-colors ml-2"
          >
            <X size={12} className="opacity-40 hover:opacity-100 transition-opacity" />
          </button>
        </div>
      ))}
    </div>
  );
};
