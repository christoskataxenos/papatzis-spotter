import React from 'react';

interface LogoProps {
  className?: string;
  size?: number;
}

export const PapatzisLogo: React.FC<LogoProps> = ({ className, size = 48 }) => {
  return (
    <div className={`relative flex flex-col items-center justify-center ${className}`} style={{ width: size, height: size }}>
      <svg 
        viewBox="0 0 100 100" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full animate-logo-zoom"
      >
        <defs>
          <filter id="intense-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3.5" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        
        <g filter="url(#intense-glow)">
        <path 
          d="M50 10C27.9086 10 10 27.9086 10 50C10 72.0914 27.9086 90 50 90C72.0914 90 90 72.0914 90 50" 
          stroke="currentColor" 
          strokeWidth="8" 
          strokeLinecap="round"
          className="opacity-20"
        />
        <path 
          d="M50 25C36.1929 25 25 36.1929 25 50C25 63.8071 36.1929 75 50 75C63.8071 75 75 63.8071 75 50" 
          stroke="currentColor" 
          strokeWidth="8" 
          strokeLinecap="round"
          className="opacity-40"
        />
        <path 
          d="M50 40C44.4772 40 40 44.4772 40 50C40 55.5228 44.4772 60 50 60C55.5228 60 60 55.5228 60 50" 
          stroke="currentColor" 
          strokeWidth="8" 
          strokeLinecap="round"
        />
        
        {/* ─── Dense Pixel Disintegration Field ─── */}
        <g className="pixel-fragments">
          {/* Large fragments near the source */}
          <rect x="72" y="32" width="6" height="6" fill="currentColor" className="opacity-70 animate-float-slow" />
          <rect x="78" y="45" width="5" height="5" fill="currentColor" className="opacity-60 animate-float" />
          <rect x="68" y="55" width="4" height="4" fill="currentColor" className="opacity-50 animate-float-fast" />
          
          {/* Medium scattered fragments */}
          <rect x="85" y="25" width="3" height="3" fill="currentColor" className="opacity-40 animate-float-slow" />
          <rect x="88" y="38" width="4" height="4" fill="currentColor" className="opacity-30 animate-float" />
          <rect x="82" y="52" width="3" height="3" fill="currentColor" className="opacity-25 animate-float-fast" />
          <rect x="76" y="20" width="3" height="3" fill="currentColor" className="opacity-35 animate-float" />
          
          {/* Tiny dust particles far out */}
          <rect x="92" y="48" width="2" height="2" fill="currentColor" className="opacity-20 animate-float-slow" />
          <rect x="86" y="60" width="2" height="2" fill="currentColor" className="opacity-15 animate-float" />
          <rect x="95" y="30" width="2" height="2" fill="currentColor" className="opacity-10 animate-float-fast" />
          <rect x="80" y="68" width="2" height="2" fill="currentColor" className="opacity-20 animate-float" />
          
          {/* Internal disintegrating pixels */}
          <rect x="62" y="25" width="4" height="4" fill="currentColor" className="opacity-40" />
          <rect x="65" y="18" width="3" height="3" fill="currentColor" className="opacity-30" />
        </g>
        
        {/* Central Pulse Dot */}
        <circle cx="50" cy="50" r="4" fill="currentColor" className="animate-pulse" />
        </g>
      </svg>
    </div>
  );
};

export const LogoWithText: React.FC<{ size?: 'sm' | 'lg' }> = ({ size = 'sm' }) => {
  const isLarge = size === 'lg';
  return (
    <div className="flex flex-col items-center space-y-4">
      <PapatzisLogo size={isLarge ? 120 : 40} className="text-accent-primary" />
      <div className="flex flex-col items-center text-center">
        <h2 className={`${isLarge ? 'text-4xl' : 'text-xs'} font-black tracking-[0.2em] text-text-primary uppercase`}>
          PAPATZIS
        </h2>
        <span className={`${isLarge ? 'text-lg mt-1' : 'text-[8px]'} font-mono font-bold text-accent-primary tracking-[0.4em] uppercase opacity-80`}>
          SPOTTER
        </span>
      </div>
    </div>
  );
};
