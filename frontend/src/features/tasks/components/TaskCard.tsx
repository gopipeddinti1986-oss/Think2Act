import { Task } from '@/types';
import { CheckCircle2, Circle, Clock, Trash2, Calendar, Target, Tag } from 'lucide-react';
import { formatDateTime } from '@/lib/utils';

interface TaskCardProps {
  task: Task;
  onComplete: (id: string) => void;
  onDelete: (id: string) => void;
}

export function TaskCard({ task, onComplete, onDelete }: TaskCardProps) {
  const isCompleted = task.status === 'COMPLETED';

  const priorityColor = {
    LOW: 'bg-slate-800 text-slate-400 border-slate-700',
    MEDIUM: 'bg-sky-500/10 text-sky-400 border-sky-500/20',
    HIGH: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    URGENT: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
  }[task.priority] || 'bg-slate-800 text-slate-400';

  return (
    <div className={`p-4 rounded-2xl border transition-all flex items-start justify-between gap-4 group ${
      isCompleted
        ? 'bg-slate-950/30 border-slate-900/80 opacity-75'
        : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 shadow-sm'
    }`}>
      <div className="flex items-start space-x-3.5 min-w-0">
        <button
          onClick={() => onComplete(task.id)}
          className="mt-0.5 text-slate-500 hover:text-brand-400 transition-colors shrink-0 cursor-pointer"
        >
          {isCompleted ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          ) : (
            <Circle className="w-5 h-5 group-hover:text-brand-400" />
          )}
        </button>

        <div className="min-w-0 space-y-1.5">
          <div className="flex items-center space-x-2">
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase border ${priorityColor}`}>
              {task.priority}
            </span>
            {task.category && (
              <span className="flex items-center text-xs text-slate-400 space-x-1">
                <Tag className="w-3 h-3 text-slate-500" />
                <span>{task.category}</span>
              </span>
            )}
          </div>

          <h4 className={`text-sm font-semibold truncate ${
            isCompleted ? 'line-through text-slate-500' : 'text-slate-200'
          }`}>
            {task.title}
          </h4>

          {task.description && (
            <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
              {task.description}
            </p>
          )}

          <div className="flex flex-wrap items-center gap-3 pt-1 text-[11px] text-slate-500">
            <div className="flex items-center space-x-1">
              <Clock className="w-3.5 h-3.5" />
              <span>{task.estimated_minutes}m est.</span>
            </div>
            {task.due_at && (
              <div className="flex items-center space-x-1">
                <Calendar className="w-3.5 h-3.5" />
                <span>Due {formatDateTime(task.due_at)}</span>
              </div>
            )}
            {isCompleted && task.completed_at && (
              <div className="text-emerald-500/80">
                Completed {formatDateTime(task.completed_at)}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-2 shrink-0">
        <button
          onClick={() => onDelete(task.id)}
          className="p-1.5 text-slate-500 hover:text-rose-400 rounded-lg hover:bg-slate-800 transition-colors opacity-0 group-hover:opacity-100"
          title="Delete task"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
