import { UserSkill } from '@/services/api/skills';
import { X, ShieldCheck, History, Calendar, Award } from 'lucide-react';
import { formatDateTime } from '@/lib/utils';

interface SkillDetailModalProps {
  isOpen: boolean;
  skill: UserSkill | null;
  onClose: () => void;
}

export function SkillDetailModal({ isOpen, skill, onClose }: SkillDetailModalProps) {
  if (!isOpen || !skill) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-2xl max-h-[85vh] overflow-y-auto shadow-2xl p-6 space-y-6 animate-in fade-in zoom-in-95">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-brand-400">
              {skill.category || 'Skill'}
            </span>
            <h2 className="text-xl font-bold text-slate-100 mt-1">{skill.name}</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Score & Confidence Overview */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-4 bg-slate-950/60 border border-slate-800 rounded-2xl">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Strength</div>
            <div className="text-2xl font-bold text-brand-400 mt-0.5">{skill.level} / 100</div>
          </div>
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Confidence</div>
            <div className="text-2xl font-bold text-emerald-400 mt-0.5">{Math.round(skill.confidence * 100)}%</div>
          </div>
          <div className="col-span-2 sm:col-span-1">
            <div className="text-xs text-slate-400 font-semibold uppercase">Total Records</div>
            <div className="text-2xl font-bold text-sky-400 mt-0.5">{skill.evidence_count}</div>
          </div>
        </div>

        {/* Evidence Provenance Timeline */}
        <div className="space-y-3">
          <h4 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-brand-400" />
            <span>Verifiable Evidence Trail</span>
          </h4>
          {skill.recent_evidence.length === 0 ? (
            <p className="text-xs text-slate-500 italic p-3 bg-slate-950/40 rounded-xl">
              No evidence recorded yet. Complete linked tasks or add manual projects to build strength.
            </p>
          ) : (
            <div className="space-y-2">
              {skill.recent_evidence.map((e) => (
                <div key={e.id} className="p-3 bg-slate-950/50 border border-slate-800/80 rounded-xl space-y-1">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-bold text-brand-300 uppercase tracking-wide">
                      {e.source_type} (+{e.strength} pts)
                    </span>
                    <span className="text-slate-500">{formatDateTime(e.occurred_at)}</span>
                  </div>
                  <p className="text-xs text-slate-300">{e.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Historical Score Adjustments */}
        <div className="space-y-3">
          <h4 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <History className="w-4 h-4 text-sky-400" />
            <span>Evaluation History</span>
          </h4>
          <div className="space-y-1.5">
            {skill.history.map((h, idx) => (
              <div key={idx} className="flex items-center justify-between text-xs p-2.5 bg-slate-950/30 rounded-xl border border-slate-850">
                <span className="text-slate-400">{h.reason || 'Assessed'}</span>
                <span className="font-semibold text-slate-200">Score: {h.level}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
