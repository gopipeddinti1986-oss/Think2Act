import { Task } from '@/types';
import { CheckCircle2, Circle, Clock, ArrowUpRight } from 'lucide-react';
import { Link } from 'react-router-dom';

interface TodayTasksCardProps {
  tasks: Task[];
  onComplete: (taskId: string) => void;
}

export function TodayTasksCard({ tasks, onComplete }: TodayTasksCardProps) {
  const priorityColor = {
    LOW: 'bg-slate-800 text-slate-400',
    MEDIUM: 'bg-sky-500/15 text-sky-400 border border-sky-500/20',
    HIGH: 'bg-amber-500/15 text-amber-400 border border-amber-500/20',
    URGENT: 'bg-rose-500/15 text-rose-400 border border-rose-500/20',
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-sm shadow-sm flex flex-col justify-between h-full">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-bold text-slate-100">Today's Priority Tasks</h3>
            <p className="text-xs text-slate-500">Scheduled execution items</p>
          </div>
          <Link
            to="/tasks"
            className="text-xs font-semibold text-brand-400 hover:text-brand-300 flex items-center space-x-1 transition-colors"
          >
            <span>View All</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {tasks.length === 0 ? (
          <div className="py-8 text-center border border-dashed border-slate-800 rounded-xl">
            <p className="text-sm text-slate-400 font-medium">No tasks recorded yet</p>
            <p className="text-xs text-slate-500 mt-1">Create a goal or task to start your daily plan</p>
            <Link
              to="/tasks"
              className="inline-block mt-3 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg transition-colors"
            >
              + Add Task
            </Link>
          </div>
        ) : (
          <div className="space-y-2.5">
            {tasks.map((task) => {
              const isCompleted = task.status === 'COMPLETED';
              return (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-3 bg-slate-950/40 hover:bg-slate-950/80 border border-slate-800/60 rounded-xl transition-colors group"
                >
                  <div className="flex items-center space-x-3 min-w-0">
                    <button
                      onClick={() => onComplete(task.id)}
                      className="text-slate-500 hover:text-brand-400 transition-colors shrink-0 cursor-pointer"
                    >
                      {isCompleted ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                      ) : (
                        <Circle className="w-5 h-5 group-hover:text-brand-400" />
                      )}
                    </button>
                    <div className="min-w-0">
                      <p
                        className={`text-sm font-medium truncate ${
                          isCompleted ? 'line-through text-slate-500' : 'text-slate-200'
                        }`}
                      >
                        {task.title}
                      </p>
                      <div className="flex items-center space-x-2 text-[11px] text-slate-500 mt-0.5">
                        <span className="flex items-center space-x-1">
                          <Clock className="w-3 h-3" />
                          <span>{task.estimated_minutes}m</span>
                        </span>
                        {task.category && <span>• {task.category}</span>}
                      </div>
                    </div>
                  </div>

                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase shrink-0 ${
                      priorityColor[task.priority] || 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {task.priority}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
