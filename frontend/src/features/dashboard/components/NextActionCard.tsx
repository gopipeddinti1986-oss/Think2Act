import { useNavigate } from 'react-router-dom';
import { Task } from '@/types';
import { Play, Sparkles, Plus, Clock, Tag } from 'lucide-react';

interface NextActionCardProps {
  task?: Task;
  onStartFocus?: (taskId: string) => void;
}

export function NextActionCard({ task, onStartFocus }: NextActionCardProps) {
  const navigate = useNavigate();

  if (!task) {
    return (
      <div className="bg-gradient-to-r from-brand-900/30 via-slate-900/60 to-slate-900/60 border border-brand-500/20 rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" />
              <span>Next Action Ready</span>
            </div>
            <h3 className="text-xl font-bold text-slate-100">Ready to build your execution profile?</h3>
            <p className="text-sm text-slate-400 max-w-xl">
              Turn your thoughts and goals into your first actionable task to unlock the complete productivity feedback loop.
            </p>
          </div>
          <button
            onClick={() => navigate('/tasks')}
            className="shrink-0 px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer"
          >
            <Plus className="w-4 h-4" />
            <span>Create First Task</span>
          </button>
        </div>
      </div>
    );
  }

  const priorityColor = {
    LOW: 'text-slate-400 bg-slate-800 border-slate-700',
    MEDIUM: 'text-sky-400 bg-sky-500/10 border-sky-500/20',
    HIGH: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    URGENT: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
  }[task.priority] || 'text-slate-400 bg-slate-800';

  return (
    <div className="bg-gradient-to-r from-brand-950/40 via-slate-900/80 to-slate-900/80 border border-brand-500/30 rounded-2xl p-6 relative overflow-hidden shadow-lg shadow-brand-950/30">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center space-x-2.5">
            <span className="flex items-center space-x-1 px-2.5 py-0.5 rounded-full bg-brand-500/20 border border-brand-500/30 text-brand-300 font-semibold text-xs tracking-wide uppercase">
              <Sparkles className="w-3 h-3 mr-1" /> Next Action
            </span>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase border ${priorityColor}`}>
              {task.priority}
            </span>
            {task.category && (
              <span className="flex items-center text-xs text-slate-400 space-x-1">
                <Tag className="w-3 h-3 text-slate-500" />
                <span>{task.category}</span>
              </span>
            )}
          </div>

          <h3 className="text-xl font-bold text-slate-100">{task.title}</h3>
          {task.description && (
            <p className="text-sm text-slate-400 line-clamp-2 max-w-2xl">{task.description}</p>
          )}

          <div className="flex items-center space-x-4 text-xs text-slate-500 pt-1">
            <div className="flex items-center space-x-1">
              <Clock className="w-3.5 h-3.5" />
              <span>Est. {task.estimated_minutes} min</span>
            </div>
            {task.due_at && (
              <div>Due {new Date(task.due_at).toLocaleDateString()}</div>
            )}
          </div>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <button
            onClick={() => onStartFocus?.(task.id)}
            className="px-5 py-3 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm flex items-center space-x-2 shadow-lg shadow-brand-500/30 hover:shadow-brand-500/40 transition-all cursor-pointer group"
          >
            <Play className="w-4 h-4 fill-current transition-transform group-hover:scale-110" />
            <span>Start Focus Session</span>
          </button>
        </div>
      </div>
    </div>
  );
}
