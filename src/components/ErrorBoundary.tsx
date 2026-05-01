import React, { Component, ErrorInfo, ReactNode } from 'react';
import { ShieldAlert, RotateCcw, Home } from 'lucide-react';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  private handleGoHome = () => {
    this.setState({ hasError: false, error: null });
    window.location.href = '/';
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-bg flex items-center justify-center p-6 bg-noise">
          <div className="max-w-md w-full bg-surface border border-slop/20 rounded-[2.5rem] p-10 text-center space-y-8 shadow-2xl anim-scale-in">
            <div className="flex justify-center">
              <div className="p-6 bg-slop/10 rounded-3xl border border-slop/20">
                <ShieldAlert size={48} className="text-slop" strokeWidth={1.5} />
              </div>
            </div>

            <div className="space-y-3">
              <h1 className="text-2xl font-black text-white tracking-tight uppercase">System Malfunction</h1>
              <p className="text-text-secondary text-sm leading-relaxed font-medium">
                The diagnostic engine encountered an unexpected structural failure.
              </p>
            </div>

            {this.state.error && (
              <div className="p-4 bg-white/[0.03] border border-white/[0.06] rounded-2xl">
                <code className="text-[10px] text-slop/70 font-mono break-all leading-tight">
                  {this.state.error.message}
                </code>
              </div>
            )}

            <div className="flex flex-col space-y-3 pt-2">
              <button
                onClick={this.handleReset}
                className="flex items-center justify-center space-x-3 px-8 py-4 bg-accent-primary text-bg font-black rounded-2xl hover:scale-[1.02] active:scale-95 transition-all duration-300 shadow-lg shadow-accent-primary/20"
              >
                <RotateCcw size={18} />
                <span className="uppercase tracking-[0.15em] text-[11px]">Restart Application</span>
              </button>
              
              <button
                onClick={this.handleGoHome}
                className="flex items-center justify-center space-x-3 px-8 py-4 bg-white/[0.03] border border-white/[0.06] text-text-secondary font-bold rounded-2xl hover:bg-white/[0.08] transition-all duration-300"
              >
                <Home size={18} />
                <span className="uppercase tracking-[0.15em] text-[11px]">Return Home</span>
              </button>
            </div>

            <p className="text-[9px] text-text-disabled uppercase font-black tracking-[0.3em] opacity-40">
              Neural Diagnostic Engine — Fault Protection
            </p>
          </div>
        </div>
      );
    }

    return this.children;
  }
}
