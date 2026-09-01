import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { plannerApi, CreatePlannerEntryInput, AutoScheduleResponse } from '@/services/api/planner';
import { tasksApi } from '@/services/api/tasks';
import { PlannerTimeline } from '../components/PlannerTimeline';
import { ScheduleModal } from '../components/ScheduleModal';
import { Calendar, Plus, Sparkles, AlertTriangle, CheckCircle2 } from 'lucide-react';

export function PlannerPage() {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [autoScheduleData, setAutoScheduleData] = useState<AutoScheduleResponse | null>(null);

  const queryClient = useQueryClient();

  const { data: entries = [], isLoading } = useQuery({
    queryKey: ['planner', selectedDate],
    queryFn: () => {
      const start = new Date(`${selectedDate}T00:00:00Z`).toISOString();
      const end = new Date(`${selectedDate}T23:59:59Z`).toISOString();
      return plannerApi.list(start, end);
    },
  });

  const { data: tasks = [] } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => tasksApi.list({ status: 'TODO' }),
  });

  const createMutation = useMutation({
    mutationFn: (data: CreatePlannerEntryInput) => plannerApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['planner'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => plannerApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['planner'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });

  const handleAutoPlan = async () => {
    try {
      const res = await plannerApi.autoSchedule(selectedDate);
      setAutoScheduleData(res);
    } catch (e) {
      console.error(e);
    }
  };

  const applySuggestions = async () => {
    if (!autoScheduleData) return;
    for (const sugg of autoScheduleData.suggestions) {
      await createMutation.mutateAsync({
        task_id: sugg.task_id,
        start_at: sugg.start_at,
        end_at: sugg.end_at,
        source: 'AUTO_SUGGESTED',
        status: 'SCHEDULED'
      });
    }
    setAutoScheduleData(null);
  };

  return (
    <div className="space-y-6">
      {/* Header & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <Calendar className="w-6 h-6 text-brand-400" />
            <span>Daily Execution Planner</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Allocate your priorities into realistic time blocks and avoid overload.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleAutoPlan}
            className="px-4 py-2.5 bg-slate-900 hover:bg-slate-850 border border-brand-500/30 text-brand-300 text-xs font-semibold rounded-xl flex items-center space-x-2 transition-colors cursor-pointer"
          >
            <Sparkles className="w-4 h-4 text-brand-400" />
            <span>Smart Auto-Plan</span>
          </button>
          <button
            onClick={() => setModalOpen(true)}
            className="px-4 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer shrink-0"
          >
            <Plus className="w-4 h-4" />
            <span>Schedule Block</span>
          </button>
        </div>
      </div>

      {/* Date selector & Daily Stats */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-slate-900/60 border border-slate-800 rounded-2xl gap-4">
        <div className="flex items-center space-x-3">
          <label className="text-xs font-semibold text-slate-400 uppercase">Viewing Schedule for:</label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="px-3 py-1.5 bg-slate-950/60 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500 font-medium"
          />
        </div>

        <div className="text-xs text-slate-400 flex items-center space-x-4">
          <span>{entries.length} Scheduled Blocks</span>
        </div>
      </div>

      {/* Auto-Plan Recommendation Banner */}
      {autoScheduleData && (
        <div className="bg-slate-900/90 border border-brand-500/40 rounded-2xl p-6 space-y-4 animate-in fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" />
              <span>Smart Schedule Generated</span>
            </div>
            {autoScheduleData.is_overloaded && (
              <div className="flex items-center space-x-1.5 text-amber-400 text-xs font-semibold px-2.5 py-1 bg-amber-500/10 border border-amber-500/20 rounded-full">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>Overload Warning: {autoScheduleData.total_planned_hours}h planned vs {autoScheduleData.available_hours}h capacity</span>
              </div>
            )}
          </div>

          <div className="space-y-2">
            {autoScheduleData.suggestions.map((s, i) => (
              <div key={i} className="p-3 bg-slate-950/50 border border-slate-800 rounded-xl flex items-center justify-between text-xs">
                <div className="space-y-0.5">
                  <p className="font-semibold text-slate-200">{s.task_title}</p>
                  <p className="text-slate-500">
                    {new Date(s.start_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} —{' '}
                    {new Date(s.end_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
                <span className="font-bold text-[10px] px-2 py-0.5 rounded bg-brand-500/10 text-brand-400 border border-brand-500/20">
                  {s.priority}
                </span>
              </div>
            ))}
          </div>

          <div className="flex items-center space-x-3 pt-2">
            <button
              onClick={applySuggestions}
              className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-brand-500/25 transition-all"
            >
              Accept All & Schedule
            </button>
            <button
              onClick={() => setAutoScheduleData(null)}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl transition-colors"
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      {/* Timeline View */}
      {isLoading ? (
        <div className="space-y-4 pl-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-slate-900/60 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : (
        <PlannerTimeline entries={entries} onDelete={(id) => deleteMutation.mutate(id)} />
      )}

      {/* Schedule Modal */}
      <ScheduleModal
        isOpen={modalOpen}
        tasks={tasks}
        onClose={() => setModalOpen(false)}
        onSubmit={async (data) => {
          await createMutation.mutateAsync(data);
        }}
      />
    </div>
  );
}
