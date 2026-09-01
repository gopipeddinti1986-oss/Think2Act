import { useState } from 'react';
import { UserSkill } from '@/services/api/skills';
import { CreateEvidenceInput } from '@/services/api/evidence';
import { X, ShieldCheck } from 'lucide-react';

interface AddEvidenceModalProps {
  isOpen: boolean;
  skill: UserSkill | null;
  onClose: () => void;
  onSubmit: (data: CreateEvidenceInput) => Promise<void>;
}

export function AddEvidenceModal({ isOpen, skill, onClose, onSubmit }: AddEvidenceModalProps) {
  const [sourceType, setSourceType] = useState('PROJECT');
  const [strength, setStrength] = useState(20);
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen || !skill) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) return;
    setSubmitting(true);
    try {
      await onSubmit({
        skill_id: skill.skill_id,
        source_type: sourceType,
        strength,
        description,
      });
      setDescription('');
      onClose();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md overflow-hidden shadow-2xl animate-in fade-in zoom-in-95">
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-brand-400" />
            <h3 className="text-lg font-bold text-slate-100">Add Evidence for {skill.name}</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Evidence Source Type
            </label>
            <select
              value={sourceType}
              onChange={(e) => setSourceType(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-sm text-slate-100 focus:outline-none focus:border-brand-500"
            >
              <option value="PROJECT">Real Project Implementation</option>
              <option value="PROBLEM_SOLVING">DSA / Contest Problem Solved</option>
              <option value="CERTIFICATE">Course / Credential Completion</option>
              <option value="TASK_EXECUTION">Executed Task Work</option>
              <option value="MANUAL">Workplace / Professional Experience</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Evidence Weight / Strength
            </label>
            <select
              value={strength}
              onChange={(e) => setStrength(Number(e.target.value))}
              className="w-full px-3.5 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-sm text-slate-100 focus:outline-none focus:border-brand-500"
            >
              <option value={30}>Major Project (High Strength +30)</option>
              <option value={20}>Feature / Practical Task (+20)</option>
              <option value={15}>Course / Certificate (+15)</option>
              <option value={10}>Coding Exercise / Review (+10)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Detailed Evidence Description *
            </label>
            <textarea
              rows={3}
              required
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="e.g. Implemented Async SQLAlchemy models and JWT bearer authentication in FastAPI backend"
              className="w-full px-3.5 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="pt-4 flex items-center justify-end space-x-3 border-t border-slate-800/80">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-brand-500/25 transition-all disabled:opacity-50"
            >
              {submitting ? 'Recalculating Skill...' : 'Record Evidence & Update'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
