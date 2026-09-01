import { LearningPath, LearningPathItem } from '@/services/api/learning';
import { BookOpen, CheckCircle2, ArrowRight, ExternalLink, Play, Clock, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface RoadmapViewProps {
  path: LearningPath;
  onConvertToTask: (itemId: string) => Promise<void>;
  onCompleteItem: (itemId: string) => Promise<void>;
}

export function RoadmapView({ path, onConvertToTask, onCompleteItem }: RoadmapViewProps) {
  const navigate = useNavigate();

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 md:p-8 space-y-6 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
            <BookOpen className="w-4 h-4" />
            <span>Active Learning Roadmap</span>
          </div>
          <h2 className="text-xl font-bold text-slate-100 mt-1">{path.title}</h2>
        </div>

        <span className="px-3 py-1 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 text-xs font-semibold uppercase">
          {path.items.length} Milestones
        </span>
      </div>

      <div className="space-y-4">
        {path.items.map((item, idx) => {
          const isDone = item.status === 'COMPLETED';
          const inProgress = item.status === 'IN_PROGRESS';

          return (
            <div
              key={item.id}
              className={`p-5 rounded-2xl border transition-all flex flex-col md:flex-row md:items-center justify-between gap-4 ${
                isDone
                  ? 'bg-slate-950/40 border-slate-900 opacity-75'
                  : inProgress
                  ? 'bg-slate-900 border-brand-500/30 shadow-md shadow-brand-950/20'
                  : 'bg-slate-950/60 border-slate-800/80 hover:border-slate-700'
              }`}
            >
              <div className="flex items-start space-x-3.5 min-w-0">
                <div className={`w-7 h-7 rounded-xl flex items-center justify-center shrink-0 text-xs font-bold ${
                  isDone ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-300'
                }`}>
                  {isDone ? <CheckCircle2 className="w-4 h-4" /> : idx + 1}
                </div>

                <div className="space-y-1 min-w-0">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold text-brand-300 uppercase tracking-wide">
                      {item.skill_name || 'Skill Milestone'}
                    </span>
                    {inProgress && (
                      <span className="text-[10px] px-2 py-0.5 rounded bg-brand-500/20 text-brand-300 font-semibold uppercase animate-pulse">
                        In Progress
                      </span>
                    )}
                  </div>

                  <h4 className={`text-sm font-bold ${isDone ? 'line-through text-slate-500' : 'text-slate-100'}`}>
                    {item.title}
                  </h4>

                  {item.resource && (
                    <div className="flex items-center space-x-2 text-xs text-slate-400 pt-1">
                      <span>Curated: {item.resource.title}</span>
                      {item.resource.url && (
                        <a
                          href={item.resource.url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-brand-400 hover:text-brand-300 inline-flex items-center space-x-0.5"
                        >
                          <ExternalLink className="w-3 h-3 ml-1" />
                        </a>
                      )}
                    </div>
                  )}
                </div>
              </div>

              <div className="flex items-center space-x-3 shrink-0">
                {!isDone && !inProgress && (
                  <button
                    onClick={() => onConvertToTask(item.id)}
                    className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl flex items-center space-x-1.5 transition-colors cursor-pointer"
                  >
                    <span>Create Task</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                )}

                {!isDone && inProgress && (
                  <>
                    <button
                      onClick={() => navigate('/focus')}
                      className="px-3.5 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl flex items-center space-x-1.5 transition-colors cursor-pointer"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>Start Focus</span>
                    </button>
                    <button
                      onClick={() => onCompleteItem(item.id)}
                      className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-xl transition-colors cursor-pointer"
                    >
                      Mark Done
                    </button>
                  </>
                )}

                {isDone && (
                  <span className="text-xs font-semibold text-emerald-400 flex items-center space-x-1">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Evidence Recorded</span>
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
