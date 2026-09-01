import { SkillGapReport, SkillGapItem } from '@/services/api/learning';
import { Target, AlertTriangle, CheckCircle2, Sparkles, ArrowRight } from 'lucide-react';

interface SkillGapScannerProps {
  report: SkillGapReport;
  onGenerateRoadmap: () => void;
  generatingRoadmap: boolean;
}

export function SkillGapScanner({ report, onGenerateRoadmap, generatingRoadmap }: SkillGapScannerProps) {
  const severityBadge = {
    CRITICAL: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    IMPORTANT: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    MODERATE: 'bg-sky-500/10 text-sky-400 border-sky-500/20',
    MINOR: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 md:p-8 space-y-6 shadow-sm">
      {/* Top Target Role & Readiness Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-800/80">
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
            <Target className="w-4 h-4" />
            <span>Target Role Evaluation</span>
          </div>
          <h2 className="text-2xl font-bold text-slate-100">{report.role_name}</h2>
          <p className="text-xs text-slate-400">
            Comparing your real skill evidence against verified role requirements.
          </p>
        </div>

        {/* Readiness Meter */}
        <div className="flex items-center space-x-6 shrink-0 bg-slate-950/60 border border-slate-800 p-4 rounded-2xl">
          <div>
            <div className="text-[11px] text-slate-400 uppercase font-semibold">Overall Readiness</div>
            <div className="text-3xl font-black text-brand-400 mt-0.5">{report.overall_readiness}%</div>
          </div>
          <div className="border-l border-slate-800 pl-4 space-y-1 text-xs">
            <div className="text-rose-400 font-semibold">{report.critical_gaps} Critical Gaps</div>
            <div className="text-slate-400">{report.total_gaps} Total Gaps</div>
          </div>
        </div>
      </div>

      {/* Gaps Table / Cards */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200">Identified Skill Gaps</h3>
          <button
            onClick={onGenerateRoadmap}
            disabled={generatingRoadmap}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer disabled:opacity-50"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{generatingRoadmap ? 'Synthesizing Roadmap...' : 'Build Learning Roadmap'}</span>
          </button>
        </div>

        <div className="divide-y divide-slate-800/60 bg-slate-950/50 border border-slate-800/80 rounded-2xl overflow-hidden">
          {report.gaps.map((gap) => (
            <div key={gap.skill_id} className="p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-950/80 transition-colors">
              <div className="space-y-1 min-w-0">
                <div className="flex items-center space-x-2.5">
                  <span className="font-bold text-sm text-slate-200">{gap.skill_name}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase border ${severityBadge[gap.severity]}`}>
                    {gap.severity}
                  </span>
                  <span className="text-[10px] text-slate-500 uppercase">Weight: {gap.importance}</span>
                </div>
                <p className="text-xs text-slate-400">{gap.recommended_action}</p>
              </div>

              <div className="flex items-center space-x-6 shrink-0">
                <div className="text-right">
                  <div className="text-xs text-slate-400 font-medium">
                    Current: <span className="text-slate-200 font-bold">{gap.current_level}</span> / Req: <span className="text-brand-300 font-bold">{gap.required_level}</span>
                  </div>
                  <div className={`text-xs font-bold mt-0.5 ${gap.gap > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                    {gap.gap > 0 ? `-${gap.gap} pts gap` : '✓ Satisfied'}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
