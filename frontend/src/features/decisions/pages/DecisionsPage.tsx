import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { decisionsApi, Decision } from '@/services/api/decisions';
import { 
  Scale, 
  Sparkles, 
  CheckCircle2, 
  ArrowRight, 
  Plus, 
  Sliders, 
  Award,
  Layers
} from 'lucide-react';

export function DecisionsPage() {
  const queryClient = useQueryClient();

  const { data: decisions = [], isLoading } = useQuery({
    queryKey: ['decisions'],
    queryFn: () => decisionsApi.list(),
  });

  const activeDecision = decisions[0];

  const updateScoreMutation = useMutation({
    mutationFn: ({ optionId, criterionId, score }: { optionId: string; criterionId: string; score: number }) => {
      if (!activeDecision) throw new Error('No active decision');
      return decisionsApi.updateScore(activeDecision.id, {
        option_id: optionId,
        criterion_id: criterionId,
        score,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['decisions'] });
    },
  });

  if (isLoading || !activeDecision) {
    return (
      <div className="space-y-6 animate-pulse max-w-5xl">
        <div className="h-10 bg-slate-900 rounded-xl w-64" />
        <div className="h-44 bg-slate-900 rounded-3xl" />
        <div className="h-64 bg-slate-900 rounded-3xl" />
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <Scale className="w-6 h-6 text-brand-400" />
            <span>Decision Simulator</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Deterministic multi-factor criteria evaluation with transparent weighted scoring algorithms.
          </p>
        </div>
      </div>

      {/* Decision Header */}
      <div className="p-6 bg-slate-900/80 border border-slate-800 rounded-3xl space-y-2 shadow-sm">
        <div className="flex items-center space-x-2 text-xs font-bold text-brand-400 uppercase tracking-wider">
          <Sparkles className="w-4 h-4" />
          <span>Strategic Decision Framework</span>
        </div>
        <h2 className="text-xl font-bold text-slate-100">{activeDecision.title}</h2>
        <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">
          {activeDecision.description}
        </p>
      </div>

      {/* Decision Options Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {activeDecision.options.map((opt, idx) => {
          const isLeader = idx === 0 || opt.total_score >= 8.0;
          return (
            <div
              key={opt.id}
              className={`p-6 rounded-3xl border flex flex-col justify-between space-y-6 transition-all ${
                isLeader
                  ? 'bg-slate-900/90 border-brand-500/40 shadow-xl'
                  : 'bg-slate-900/60 border-slate-800'
              }`}
            >
              <div className="space-y-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    {isLeader && (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 uppercase">
                        Recommended Choice
                      </span>
                    )}
                    <h3 className="text-base font-bold text-slate-100 mt-1.5">{opt.name}</h3>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="text-2xl font-black text-brand-400">{opt.total_score}</div>
                    <span className="text-[9px] font-bold text-slate-500 uppercase">Weighted Score</span>
                  </div>
                </div>

                {/* Criteria Scoring Sliders */}
                <div className="space-y-3 pt-2 border-t border-slate-800/80">
                  {activeDecision.criteria.map((crit) => {
                    const existingScore = opt.scores.find((s) => s.criterion_id === crit.id)?.score || 7.0;
                    return (
                      <div key={crit.id} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-300 font-medium">{crit.name}</span>
                          <span className="text-slate-400 font-bold">{existingScore}/10</span>
                        </div>
                        <input
                          type="range"
                          min="1"
                          max="10"
                          step="0.5"
                          value={existingScore}
                          onChange={(e) => updateScoreMutation.mutate({
                            optionId: opt.id,
                            criterionId: crit.id,
                            score: parseFloat(e.target.value)
                          })}
                          className="w-full accent-brand-500 h-1 bg-slate-950 rounded-lg cursor-pointer"
                        />
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800/80 text-center">
                <span className="text-[11px] text-slate-400">
                  Criteria Weighted Factor: <span className="font-bold text-slate-200">100% Deterministic</span>
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
