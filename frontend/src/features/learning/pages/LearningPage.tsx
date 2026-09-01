import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { learningApi } from '@/services/api/learning';
import { goalsApi } from '@/services/api/goals';
import { SkillGapScanner } from '../components/SkillGapScanner';
import { RoadmapView } from '../components/RoadmapView';
import { BookOpen, Sparkles, Target, Compass } from 'lucide-react';

export function LearningPage() {
  const queryClient = useQueryClient();
  const [selectedRoleId, setSelectedRoleId] = useState<string>('');

  const { data: roles = [] } = useQuery({
    queryKey: ['roles'],
    queryFn: () => learningApi.getRoles(),
  });

  const { data: gapReport, isLoading: gapsLoading } = useQuery({
    queryKey: ['skill_gaps', selectedRoleId],
    queryFn: () => learningApi.getSkillGaps(selectedRoleId || undefined),
  });

  const { data: learningPaths = [], isLoading: pathsLoading } = useQuery({
    queryKey: ['learning_paths'],
    queryFn: () => learningApi.getPaths(),
  });

  const generateRoadmapMutation = useMutation({
    mutationFn: () =>
      learningApi.generateRoadmap({
        role_id: selectedRoleId || (roles[0]?.id || undefined),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['learning_paths'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });

  const convertTaskMutation = useMutation({
    mutationFn: (itemId: string) => learningApi.convertToTask(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['learning_paths'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });

  const completeItemMutation = useMutation({
    mutationFn: (itemId: string) => learningApi.completeItem(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['learning_paths'] });
      queryClient.invalidateQueries({ queryKey: ['my_skills'] });
      queryClient.invalidateQueries({ queryKey: ['skill_gaps'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });

  const activePath = learningPaths[0];

  return (
    <div className="space-y-8 max-w-6xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <BookOpen className="w-6 h-6 text-brand-400" />
            <span>Skill Gap Scanner & Learning Roadmap</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Analyze capability deficits for your target role and transform gaps into executable tasks.
          </p>
        </div>

        {/* Role Selector */}
        {roles.length > 0 && (
          <div className="flex items-center space-x-2 shrink-0">
            <span className="text-xs text-slate-400 font-semibold uppercase">Role:</span>
            <select
              value={selectedRoleId || (roles[0]?.id || '')}
              onChange={(e) => setSelectedRoleId(e.target.value)}
              className="px-3.5 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 font-medium focus:outline-none focus:border-brand-500"
            >
              {roles.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.name}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* 1. On-Demand Skill Gap Scanner */}
      {gapsLoading || !gapReport ? (
        <div className="h-64 bg-slate-900/60 rounded-3xl animate-pulse" />
      ) : (
        <SkillGapScanner
          report={gapReport}
          onGenerateRoadmap={() => generateRoadmapMutation.mutate()}
          generatingRoadmap={generateRoadmapMutation.isPending}
        />
      )}

      {/* 2. Structured Roadmap View */}
      {activePath && (
        <RoadmapView
          path={activePath}
          onConvertToTask={async (id) => {
            await convertTaskMutation.mutateAsync(id);
          }}
          onCompleteItem={async (id) => {
            await completeItemMutation.mutateAsync(id);
          }}
        />
      )}
    </div>
  );
}
