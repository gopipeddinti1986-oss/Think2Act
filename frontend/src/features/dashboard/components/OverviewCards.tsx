import { TasksSummary } from '@/types';
import { CheckCircle2, Flame, Clock, Award } from 'lucide-react';

interface OverviewCardsProps {
  summary: TasksSummary;
  productivityScore: number;
  focusMinutes: number;
  readinessScore: number;
}

export function OverviewCards({
  summary,
  productivityScore,
  focusMinutes,
  readinessScore
}: OverviewCardsProps) {
  const hours = Math.floor(focusMinutes / 60);
  const minutes = focusMinutes % 60;
  const focusTimeStr = hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;

  const cards = [
    {
      title: 'Tasks',
      value: `${summary.completed} / ${summary.total}`,
      subtitle: `${summary.completion_rate}% completed`,
      icon: CheckCircle2,
      color: 'text-emerald-400',
      bgColor: 'bg-emerald-500/10',
      borderColor: 'border-emerald-500/20'
    },
    {
      title: 'Productivity',
      value: `${productivityScore} / 100`,
      subtitle: summary.total > 0 ? 'Execution Score' : 'No activity yet',
      icon: Flame,
      color: 'text-amber-400',
      bgColor: 'bg-amber-500/10',
      borderColor: 'border-amber-500/20'
    },
    {
      title: 'Focus Time',
      value: focusTimeStr,
      subtitle: 'Recorded today',
      icon: Clock,
      color: 'text-sky-400',
      bgColor: 'bg-sky-500/10',
      borderColor: 'border-sky-500/20'
    },
    {
      title: 'Role Readiness',
      value: `${readinessScore}%`,
      subtitle: 'Target: Software Engineer',
      icon: Award,
      color: 'text-brand-400',
      bgColor: 'bg-brand-500/10',
      borderColor: 'border-brand-500/20'
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, i) => (
        <div
          key={i}
          className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-5 backdrop-blur-sm relative overflow-hidden group hover:border-slate-700 transition-all shadow-sm"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              {card.title}
            </span>
            <div className={`p-2 rounded-xl ${card.bgColor} ${card.borderColor} border`}>
              <card.icon className={`w-4 h-4 ${card.color}`} />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-bold text-slate-100 tracking-tight">{card.value}</div>
            <p className="text-xs text-slate-500 mt-1">{card.subtitle}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
