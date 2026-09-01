import { DailyMetricPoint } from '@/services/api/progress';

interface ProductivityChartProps {
  history: DailyMetricPoint[];
}

export function ProductivityChart({ history }: ProductivityChartProps) {
  const maxScore = 100;

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-slate-100">Productivity Score History</h3>
          <p className="text-xs text-slate-500">Daily execution quality index</p>
        </div>
      </div>

      {/* Bar Chart Visualization */}
      <div className="h-48 flex items-end gap-1 sm:gap-2 pt-6 pb-2">
        {history.map((point, index) => {
          const heightPct = Math.max(8, (point.score / maxScore) * 100);
          const hasActivity = point.score > 0 || point.focus_minutes > 0;

          return (
            <div key={index} className="flex-1 flex flex-col items-center h-full justify-end group relative">
              {/* Tooltip */}
              <div className="absolute -top-14 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-950 border border-slate-700 text-slate-200 text-[11px] p-2 rounded-lg shadow-xl z-20 pointer-events-none whitespace-nowrap">
                <p className="font-bold">{point.date}: {point.score}/100</p>
                <p className="text-slate-400">{point.focus_minutes}m focused • {point.tasks_completed} tasks</p>
              </div>

              {/* Bar */}
              <div
                style={{ height: `${heightPct}%` }}
                className={`w-full rounded-t-md transition-all ${
                  hasActivity
                    ? 'bg-gradient-to-t from-brand-600 to-indigo-400 group-hover:brightness-125'
                    : 'bg-slate-800/40'
                }`}
              />

              {/* Day label on every few items */}
              {(index % Math.ceil(history.length / 7) === 0 || index === history.length - 1) && (
                <span className="text-[10px] text-slate-500 mt-2 truncate max-w-full">
                  {point.date}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
