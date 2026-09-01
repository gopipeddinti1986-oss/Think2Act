import { PlannerEntry } from '@/services/api/planner';
import { Clock, Trash2, CheckCircle2, Play, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface PlannerTimelineProps {
  entries: PlannerEntry[];
  onDelete: (id: string) => void;
}

export function PlannerTimeline({ entries, onDelete }: PlannerTimelineProps) {
  const navigate = useNavigate();

  const formatTime = (isoString: string) => {
    return new Date(isoString).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (entries.length === 0) {
    return (
      <div className="py-16 text-center bg-slate-900/40 border border-dashed border-slate-800 rounded-2xl">
        <Clock className="w-10 h-10 text-slate-600 mx-auto mb-3" />
        <h3 className="text-base font-bold text-slate-200">No Time Blocks Scheduled</h3>
        <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1">
          Allocate your pending tasks into realistic morning, afternoon, or evening slots.
        </p>
      </div>
    );
  }

  return (
    <div className="relative border-l-2 border-slate-800 ml-4 pl-6 space-y-6">
      {entries.map((entry) => {
        const isCompleted = entry.status === 'COMPLETED';
        return (
          <div key={entry.id} className="relative group">
            {/* Timeline node icon */}
            <div className={`absolute -left-[31px] top-1.5 w-4 h-4 rounded-full border-2 border-slate-950 flex items-center justify-center ${
              isCompleted ? 'bg-emerald-500' : 'bg-brand-500'
            }`} />

            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
              <div className="space-y-1 min-w-0">
                <div className="flex items-center space-x-2 text-xs font-semibold text-brand-400">
                  <Clock className="w-3.5 h-3.5" />
                  <span>
                    {formatTime(entry.start_at)} — {formatTime(entry.end_at)}
                  </span>
                  {entry.source === 'AUTO_SUGGESTED' && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                      Auto-Plan
                    </span>
                  )}
                </div>

                <h4 className={`text-base font-bold truncate ${
                  isCompleted ? 'line-through text-slate-500' : 'text-slate-100'
                }`}>
                  {entry.task?.title || 'Scheduled Task'}
                </h4>

                {entry.task?.category && (
                  <p className="text-xs text-slate-500">Category: {entry.task.category}</p>
                )}
              </div>

              <div className="flex items-center space-x-3 shrink-0">
                <button
                  onClick={() => navigate('/focus')}
                  className="px-3.5 py-1.5 rounded-xl bg-brand-600/20 hover:bg-brand-600/40 border border-brand-500/30 text-brand-300 text-xs font-semibold flex items-center space-x-1.5 transition-colors cursor-pointer"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>Focus Now</span>
                </button>
                <button
                  onClick={() => onDelete(entry.id)}
                  className="p-1.5 text-slate-500 hover:text-rose-400 rounded-lg hover:bg-slate-800 transition-colors opacity-0 group-hover:opacity-100 cursor-pointer"
                  title="Remove time block"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
