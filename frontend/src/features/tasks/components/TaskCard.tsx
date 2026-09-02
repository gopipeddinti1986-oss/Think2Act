import { useState } from 'react';
import { Task, Goal } from '@/types';
import { Play, MoreVertical, Trash2, CheckCircle2, Circle, Edit3 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface TaskCardProps {
  task: Task;
  goals?: Goal[];
  onSelect: (task: Task) => void;
  onComplete: (id: string) => void;
  onDelete: (id: string) => void;
}

export function TaskCard({ task, goals = [], onSelect, onComplete, onDelete }: TaskCardProps) {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const isDone = task.status === 'COMPLETED';

  const priorityDot = {
    URGENT: '🔴',
    HIGH: '🔴',
    MEDIUM: '🟡',
    LOW: '🟢',
  }[task.priority] || '🟡';

  const goal = goals.find((g) => g.id === task.goal_id);

  return (
    <div
      onClick={() => onSelect(task)}
      className={`p-5 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between group relative ${
        isDone
          ? 'bg-slate-950/40 border-slate-900/80 opacity-70'
          : 'bg-slate-900/70 border-slate-800 hover:border-slate-700 shadow-sm'
      }`}
    >
      <div className="space-y-3">
        {/* Priority Dot + Label */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-xs font-bold text-slate-300 uppercase tracking-wide">
            <span>{priorityDot}</span>
            <span>{task.priority} Priority</span>
          </div>

          <div className="relative">
            <button
              onClick={(e) => {
                e.stopPropagation();
                setMenuOpen(!menuOpen);
              }}
              className="p-1 rounded-lg text-slate-500 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            >
              <MoreVertical className="w-4 h-4" />
            </button>

            {menuOpen && (
              <div
                onClick={(e) => e.stopPropagation()}
                className="absolute right-0 top-6 z-20 w-36 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl py-1 text-xs"
              >
                {!isDone && (
                  <button
                    onClick={() => {
                      setMenuOpen(false);
                      onComplete(task.id);
                    }}
                    className="w-full px-3 py-2 text-left text-slate-200 hover:bg-slate-800 flex items-center space-x-2"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Complete</span>
                  </button>
                )}
                <button
                  onClick={() => {
                    setMenuOpen(false);
                    onDelete(task.id);
                  }}
                  className="w-full px-3 py-2 text-left text-rose-400 hover:bg-rose-500/10 flex items-center space-x-2"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Delete</span>
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Title */}
        <h3 className={`text-base font-bold leading-snug ${isDone ? 'line-through text-slate-500' : 'text-slate-100 group-hover:text-brand-300 transition-colors'}`}>
          {task.title}
        </h3>

        {/* Goal & Skill Info */}
        <div className="space-y-1 text-xs text-slate-400">
          {goal && (
            <p className="truncate">
              <span className="text-slate-500">Goal: </span>
              <span className="text-slate-300 font-semibold">{goal.title}</span>
            </p>
          )}
          {task.category && (
            <p className="truncate">
              <span className="text-slate-500">Skill: </span>
              <span className="text-brand-400 font-semibold">{task.category}</span>
            </p>
          )}
          <p className="text-slate-500">
            {task.estimated_minutes} min · {task.due_at ? `Due ${new Date(task.due_at).toLocaleDateString([], { month: 'short', day: 'numeric' })}` : 'Due today'}
          </p>
        </div>
      </div>

      {/* Start Button */}
      <div className="pt-4 mt-4 border-t border-slate-800/80 flex items-center justify-between">
        {!isDone ? (
          <button
            onClick={(e) => {
              e.stopPropagation();
              navigate('/focus');
            }}
            className="px-4 py-1.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold flex items-center space-x-1.5 shadow-md shadow-brand-500/20 transition-all cursor-pointer"
          >
            <Play className="w-3 h-3 fill-current" />
            <span>Start</span>
          </button>
        ) : (
          <span className="text-xs font-semibold text-emerald-400 flex items-center space-x-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Done</span>
          </span>
        )}
      </div>
    </div>
  );
}
