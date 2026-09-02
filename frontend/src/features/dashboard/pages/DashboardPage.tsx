import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { dashboardApi } from '@/services/api/dashboard';
import { tasksApi } from '@/services/api/tasks';
import { goalsApi } from '@/services/api/goals';
import { Task, Goal } from '@/types';
import { TaskDetailModal } from '@/features/tasks/components/TaskDetailModal';
import { TaskModal } from '@/features/tasks/components/TaskModal';
import { 
  Sparkles, 
  CheckCircle2, 
  Circle, 
  Play, 
  Calendar, 
  Clock, 
  Target, 
  Plus, 
  ArrowRight, 
  Briefcase,
  TrendingUp
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

export function DashboardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [createTaskOpen, setCreateTaskOpen] = useState(false);

  const { data: dashboard, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => dashboardApi.getSummary(),
  });

  const { data: goals = [] } = useQuery({
    queryKey: ['goals'],
    queryFn: () => goalsApi.list(),
  });

  const completeMutation = useMutation({
    mutationFn: (taskId: string) => tasksApi.complete(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const createTaskMutation = useMutation({
    mutationFn: (data: any) => tasksApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      setCreateTaskOpen(false);
    },
  });

  // Skeleton Loading State
  if (isLoading) {
    return (
      <div className="space-y-6 animate-pulse max-w-5xl mx-auto">
        <div className="h-10 bg-slate-900 rounded-xl w-72" />
        <div className="h-36 bg-slate-900 rounded-3xl" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-64 bg-slate-900 rounded-3xl" />
          <div className="h-64 bg-slate-900 rounded-3xl" />
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="h-44 bg-slate-900 rounded-3xl" />
          <div className="h-44 bg-slate-900 rounded-3xl" />
          <div className="h-44 bg-slate-900 rounded-3xl" />
        </div>
      </div>
    );
  }

  // Error State
  if (error || !dashboard) {
    return (
      <div className="p-8 text-center bg-slate-900/60 border border-slate-800 rounded-3xl max-w-xl mx-auto my-12 space-y-4">
        <h3 className="text-lg font-bold text-slate-100">Something went wrong.</h3>
        <p className="text-sm text-slate-400">Could not retrieve your dashboard summary right now.</p>
        <button
          onClick={() => queryClient.invalidateQueries({ queryKey: ['dashboard'] })}
          className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl transition-colors cursor-pointer"
        >
          Try Again
        </button>
      </div>
    );
  }

  const tasks = dashboard.today_tasks || [];
  const pendingCount = dashboard.tasks_summary?.pending || 0;
  const nextAction = dashboard.next_action;

  const priorityDot = (p: string) => {
    switch (p) {
      case 'URGENT':
      case 'HIGH':
        return <span className="text-rose-400">🔴</span>;
      case 'MEDIUM':
        return <span className="text-amber-400">🟡</span>;
      default:
        return <span className="text-emerald-400">🟢</span>;
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* 1. Header: Greeting & Important items count */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
            Good morning, {dashboard.user?.name || user?.name || 'there'}.
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            You have <span className="font-bold text-slate-200">{pendingCount}</span> important {pendingCount === 1 ? 'thing' : 'things'} today.
          </p>
        </div>

        <button
          onClick={() => setCreateTaskOpen(true)}
          className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer shrink-0 self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>+ New Task</span>
        </button>
      </div>

      {/* 2. Recommended Next Action Card */}
      <div className="p-6 bg-gradient-to-r from-slate-900 via-slate-900 to-brand-950/40 border border-brand-500/30 rounded-3xl shadow-xl relative overflow-hidden space-y-4">
        <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
          <Sparkles className="w-4 h-4 text-brand-400 animate-pulse" />
          <span>Recommended next action</span>
        </div>

        <div>
          <h2 className="text-xl font-bold text-slate-100">
            {nextAction ? nextAction.title : dashboard.ai_suggestion?.title || 'Plan your next focus block'}
          </h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
            {nextAction
              ? (nextAction.description || `Highest priority task with ${nextAction.estimated_minutes} min estimate.`)
              : (dashboard.ai_suggestion?.message || 'Create tasks aligned with your target role to build momentum.')}
          </p>
        </div>

        <div className="flex items-center space-x-3 pt-1">
          <button
            onClick={() => navigate('/focus')}
            className="px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 shadow-md shadow-brand-500/25 transition-all cursor-pointer"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Start Focus</span>
          </button>
          <button
            onClick={() => navigate('/planner')}
            className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-xl flex items-center space-x-2 transition-colors cursor-pointer"
          >
            <Calendar className="w-3.5 h-3.5" />
            <span>Schedule</span>
          </button>
        </div>
      </div>

      {/* 3. Grid: Today's Tasks & Today's Schedule */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Today's Tasks Card (7 cols) */}
        <div className="lg:col-span-7 bg-slate-900/70 border border-slate-800 rounded-3xl p-6 space-y-4 shadow-sm">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-100">Today's Tasks</h3>
            <button
              onClick={() => navigate('/tasks')}
              className="text-xs font-semibold text-brand-400 hover:text-brand-300 flex items-center space-x-1"
            >
              <span>View All</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          {tasks.length === 0 ? (
            <div className="py-10 text-center border border-dashed border-slate-800 rounded-2xl p-6 space-y-3">
              <p className="text-xs text-slate-400">
                You don't have any tasks yet. Create your first task to get started.
              </p>
              <button
                onClick={() => setCreateTaskOpen(true)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-xl transition-colors cursor-pointer inline-flex items-center space-x-1.5"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>+ New Task</span>
              </button>
            </div>
          ) : (
            <div className="divide-y divide-slate-800/80 bg-slate-950/50 rounded-2xl border border-slate-800/80 overflow-hidden">
              {tasks.map((task) => {
                const isDone = task.status === 'COMPLETED';
                return (
                  <div
                    key={task.id}
                    onClick={() => setSelectedTask(task)}
                    className="p-3.5 flex items-center justify-between hover:bg-slate-900/60 transition-colors cursor-pointer group"
                  >
                    <div className="flex items-center space-x-3 min-w-0">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          if (!isDone) completeMutation.mutate(task.id);
                        }}
                        className="p-0.5 text-slate-500 hover:text-brand-400 transition-colors cursor-pointer shrink-0"
                      >
                        {isDone ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        ) : (
                          <Circle className="w-4 h-4 text-slate-500 hover:text-brand-400" />
                        )}
                      </button>

                      <div className="flex items-center space-x-2 min-w-0">
                        <span className="text-xs shrink-0">{priorityDot(task.priority)}</span>
                        <span className={`text-xs font-semibold truncate ${isDone ? 'line-through text-slate-500' : 'text-slate-200 group-hover:text-brand-300'}`}>
                          {task.title}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3 text-[11px] text-slate-400 shrink-0 ml-3">
                      {task.category && (
                        <span className="hidden sm:inline-block px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                          {task.category}
                        </span>
                      )}
                      <span>{task.estimated_minutes}m</span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Today's Schedule Card (5 cols) */}
        <div className="lg:col-span-5 bg-slate-900/70 border border-slate-800 rounded-3xl p-6 space-y-4 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-slate-100">Today's Schedule</h3>
              <button
                onClick={() => navigate('/planner')}
                className="text-xs font-semibold text-brand-400 hover:text-brand-300 flex items-center space-x-1"
              >
                <span>Planner</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            <div className="space-y-3">
              <div className="flex items-center space-x-3 text-xs p-2.5 bg-slate-950/40 rounded-xl border border-slate-800/80">
                <span className="font-mono text-brand-400 font-bold">09:00</span>
                <span className="text-slate-500">──</span>
                <span className="text-slate-300 font-medium">Core Execution Sprint</span>
              </div>
              <div className="flex items-center space-x-3 text-xs p-2.5 bg-slate-950/40 rounded-xl border border-slate-800/80">
                <span className="font-mono text-brand-400 font-bold">14:00</span>
                <span className="text-slate-500">──</span>
                <span className="text-slate-300 font-medium">Project Architecture Build</span>
              </div>
              <div className="flex items-center space-x-3 text-xs p-2.5 bg-slate-950/40 rounded-xl border border-slate-800/80">
                <span className="font-mono text-brand-400 font-bold">19:00</span>
                <span className="text-slate-500">──</span>
                <span className="text-slate-300 font-medium">Skill Gap Practice</span>
              </div>
            </div>
          </div>

          <p className="text-[11px] text-slate-500 mt-2">
            Build and lock custom time blocks in Daily Planner.
          </p>
        </div>
      </div>

      {/* 4. Bottom 3-Card Row: Focus Today | Progress | Career Snapshot */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Focus Today Card */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 space-y-4 shadow-sm flex flex-col justify-between">
          <div className="space-y-1">
            <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
              <Clock className="w-4 h-4" />
              <span>Focus Today</span>
            </div>
            <div className="text-3xl font-black text-slate-100 pt-2">
              {Math.floor((dashboard.focus_minutes_today || 0) / 60)}h {(dashboard.focus_minutes_today || 0) % 60}m
            </div>
            <p className="text-xs text-emerald-400 font-semibold pt-1">
              ↑ 18% vs yesterday
            </p>
          </div>

          <button
            onClick={() => navigate('/focus')}
            className="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl flex items-center justify-center space-x-1.5 shadow-md shadow-brand-500/20 transition-all cursor-pointer"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Start Focus</span>
          </button>
        </div>

        {/* Progress Card */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 space-y-4 shadow-sm flex flex-col justify-between">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-brand-400 uppercase tracking-wider">Progress</span>
              <span className="text-xs font-bold text-slate-200">
                Productivity: {dashboard.productivity_score || 78} / 100
              </span>
            </div>

            {/* ASCII Progress bars */}
            <div className="space-y-2 text-xs">
              <div>
                <div className="flex justify-between text-[11px] text-slate-400 mb-1">
                  <span>Tasks</span>
                  <span>{dashboard.tasks_summary?.completion_rate || 80}%</span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div style={{ width: `${dashboard.tasks_summary?.completion_rate || 80}%` }} className="h-full bg-brand-500 rounded-full" />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-[11px] text-slate-400 mb-1">
                  <span>Focus</span>
                  <span>70%</span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div style={{ width: '70%' }} className="h-full bg-emerald-500 rounded-full" />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-[11px] text-slate-400 mb-1">
                  <span>Distraction</span>
                  <span>20%</span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div style={{ width: '20%' }} className="h-full bg-rose-500/80 rounded-full" />
                </div>
              </div>
            </div>
          </div>

          <button
            onClick={() => navigate('/progress')}
            className="text-xs font-bold text-brand-400 hover:text-brand-300 flex items-center space-x-1"
          >
            <span>View detailed progress →</span>
          </button>
        </div>

        {/* Career Snapshot Card */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 space-y-4 shadow-sm flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
              <Briefcase className="w-4 h-4" />
              <span>Career Snapshot</span>
            </div>
            <div className="pt-1">
              <div className="text-xs text-slate-400 font-semibold">Target: <span className="text-slate-200">Backend Software Engineer</span></div>
              <div className="text-lg font-black text-brand-400 mt-1">Readiness: {dashboard.readiness_score || 72}%</div>
              <p className="text-xs text-amber-400 font-semibold mt-1">
                Top Skill Gap: Docker (38 → 65)
              </p>
            </div>
          </div>

          <button
            onClick={() => navigate('/learning')}
            className="w-full py-2.5 bg-slate-800 hover:bg-slate-750 text-slate-200 text-xs font-bold rounded-xl transition-colors cursor-pointer"
          >
            View Skill Gaps
          </button>
        </div>
      </div>

      {/* 5. Think2Act AI Card */}
      <div className="p-6 bg-slate-900/70 border border-slate-800 rounded-3xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
        <div className="space-y-1">
          <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-4 h-4" />
            <span>Think2Act AI</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed italic">
            "{dashboard.ai_suggestion?.message || 'Your execution velocity peaks in 45-minute morning sessions. Keep high-leverage tasks scheduled early.'}"
          </p>
        </div>

        <button
          onClick={() => navigate('/ai')}
          className="px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl shadow-md shadow-brand-500/25 transition-all cursor-pointer shrink-0"
        >
          Analyze
        </button>
      </div>

      {/* Task Details Modal */}
      <TaskDetailModal
        task={selectedTask}
        isOpen={!!selectedTask}
        onClose={() => setSelectedTask(null)}
        onComplete={async (id) => {
          await completeMutation.mutateAsync(id);
        }}
      />

      {/* Create Task Modal */}
      <TaskModal
        isOpen={createTaskOpen}
        goals={goals}
        onClose={() => setCreateTaskOpen(false)}
        onSubmit={async (data) => {
          await createTaskMutation.mutateAsync(data);
        }}
      />
    </div>
  );
}
