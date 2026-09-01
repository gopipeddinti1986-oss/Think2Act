import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { progressApi } from '@/services/api/progress';
import { MetricsOverview } from '../components/MetricsOverview';
import { ProductivityChart } from '../components/ProductivityChart';
import { TrendingUp, Clock, CheckCircle2, AlertCircle } from 'lucide-react';

export function ProgressPage() {
  const [rangeDays, setRangeDays] = useState<number>(30);

  const { data: progressData, isLoading } = useQuery({
    queryKey: ['productivity', rangeDays],
    queryFn: () => progressApi.getProductivityTrends(rangeDays),
  });

  return (
    <div className="space-y-8 max-w-6xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <TrendingUp className="w-6 h-6 text-brand-400" />
            <span>Execution Progress & Analytics</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Track historical productivity scores, focus consistency, and estimation accuracy over time.
          </p>
        </div>

        {/* Timeframe Selector */}
        <div className="flex items-center space-x-1 p-1 bg-slate-900 border border-slate-800 rounded-xl shrink-0">
          {[7, 30, 90].map((days) => (
            <button
              key={days}
              onClick={() => setRangeDays(days)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                rangeDays === days
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-500/25'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {days} Days
            </button>
          ))}
        </div>
      </div>

      {isLoading || !progressData ? (
        <div className="space-y-6 animate-pulse">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-slate-900/60 rounded-2xl" />
            ))}
          </div>
          <div className="h-64 bg-slate-900/60 rounded-2xl" />
        </div>
      ) : (
        <>
          {/* Key Metric Cards */}
          <MetricsOverview data={progressData} />

          {/* Productivity Trends Visual Chart */}
          <ProductivityChart history={progressData.history} />

          {/* Historical Activity Stream Breakdown */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-sm">
            <h3 className="text-base font-bold text-slate-100 mb-4">Daily Breakdown History</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 uppercase font-semibold">
                    <th className="pb-3 px-2">Date</th>
                    <th className="pb-3 px-2">Productivity Score</th>
                    <th className="pb-3 px-2">Focus Time</th>
                    <th className="pb-3 px-2">Distraction</th>
                    <th className="pb-3 px-2">Tasks Completed</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  {progressData.history
                    .slice()
                    .reverse()
                    .map((item, idx) => (
                      <tr key={idx} className="hover:bg-slate-950/40 transition-colors">
                        <td className="py-3 px-2 font-medium text-slate-200">{item.date}</td>
                        <td className="py-3 px-2">
                          <span className={`font-bold ${item.score >= 75 ? 'text-emerald-400' : item.score >= 50 ? 'text-amber-400' : 'text-slate-400'}`}>
                            {item.score > 0 ? `${item.score}/100` : '—'}
                          </span>
                        </td>
                        <td className="py-3 px-2">{item.focus_minutes}m</td>
                        <td className="py-3 px-2 text-amber-400/80">{item.distraction_minutes}m</td>
                        <td className="py-3 px-2 font-medium">{item.tasks_completed}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
