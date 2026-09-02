import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { resumeApi } from '@/services/api/resume';
import { 
  FileText, 
  Sparkles, 
  CheckCircle2, 
  ArrowRight, 
  Layers, 
  Zap,
  TrendingUp,
  AlertCircle
} from 'lucide-react';

export function ResumePage() {
  const queryClient = useQueryClient();

  const { data: resumes = [], isLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: () => resumeApi.list(),
  });

  const activeResume = resumes[0];

  const applyMutation = useMutation({
    mutationFn: (suggestionId: string) => {
      if (!activeResume) throw new Error('No resume loaded');
      return resumeApi.applySuggestion(activeResume.id, suggestionId);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
    },
  });

  if (isLoading || !activeResume) {
    return (
      <div className="space-y-6 animate-pulse max-w-5xl">
        <div className="h-10 bg-slate-900 rounded-xl w-64" />
        <div className="h-36 bg-slate-900 rounded-3xl" />
        <div className="h-64 bg-slate-900 rounded-3xl" />
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <FileText className="w-6 h-6 text-brand-400" />
            <span>Resume & ATS Optimizer</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Grounded resume enhancement backed by real execution evidence and market ATS benchmarks.
          </p>
        </div>
      </div>

      {/* Top ATS Score Hero Card */}
      <div className="p-8 bg-gradient-to-br from-slate-900 via-slate-900 to-brand-950/40 border border-brand-500/30 rounded-3xl shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-4 h-4" />
            <span>Target Role Alignment</span>
          </div>
          <h2 className="text-xl font-bold text-slate-100">{activeResume.title}</h2>
          <p className="text-xs text-slate-400">
            Targeting: <span className="font-semibold text-slate-200">{activeResume.target_role}</span>
          </p>
        </div>

        <div className="flex items-center space-x-4 bg-slate-950/60 border border-slate-800 rounded-2xl p-4 shrink-0">
          <div className="text-center">
            <div className="text-3xl font-black text-brand-400">{Math.round(activeResume.ats_score)}/100</div>
            <p className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">ATS Score</p>
          </div>
        </div>
      </div>

      {/* 2-Column: Live Resume Sections & ATS Suggestions */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Parsed Resume Sections (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">Professional Summary</h3>
            <p className="text-xs text-slate-300 leading-relaxed p-4 bg-slate-950/50 border border-slate-850 rounded-2xl">
              {activeResume.parsed_sections?.summary || 'No summary configured.'}
            </p>

            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider pt-2">Experience Bullets</h3>
            <div className="space-y-2.5">
              {activeResume.parsed_sections?.experience?.map((exp, idx) => (
                <div key={idx} className="text-xs text-slate-300 p-3.5 bg-slate-950/50 border border-slate-850 rounded-2xl leading-relaxed">
                  • {exp}
                </div>
              ))}
            </div>

            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider pt-2">Verified Skill Stack</h3>
            <div className="flex flex-wrap gap-2">
              {activeResume.parsed_sections?.skills?.map((s, idx) => (
                <span key={idx} className="px-2.5 py-1 rounded-xl bg-slate-950 border border-slate-800 text-xs text-brand-300 font-semibold">
                  {s}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Right: AI ATS Improvement Recommendations (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">AI Impact Recommendations</h3>
            <span className="text-xs text-brand-400 font-bold">{activeResume.suggestions.length} available</span>
          </div>

          <div className="space-y-4">
            {activeResume.suggestions.map((sugg) => (
              <div
                key={sugg.id}
                className="p-5 bg-slate-900/80 border border-slate-800 rounded-3xl space-y-3 shadow-sm"
              >
                <div className="flex items-center justify-between text-[10px] font-bold">
                  <span className="px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 uppercase">
                    {sugg.suggestion_type}
                  </span>
                  <span className="text-slate-500 uppercase">{sugg.section}</span>
                </div>

                <div className="space-y-2 text-xs">
                  <div>
                    <span className="text-[10px] text-slate-500 uppercase font-bold">Current:</span>
                    <p className="text-slate-400 italic line-through mt-0.5">{sugg.current_text}</p>
                  </div>
                  <div>
                    <span className="text-[10px] text-emerald-400 uppercase font-bold">Optimized for ATS:</span>
                    <p className="text-slate-200 font-medium mt-0.5">{sugg.recommended_text}</p>
                  </div>
                </div>

                {sugg.impact_reason && (
                  <p className="text-[11px] text-slate-400 leading-relaxed bg-slate-950/40 p-2.5 rounded-xl border border-slate-850">
                    💡 {sugg.impact_reason}
                  </p>
                )}

                <div className="pt-2">
                  {!sugg.is_applied ? (
                    <button
                      onClick={() => applyMutation.mutate(sugg.id)}
                      className="w-full py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl shadow-md shadow-brand-500/20 transition-all cursor-pointer"
                    >
                      Apply Optimization (+8 ATS)
                    </button>
                  ) : (
                    <div className="text-center text-xs font-bold text-emerald-400 py-1">
                      Applied to Resume ✓
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
