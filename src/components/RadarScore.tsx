import React from 'react';
import { 
  Radar, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  ResponsiveContainer 
} from 'recharts';

interface RadarScoreProps {
  pillars: Array<{
    pillar: string;
    score: number;
  }>;
  lang?: string;
}

export const RadarScore: React.FC<RadarScoreProps> = ({ pillars }) => {
  /* Προετοιμασία δεδομένων για το Radar Chart */
  const data = pillars.map(p => ({
    subject: p.pillar,
    A: Math.max(5, p.score), // Ελάχιστο 5 για να μη "χάνεται" το σχήμα
    fullMark: 100,
  }));

  return (
    <div className="w-full h-full relative group">
      {/* Background glow effects */}
      <div className="absolute inset-0 bg-accent-primary/[0.04] blur-[40px] rounded-full group-hover:bg-accent-primary/[0.08] transition-all duration-[2000ms]" />
      
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart 
          cx="50%" 
          cy="50%" 
          outerRadius="50%" 
          data={data}
          margin={{ top: 10, right: 60, bottom: 10, left: 60 }}
        >
          <PolarGrid 
            stroke="rgba(255,255,255,0.06)" 
            strokeDasharray="3 3"
          />
          <PolarAngleAxis 
            dataKey="subject" 
            tick={{ fill: 'rgba(255,255,255,0.5)', fontSize: 11, fontWeight: 700, letterSpacing: '0.02em' }}
          />
          <Radar
            name="Slop Analysis"
            dataKey="A"
            stroke="var(--accent-primary)"
            strokeWidth={2}
            fill="var(--accent-primary)"
            fillOpacity={0.25}
            animationDuration={1500}
            animationEasing="ease-out"
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
