import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { skillsApi, UserSkill } from '@/services/api/skills';
import { evidenceApi, CreateEvidenceInput } from '@/services/api/evidence';
import { SkillCard } from '../components/SkillCard';
import { AddEvidenceModal } from '../components/AddEvidenceModal';
import { SkillDetailModal } from '../components/SkillDetailModal';
import { Layers, ShieldCheck, Sparkles, Plus, Grid, List as ListIcon } from 'lucide-react';

export function SkillsPage() {
  const queryClient = useQueryClient();
  const [selectedSkill, setSelectedSkill] = useState<UserSkill | null>(null);
  const [evidenceSkill, setEvidenceSkill] = useState<UserSkill | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const { data: skills = [], isLoading } = useQuery({
    queryKey: ['my_skills'],
    queryFn: () => skillsApi.getMySkills(),
  });

  const addEvidenceMutation = useMutation({
    mutationFn: (data: CreateEvidenceInput) => evidenceApi.addManual(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['my_skills'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });

  return (
    <div className="space-y-6 max-w-6xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <Layers className="w-6 h-6 text-brand-400" />
            <span>Evidence-Based Skill Graph</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Proven capabilities derived from real project commits, completed tasks, and verified work.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          {/* View toggle */}
          <div className="flex items-center p-1 bg-slate-900 border border-slate-800 rounded-xl">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                viewMode === 'grid' ? 'bg-brand-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Grid View"
            >
              <Grid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                viewMode === 'list' ? 'bg-brand-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
              title="List View"
            >
              <ListIcon className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Info Callout: Evidence Philosophy */}
      <div className="p-4 bg-brand-500/10 border border-brand-500/20 rounded-2xl flex items-start space-x-3 text-xs text-brand-300">
        <ShieldCheck className="w-5 h-5 shrink-0 text-brand-400 mt-0.5" />
        <div>
          <span className="font-bold">Evidence over self-assessment:</span> Skill scores are strictly calculated from verifiable executions, completed tasks, project builds, and credentials. Scores decay over prolonged inactivity and strengthen through real-world work.
        </div>
      </div>

      {/* Skills Grid / List */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-44 bg-slate-900/60 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : skills.length === 0 ? (
        <div className="py-16 text-center bg-slate-900/40 border border-dashed border-slate-800 rounded-2xl">
          <Layers className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-200">No Skills Found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1">
            Complete tasks or add project evidence to begin cultivating your Skill Graph.
          </p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {skills.map((s) => (
            <SkillCard
              key={s.skill_id}
              skill={s}
              onSelect={setSelectedSkill}
              onAddEvidence={setEvidenceSkill}
            />
          ))}
        </div>
      ) : (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden shadow-sm">
          <div className="divide-y divide-slate-800/80">
            {skills.map((s) => (
              <div
                key={s.skill_id}
                className="p-4 flex items-center justify-between hover:bg-slate-950/40 transition-colors"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-sm text-slate-200">{s.name}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                      {s.category}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500">{s.evidence_count} evidence records</p>
                </div>

                <div className="flex items-center space-x-6">
                  <div className="text-right">
                    <div className="text-sm font-bold text-brand-400">{s.level} / 100</div>
                    <div className="text-[10px] text-slate-500">
                      {Math.round(s.confidence * 100)}% confidence
                    </div>
                  </div>

                  <button
                    onClick={() => setSelectedSkill(s)}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl transition-colors cursor-pointer"
                  >
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Add Evidence Modal */}
      <AddEvidenceModal
        isOpen={!!evidenceSkill}
        skill={evidenceSkill}
        onClose={() => setEvidenceSkill(null)}
        onSubmit={async (data) => {
          await addEvidenceMutation.mutateAsync(data);
        }}
      />

      {/* Skill Detail Modal */}
      <SkillDetailModal
        isOpen={!!selectedSkill}
        skill={selectedSkill}
        onClose={() => setSelectedSkill(null)}
      />
    </div>
  );
}
