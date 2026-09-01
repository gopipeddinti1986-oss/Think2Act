import { useState } from 'react';
import { Task } from '@/types';
import { CreatePlannerEntryInput } from '@/services/api/planner';
import { X, Calendar, Clock } from 'lucide-react';

interface ScheduleModalProps {
  isOpen: boolean;
  tasks: Task[];
  initialTaskId?: string;
  onClose: () => void;
  onSubmit: (data: CreatePlannerEntryInput) => Promise<void>;
}

export function ScheduleModal({ isOpen, tasks, initialTaskId, onClose, onSubmit }: ScheduleModalProps) {
  const [taskId, setTaskId] = useState(initialTaskId || (tasks[0]?.id || ''));
  const [date, setDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [startTime, setStartTime] = useState('09:00');
  const [durationMins, setDurationMins] = useState(60);
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!taskId) return;

    setSubmitting(true);
    try {
      const startDateTime = new Date(`${date}T${startTime}:00`);
      const endDateTime = new Date(startDateTime.getTime() + durationMins * 60000);

      await onSubmit({
        task_id: taskId,
        start_at: startDateTime.toISOString(),
        end_at: endDateTime.toISOString(),
        status: 'SCHEDULED',
        source: 'MANUAL',
      });
      onClose();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md overflow-hidden shadow-2xl animate-in fade-in zoom-in-95">
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Calendar className="w-5 h-5 text-brand-400" />
            <h3 className="text-lg font-bold text-slate-100">Schedule Time Block</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Select Task *
            </label>
            <select
              value={taskId}
              onChange={(e) => setTaskId(e.target.value)}
              required
              className="w-full px-3.5 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-sm text-slate-100 focus:outline-none focus:border-brand-500"
            >
              <option value="">-- Choose a task --</option>
              {tasks.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.title} ({t.priority})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Date *
            </label>
            <input
              type="date"
              required
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-sm text-slate-100 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Start Time *
              </label>
              <input
                type="time"
                required
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                className="w-full px-3.5 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-sm text-slate-100 focus:outline-none focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Duration (Min)
              </label>
              <input
                type="number"
                min="15"
                max="360"
                step="15"
                value={durationMins}
                onChange={(e) => setDurationMins(parseInt(e.target.value) || 60)}
                className="w-full px-3.5 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-sm text-slate-100 focus:outline-none focus:border-brand-500"
              />
            </div>
          </div>

          <div className="pt-4 flex items-center justify-end space-x-3 border-t border-slate-800/80">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting || !taskId}
              className="px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-brand-500/25 transition-all disabled:opacity-50"
            >
              {submitting ? 'Scheduling...' : 'Lock Time Block'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
