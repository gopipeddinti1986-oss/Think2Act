import { UserSkill } from '@/services/api/skills';
import { Layers, ShieldCheck, Plus, Sparkles, ChevronRight } from 'lucide-react';

interface SkillCardProps {
  skill: UserSkill;
  onSelect: (skill: UserSkill) => void;
  onAddEvidence: (skill: UserSkill) => void;
}

export function SkillCard({ skill, onSelect, onAddEvidence }: SkillCardProps) {
  const confidenceLabel =
    skill.confidence >= 0.8 ? 'High Confidence' : skill.confidence >= 0.5 ? 'Medium Confidence' : 'Low Evidence';
  
  const confidenceColor =
    skill.confidence >= 0.8 ? 'text-emerald-400 border-emerald-500/20 bg-emerald-500/10' :
    skill.confidence >= 0.5 ? 'text-sky-400 border-sky-500/20 bg-sky-500/10' :
    'text-amber-400 border-amber-500/20 bg-amber-500/10';

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all flex flex-col justify-between group shadow-sm">
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
            {skill.category || 'General'}
          </span>
          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase ${confidenceColor}`}>
            {confidenceLabel}
          </span>
        </div>

        <div>
          <h3 className="text-base font-bold text-slate-100 group-hover:text-brand-300 transition-colors">
            {skill.name}
          </h3>
          <div className="flex items-center space-x-2 text-xs text-slate-400 mt-1">
            <span>{skill.evidence_count} evidence records</span>
          </div>
        </div>

        {/* Strength Progress Bar */}
        <div>
          <div className="flex items-center justify-between text-xs mb-1">
            <span className="text-slate-400">Calculated Strength</span>
            <span className="font-bold text-brand-400">{skill.level} / 100</span>
          </div>
          <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
            <div
              style={{ width: `${Math.min(100, skill.level)}%` }}
              className="h-full bg-gradient-to-r from-brand-600 to-indigo-400 rounded-full transition-all duration-500"
            />
          </div>
        </div>
      </div>

      <div className="pt-4 mt-4 border-t border-slate-800/80 flex items-center justify-between gap-2">
        <button
          onClick={() => onAddEvidence(skill)}
          className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium flex items-center space-x-1.5 transition-colors cursor-pointer"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Add Evidence</span>
        </button>

        <button
          onClick={() => onSelect(skill)}
          className="px-3 py-1.5 text-brand-400 hover:text-brand-300 text-xs font-semibold flex items-center space-x-1 transition-colors cursor-pointer"
        >
          <span>Evidence Trail</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
