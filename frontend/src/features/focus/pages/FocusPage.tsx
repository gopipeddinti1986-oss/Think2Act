import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { focusApi } from '@/services/api/focus';
import { tasksApi } from '@/services/api/tasks';
import { FocusCompleteModal } from '../components/FocusCompleteModal';
import { Play, Square, AlertCircle } from 'lucide-react';

export function FocusPage() {
  const queryClient = useQueryClient();

  const [isRunning, setIsRunning] = useState(false);
  const [isDistracted, setIsDistracted] = useState(false);
  const [productiveSeconds, setProductiveSeconds] = useState(0);
  const [distractedSeconds, setDistractedSeconds] = useState(0);
  const [selectedTaskId, setSelectedTaskId] = useState<string>('');
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [completeModalOpen, setCompleteModalOpen] = useState(false);

  const { data: tasks = [] } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => tasksApi.list({ status: 'TODO' }),
  });

  const { data: todaySummary } = useQuery({
    queryKey: ['focus_today'],
    queryFn: () => focusApi.getToday(),
  });

  // Active timer ticker
  useEffect(() => {
    let interval: any = null;
    if (isRunning) {
      interval = setInterval(() => {
        if (isDistracted) {
          setDistractedSeconds((prev) => prev + 1);
        } else {
          setProductiveSeconds((prev) => prev + 1);
        }
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRunning, isDistracted]);

  const startMutation = useMutation({
    mutationFn: (taskId?: string) => focusApi.start(taskId || undefined),
    onSuccess: (session) => {
      setActiveSessionId(session.id);
      setIsRunning(true);
      setIsDistracted(false);
    },
  });

  const finishMutation = useMutation({
    mutationFn: (data: { markTaskCompleted: boolean }) => {
      if (!activeSessionId) throw new Error('No active session');
      return focusApi.finish(activeSessionId, {
        productive_seconds: productiveSeconds,
        distracted_seconds: distractedSeconds,
        mark_task_completed: data.markTaskCompleted,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['focus_today'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['productivity'] });
      setIsRunning(false);
      setIsDistracted(false);
      setProductiveSeconds(0);
      setDistractedSeconds(0);
      setActiveSessionId(null);
    },
  });

  const handleStart = async () => {
    await startMutation.mutateAsync(selectedTaskId || undefined);
  };

  const handleStop = () => {
    setIsRunning(false);
    setCompleteModalOpen(true);
  };

  const formatTimer = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const selectedTask = tasks.find((t) => t.id === selectedTaskId);

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-slate-100 tracking-tight">Focus & Attention Tracker</h1>
        <p className="text-sm text-slate-400">
          Measure true execution effort versus distractions with structured focus blocks.
        </p>
      </div>

      {/* Main Timer Display */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-3xl p-8 md:p-12 text-center shadow-2xl backdrop-blur-md relative overflow-hidden">
        {/* Glow ambient */}
        <div className={`absolute -top-24 left-1/2 -translate-x-1/2 w-72 h-72 rounded-full blur-3xl transition-all duration-700 pointer-events-none ${
          isRunning
            ? isDistracted
              ? 'bg-amber-500/20'
              : 'bg-brand-500/25'
            : 'bg-slate-700/10'
        }`} />

        {/* Task Selector */}
        {!isRunning && (
          <div className="max-w-md mx-auto mb-8">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Working on Task:
            </label>
            <select
              value={selectedTaskId}
              onChange={(e) => setSelectedTaskId(e.target.value)}
              className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-200 focus:outline-none focus:border-brand-500"
            >
              <option value="">General Focus / No Task</option>
              {tasks.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.title} ({t.priority})
                </option>
              ))}
            </select>
          </div>
        )}

        {isRunning && selectedTask && (
          <div className="mb-6 inline-flex items-center space-x-2 px-4 py-1.5 bg-brand-500/10 border border-brand-500/20 rounded-full text-xs text-brand-300 font-semibold">
            <span>Working on: {selectedTask.title}</span>
          </div>
        )}

        {/* Big Timer */}
        <div className="my-6">
          <div className="font-mono text-6xl md:text-8xl font-black text-slate-100 tracking-tighter">
            {formatTimer(productiveSeconds)}
          </div>
          <div className="flex items-center justify-center space-x-2 text-xs font-semibold uppercase tracking-wider text-slate-500 mt-2">
            <span className={`w-2 h-2 rounded-full ${isRunning ? (isDistracted ? 'bg-amber-400 animate-ping' : 'bg-emerald-400 animate-pulse') : 'bg-slate-600'}`} />
            <span>
              {!isRunning ? 'Ready to Start' : isDistracted ? 'Distraction Logged' : 'Focus Mode Active'}
            </span>
          </div>
        </div>

        {/* Timer Controls */}
        <div className="flex items-center justify-center gap-4 mt-8">
          {!isRunning ? (
            <button
              onClick={handleStart}
              className="px-8 py-3.5 bg-brand-600 hover:bg-brand-500 text-white font-bold text-base rounded-2xl shadow-xl shadow-brand-500/30 hover:shadow-brand-500/50 flex items-center space-x-2.5 transition-all cursor-pointer group"
            >
              <Play className="w-5 h-5 fill-current transition-transform group-hover:scale-110" />
              <span>Start Focus Session</span>
            </button>
          ) : (
            <>
              <button
                onClick={() => setIsDistracted(!isDistracted)}
                className={`px-5 py-3 rounded-2xl border text-xs font-bold transition-all cursor-pointer flex items-center space-x-2 ${
                  isDistracted
                    ? 'bg-amber-500 text-slate-950 border-amber-400'
                    : 'bg-slate-800 hover:bg-slate-700 text-amber-300 border-slate-700'
                }`}
              >
                <AlertCircle className="w-4 h-4" />
                <span>{isDistracted ? 'Back to Focus' : "I'm Distracted"}</span>
              </button>

              <button
                onClick={handleStop}
                className="px-6 py-3 bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs rounded-2xl shadow-lg shadow-rose-600/30 flex items-center space-x-2 transition-all cursor-pointer"
              >
                <Square className="w-4 h-4 fill-current" />
                <span>End Session</span>
              </button>
            </>
          )}
        </div>

        {/* Live Distraction Counter */}
        {isRunning && distractedSeconds > 0 && (
          <p className="text-xs text-amber-400/80 mt-4">
            Distracted time recorded: {formatTimer(distractedSeconds)}
          </p>
        )}
      </div>

      {/* Today's Summary Row */}
      {todaySummary && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 text-center">
            <div className="text-xs text-slate-400 uppercase font-semibold">Total Focused Today</div>
            <div className="text-2xl font-bold text-slate-100 mt-1">
              {Math.round(todaySummary.focus_seconds / 60)} mins
            </div>
          </div>
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 text-center">
            <div className="text-xs text-slate-400 uppercase font-semibold">Sessions Completed</div>
            <div className="text-2xl font-bold text-brand-400 mt-1">
              {todaySummary.total_sessions}
            </div>
          </div>
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 text-center">
            <div className="text-xs text-slate-400 uppercase font-semibold">Focus Ratio</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">
              {todaySummary.focus_ratio}%
            </div>
          </div>
        </div>
      )}

      {/* Completion Review Modal */}
      <FocusCompleteModal
        isOpen={completeModalOpen}
        productiveSeconds={productiveSeconds}
        distractedSeconds={distractedSeconds}
        taskTitle={selectedTask?.title}
        onClose={() => setCompleteModalOpen(false)}
        onConfirm={async (markTaskCompleted) => {
          await finishMutation.mutateAsync({ markTaskCompleted });
        }}
      />
    </div>
  );
}
