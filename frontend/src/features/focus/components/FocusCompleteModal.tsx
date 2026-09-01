import { useState } from 'react';
import { Award, CheckCircle2, X } from 'lucide-react';

interface FocusCompleteModalProps {
  isOpen: boolean;
  productiveSeconds: number;
  distractedSeconds: number;
  taskTitle?: string;
  onClose: () => void;
  onConfirm: (markTaskCompleted: boolean) => Promise<void>;
}

export function FocusCompleteModal({
  isOpen,
  productiveSeconds,
  distractedSeconds,
  taskTitle,
  onClose,
  onConfirm
}: FocusCompleteModalProps) {
  const [markCompleted, setMarkCompleted] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const productiveMins = Math.round(productiveSeconds / 60);
  const distractedMins = Math.round(distractedSeconds / 60);
  const totalMins = productiveMins + distractedMins;
  const ratio = totalMins > 0 ? Math.round((productiveMins / totalMins) * 100) : 100;

  const handleFinish = async () => {
    setSubmitting(true);
    try {
      await onConfirm(markCompleted);
      onClose();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl p-6 text-center space-y-5 animate-in fade-in zoom-in-95">
        <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 mx-auto flex items-center justify-center">
          <Award className="w-6 h-6" />
        </div>

        <div>
          <h3 className="text-xl font-extrabold text-slate-100">Session Complete!</h3>
          <p className="text-xs text-slate-400 mt-1">
            {taskTitle ? `Completed work on: ${taskTitle}` : 'Great deep-work block recorded'}
          </p>
        </div>

        {/* Stats summary */}
        <div className="grid grid-cols-3 gap-2 p-4 bg-slate-950/60 border border-slate-800/80 rounded-2xl">
          <div>
            <div className="text-lg font-bold text-emerald-400">{productiveMins}m</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold">Focused</div>
          </div>
          <div>
            <div className="text-lg font-bold text-amber-400">{distractedMins}m</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold">Distracted</div>
          </div>
          <div>
            <div className="text-lg font-bold text-brand-400">{ratio}%</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold">Efficiency</div>
          </div>
        </div>

        {/* Prompt: Did you complete the task? */}
        {taskTitle && (
          <div className="text-left p-4 bg-slate-950/40 border border-slate-800/60 rounded-2xl space-y-2">
            <p className="text-xs font-semibold text-slate-300">Did you finish this task?</p>
            <div className="flex items-center space-x-4 pt-1">
              <label className="flex items-center space-x-2 text-xs text-slate-200 cursor-pointer">
                <input
                  type="radio"
                  name="task_status"
                  checked={markCompleted}
                  onChange={() => setMarkCompleted(true)}
                  className="text-brand-600 focus:ring-brand-500"
                />
                <span>Yes, mark as Completed</span>
              </label>
              <label className="flex items-center space-x-2 text-xs text-slate-400 cursor-pointer">
                <input
                  type="radio"
                  name="task_status"
                  checked={!markCompleted}
                  onChange={() => setMarkCompleted(false)}
                  className="text-brand-600 focus:ring-brand-500"
                />
                <span>Still In Progress</span>
              </label>
            </div>
          </div>
        )}

        <button
          onClick={handleFinish}
          disabled={submitting}
          className="w-full py-3 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm rounded-xl shadow-lg shadow-brand-500/25 transition-all cursor-pointer disabled:opacity-50"
        >
          {submitting ? 'Saving Progress...' : 'Save & Update Progress'}
        </button>
      </div>
    </div>
  );
}
