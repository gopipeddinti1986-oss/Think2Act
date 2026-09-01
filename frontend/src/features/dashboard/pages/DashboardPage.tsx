import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { dashboardApi } from '@/services/api/dashboard';
import { tasksApi } from '@/services/api/tasks';
import { OverviewCards } from '../components/OverviewCards';
import { NextActionCard } from '../components/NextActionCard';
import { TodayTasksCard } from '../components/TodayTasksCard';
import { Sparkles, Target, ArrowRight, Plus } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

export function DashboardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: dashboard, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => dashboardApi.getSummary(),
  });

  const completeMutation = useMutation({
    mutationFn: (taskId: string) => tasksApi.complete(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  if (isLoading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-8 bg-slate-900 rounded-lg w-64" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-28 bg-slate-900 rounded-2xl" />
          ))}
        </div>
        <div className="h-40 bg-slate-900 rounded-2xl" />
      </div>
    );
  }

  if (error || !dashboard) {
    return (
      <div className="p-8 text-center bg-slate-900/50 border border-slate-800 rounded-2xl">
        <h2 className="text-lg font-bold text-slate-200">Unable to load dashboard</h2>
        <p className="text-sm text-slate-400 mt-1">Please ensure the backend service is running.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Top Greeting */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
            Good day, {dashboard.user?.name || user?.name} 👋
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Here is what matters for your execution and career momentum today.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => navigate('/goals')}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-850 border border-slate-800 text-slate-200 text-xs font-semibold rounded-xl flex items-center space-x-2 transition-colors cursor-pointer"
          >
            <Target className="w-3.5 h-3.5" />
            <span>Manage Goals</span>
          </button>
          <button
            onClick={() => navigate('/tasks')}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl flex items-center space-x-2 shadow-lg shadow-brand-500/20 transition-all cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New Task</span>
          </button>
        </div>
      </div>

      {/* 1. Hero Next Action Card */}
      <NextActionCard
        task={dashboard.next_action}
        onStartFocus={() => navigate('/focus')}
      />

      {/* 2. Overview Metrics Cards */}
      <OverviewCards
        summary={dashboard.tasks_summary}
        productivityScore={dashboard.productivity_score}
        focusMinutes={dashboard.focus_minutes_today}
        readinessScore={dashboard.readiness_score}
      />

      {/* 3. Two-Column Layout: Today's Tasks & Active Goals */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Today's Priority Tasks (7 cols) */}
        <div className="lg:col-span-7">
          <TodayTasksCard
            tasks={dashboard.today_tasks}
            onComplete={(id) => completeMutation.mutate(id)}
          />
        </div>

        {/* Right Column: Goals & AI Coach Suggestions (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          {/* Active Goals Summary */}
          <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-sm shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-slate-100">Active Goals</h3>
                <p className="text-xs text-slate-500">Your high-level roadmap</p>
              </div>
              <button
                onClick={() => navigate('/goals')}
                className="text-xs font-semibold text-brand-400 hover:text-brand-300 flex items-center space-x-1"
              >
                <span>View All</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            {dashboard.goals.length === 0 ? (
              <div className="py-6 text-center border border-dashed border-slate-800 rounded-xl">
                <p className="text-xs text-slate-400">No active goals set</p>
                <button
                  onClick={() => navigate('/goals')}
                  className="mt-2 text-xs font-semibold text-brand-400 hover:underline"
                >
                  + Set a Career/Learning Goal
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                {dashboard.goals.map((goal) => (
                  <div
                    key={goal.id}
                    className="p-3 bg-slate-950/40 border border-slate-800/60 rounded-xl flex items-center justify-between"
                  >
                    <div>
                      <h4 className="text-sm font-semibold text-slate-200">{goal.title}</h4>
                      <p className="text-xs text-slate-500 mt-0.5">{goal.category || 'General'}</p>
                    </div>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 uppercase">
                      {goal.priority}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* AI Coach Suggestion Widget */}
          {dashboard.ai_suggestion && (
            <div className="bg-gradient-to-br from-slate-900 via-slate-900 to-brand-950/30 border border-brand-500/25 rounded-2xl p-5 relative overflow-hidden">
              <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider mb-2">
                <Sparkles className="w-3.5 h-3.5" />
                <span>AI Insight</span>
              </div>
              <h4 className="text-sm font-bold text-slate-100">{dashboard.ai_suggestion.title}</h4>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                {dashboard.ai_suggestion.message}
              </p>
              {dashboard.ai_suggestion.action_label && (
                <button
                  onClick={() => navigate('/tasks')}
                  className="mt-3 px-3 py-1.5 bg-brand-600/30 hover:bg-brand-600/50 border border-brand-500/40 rounded-lg text-xs font-semibold text-brand-200 transition-colors"
                >
                  {dashboard.ai_suggestion.action_label}
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
