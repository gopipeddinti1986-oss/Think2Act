import { LucideIcon, Sparkles } from 'lucide-react';

interface FeaturePlaceholderProps {
  title: string;
  milestone: string;
  description: string;
  icon: LucideIcon;
  features: string[];
}

export function FeaturePlaceholder({
  title,
  milestone,
  description,
  icon: Icon,
  features,
}: FeaturePlaceholderProps) {
  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center space-x-3">
        <div className="p-3 bg-brand-500/10 border border-brand-500/20 rounded-2xl text-brand-400">
          <Icon className="w-7 h-7" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-extrabold text-slate-100 tracking-tight">{title}</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-slate-800 text-brand-400 text-xs font-semibold uppercase tracking-wider">
              {milestone}
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">{description}</p>
        </div>
      </div>

      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm space-y-4">
        <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
          <Sparkles className="w-4 h-4" />
          <span>Planned Architecture Capabilities</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
          {features.map((feat, i) => (
            <div
              key={i}
              className="p-3 bg-slate-950/40 border border-slate-800/60 rounded-xl text-xs text-slate-300 flex items-center space-x-2.5"
            >
              <div className="w-1.5 h-1.5 rounded-full bg-brand-400 shrink-0" />
              <span>{feat}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
