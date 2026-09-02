import { Task } from '@/types';
import { X, CheckCircle2, Clock, Calendar, Target, Layers, Play } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface TaskDetailModalProps {
  task: Task | null;
  isOpen: boolean;
  onClose: () => void;
  onComplete: (taskId: string) => Promise<void>;
}

export function TaskDetailModal({ task, isOpen, onClose, onComplete }: TaskDetailModalProps) {
  const navigate = useNavigate();

  if (!isOpen || !task) return null;

  const priorityDot = {
    HIGH: '🔴',
    URGENT: '🔴',
    MEDIUM: '🟡',
    LOW: '🟢',
  }[task.priority] || '🟡';

  const isCompleted = task.status === 'COMPLETED';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-xl overflow-hidden shadow-2xl animate-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-start justify-between">
          <div className="space-y-1">
            <div className="flex items-center space-x-2 text-xs">
              <span>{priorityDot}</span>
              <span className="font-bold text-slate-300 uppercase tracking-wider">{task.priority} Priority</span>
              {task.category && (
                <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 text-[10px]">
                  {task.category}
                </span>
              )}
            </div>
            <h2 className="text-xl font-bold text-slate-100">{task.title}</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6 max-h-[70vh] overflow-y-auto">
          {/* Metadata Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div className="p-3 bg-slate-950/60 border border-slate-800/80 rounded-2xl">
              <div className="text-[10px] text-slate-500 uppercase font-bold flex items-center space-x-1">
                <Clock className="w-3 h-3" />
                <span>Estimate</span>
              </div>
              <p className="text-sm font-bold text-slate-200 mt-1">{task.estimated_minutes} min</p>
            </div>

            <div className="p-3 bg-slate-950/60 border border-slate-800/80 rounded-2xl">
              <div className="text-[10px] text-slate-500 uppercase font-bold flex items-center space-x-1">
                <Calendar className="w-3 h-3" />
                <span>Due Date</span>
              </div>
              <p className="text-sm font-bold text-slate-200 mt-1">
                {task.due_at ? new Date(task.due_at).toLocaleDateString([], { month: 'short', day: 'numeric' }) : 'Today'}
              </p>
            </div>

            <div className="p-3 bg-slate-950/60 border border-slate-800/80 rounded-2xl col-span-2 sm:col-span-1">
              <div className="text-[10px] text-slate-500 uppercase font-bold flex items-center space-x-1">
                <Target className="w-3 h-3" />
                <span>Status</span>
              </div>
              <p className={`text-sm font-bold mt-1 ${isCompleted ? 'text-emerald-400' : 'text-brand-400'}`}>
                {task.status}
              </p>
            </div>
          </div>

          {/* Description */}
          <div className="space-y-1.5">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Description</h4>
            <p className="text-sm text-slate-300 leading-relaxed p-4 bg-slate-950/40 rounded-2xl border border-slate-850">
              {task.description || 'No detailed description provided.'}
            </p>
          </div>

          {/* Schedule placeholder */}
          <div className="space-y-1.5">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Schedule</h4>
            <p className="text-xs text-slate-500 p-3 bg-slate-950/30 rounded-xl border border-slate-850">
              {isCompleted ? 'Completed' : 'Ready to be scheduled in Daily Planner'}
            </p>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-6 border-t border-slate-800 bg-slate-950/60 flex items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => {
                onClose();
                navigate('/focus');
              }}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-750 text-slate-200 text-xs font-semibold rounded-xl flex items-center space-x-1.5 transition-colors cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Start Focus</span>
            </button>
            <button
              onClick={() => {
                onClose();
                navigate('/planner');
              }}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-750 text-slate-200 text-xs font-semibold rounded-xl transition-colors cursor-pointer"
            >
              Reschedule
            </button>
          </div>

          {!isCompleted ? (
            <button
              onClick={async () => {
                await onComplete(task.id);
                onClose();
              }}
              className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-emerald-600/25 flex items-center space-x-1.5 transition-all cursor-pointer"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Mark Complete</span>
            </button>
          ) : (
            <span className="text-xs font-bold text-emerald-400 flex items-center space-x-1">
              <CheckCircle2 className="w-4 h-4" />
              <span>Completed</span>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
