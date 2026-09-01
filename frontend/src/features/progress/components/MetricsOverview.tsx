import { ProductivityTrendResponse } from '@/services/api/progress';
import { TrendingUp, Flame, Award, Clock } from 'lucide-react';

interface MetricsOverviewProps {
  data: ProductivityTrendResponse;
}

export function MetricsOverview({ data }: MetricsOverviewProps) {
  const isPositive = data.change_percentage >= 0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase text-slate-400">Average Productivity</span>
          <Flame className="w-4 h-4 text-amber-400" />
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <div className="text-3xl font-extrabold text-slate-100">{data.current_score}</div>
          <span className="text-xs text-slate-500">/ 100</span>
        </div>
        <div className="flex items-center space-x-1 text-xs mt-2">
          <TrendingUp className={`w-3.5 h-3.5 ${isPositive ? 'text-emerald-400' : 'text-rose-400'}`} />
          <span className={isPositive ? 'text-emerald-400' : 'text-rose-400'}>
            {isPositive ? `+${data.change_percentage}%` : `${data.change_percentage}%`}
          </span>
          <span className="text-slate-500">vs previous {data.range_days}d</span>
        </div>
      </div>

      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase text-slate-400">Estimation Accuracy</span>
          <Award className="w-4 h-4 text-brand-400" />
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <div className="text-3xl font-extrabold text-brand-400">{data.estimation_accuracy_percentage}%</div>
        </div>
        <p className="text-xs text-slate-500 mt-2">Planned vs. Actual time delta</p>
      </div>

      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-sm lg:col-span-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase text-slate-400">Peak Focus Zone</span>
          <Clock className="w-4 h-4 text-sky-400" />
        </div>
        <div className="mt-3 text-lg font-bold text-slate-100">
          {data.strongest_focus_period}
        </div>
        <p className="text-xs text-slate-500 mt-1">
          Historically highest task completion and lowest distraction rates.
        </p>
      </div>
    </div>
  );
}
