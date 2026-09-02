import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { jobsApi, JobPosting, JobApplication } from '@/services/api/jobs';
import { 
  Briefcase, 
  MapPin, 
  DollarSign, 
  CheckCircle2, 
  Clock, 
  Plus, 
  Search, 
  ArrowRight,
  TrendingUp,
  AlertCircle
} from 'lucide-react';

export function JobsPage() {
  const [activeTab, setActiveTab] = useState<'MATCHES' | 'KANBAN'>('MATCHES');
  const [search, setSearch] = useState('');
  const queryClient = useQueryClient();

  const { data: jobs = [], isLoading: jobsLoading } = useQuery({
    queryKey: ['jobs'],
    queryFn: () => jobsApi.list(),
  });

  const { data: applications = [], isLoading: appsLoading } = useQuery({
    queryKey: ['applications'],
    queryFn: () => jobsApi.listApplications(),
  });

  const applyMutation = useMutation({
    mutationFn: (jobId: string) => jobsApi.createApplication(jobId, 'APPLIED'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['applications'] });
      setActiveTab('KANBAN');
    },
  });

  const updateStatusMutation = useMutation({
    mutationFn: ({ appId, status }: { appId: string; status: string }) => 
      jobsApi.updateStatus(appId, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['applications'] });
    },
  });

  const kanbanColumns = [
    { id: 'SAVED', title: 'Saved / Review' },
    { id: 'APPLIED', title: 'Applied' },
    { id: 'OA', title: 'Online Assessment' },
    { id: 'INTERVIEW', title: 'Interviewing' },
    { id: 'OFFER', title: 'Offer Received 🎉' },
  ];

  const filteredJobs = jobs.filter((j) => 
    j.title.toLowerCase().includes(search.toLowerCase()) ||
    j.company.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8 max-w-6xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <Briefcase className="w-6 h-6 text-brand-400" />
            <span>Job Matching & Applications</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time market opportunities matched against your verified Skill Graph.
          </p>
        </div>

        {/* Tab switch */}
        <div className="flex items-center space-x-1 p-1 bg-slate-900 border border-slate-800 rounded-2xl shrink-0">
          <button
            onClick={() => setActiveTab('MATCHES')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
              activeTab === 'MATCHES'
                ? 'bg-brand-600 text-white shadow-md shadow-brand-500/25'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Matched Roles ({jobs.length})
          </button>
          <button
            onClick={() => setActiveTab('KANBAN')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
              activeTab === 'KANBAN'
                ? 'bg-brand-600 text-white shadow-md shadow-brand-500/25'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Pipeline Tracker ({applications.length})
          </button>
        </div>
      </div>

      {activeTab === 'MATCHES' ? (
        <div className="space-y-4">
          {/* Search */}
          <div className="relative max-w-md">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by title or company..."
              className="w-full pl-10 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
            />
          </div>

          {/* Job Cards */}
          {jobsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-44 bg-slate-900/60 rounded-3xl animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {filteredJobs.map((job) => {
                const isApplied = applications.some((a) => a.job_id === job.id);
                return (
                  <div
                    key={job.id}
                    className="p-6 bg-slate-900/70 border border-slate-800 rounded-3xl space-y-4 flex flex-col justify-between hover:border-slate-700 transition-all shadow-sm"
                  >
                    <div className="space-y-3">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">{job.company}</span>
                          <h3 className="text-base font-bold text-slate-100 mt-0.5">{job.title}</h3>
                        </div>

                        {/* Match Badge */}
                        <div className="px-3 py-1 bg-brand-500/10 border border-brand-500/25 rounded-xl text-center shrink-0">
                          <span className="text-xs font-black text-brand-400">{job.match_percentage}%</span>
                          <p className="text-[9px] text-slate-500 font-bold uppercase">Match</p>
                        </div>
                      </div>

                      <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400">
                        <span className="flex items-center space-x-1">
                          <MapPin className="w-3.5 h-3.5 text-slate-500" />
                          <span>{job.location}</span>
                        </span>
                        {job.salary_range && (
                          <span className="flex items-center space-x-1">
                            <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
                            <span>{job.salary_range}</span>
                          </span>
                        )}
                      </div>

                      <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                        {job.description}
                      </p>

                      {/* Required skills */}
                      {job.required_skills && job.required_skills.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {job.required_skills.map((s, idx) => (
                            <span key={idx} className="px-2 py-0.5 rounded-lg bg-slate-950 border border-slate-800 text-[10px] font-semibold text-slate-300">
                              {s.name}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    <div className="pt-4 border-t border-slate-800/80 flex items-center justify-between">
                      {job.missing_skills.length > 0 ? (
                        <span className="text-[11px] text-amber-400/90 font-medium">
                          Gap: {job.missing_skills.slice(0, 2).join(', ')}
                        </span>
                      ) : (
                        <span className="text-[11px] text-emerald-400 font-semibold flex items-center space-x-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>Full Skill Coverage</span>
                        </span>
                      )}

                      {!isApplied ? (
                        <button
                          onClick={() => applyMutation.mutate(job.id)}
                          className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl shadow-md shadow-brand-500/20 transition-all cursor-pointer"
                        >
                          1-Click Apply
                        </button>
                      ) : (
                        <span className="text-xs font-bold text-slate-400">Applied ✓</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      ) : (
        /* Kanban Pipeline View */
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 overflow-x-auto pb-4">
          {kanbanColumns.map((col) => {
            const colApps = applications.filter((a) => a.status === col.id);
            return (
              <div key={col.id} className="bg-slate-900/50 border border-slate-800 rounded-3xl p-4 space-y-3 min-w-[220px]">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-200">{col.title}</span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
                    {colApps.length}
                  </span>
                </div>

                <div className="space-y-3">
                  {colApps.length === 0 ? (
                    <div className="py-8 text-center text-[11px] text-slate-500 border border-dashed border-slate-800/80 rounded-2xl">
                      Empty
                    </div>
                  ) : (
                    colApps.map((app) => (
                      <div key={app.id} className="p-3.5 bg-slate-950 border border-slate-800 rounded-2xl space-y-2 shadow-sm">
                        <span className="text-[10px] font-bold text-slate-500 uppercase">{app.job?.company || 'Company'}</span>
                        <h4 className="text-xs font-bold text-slate-100">{app.job?.title || 'Position'}</h4>
                        
                        <div className="flex items-center justify-between pt-2 border-t border-slate-900 text-[10px]">
                          <select
                            value={app.status}
                            onChange={(e) => updateStatusMutation.mutate({ appId: app.id, status: e.target.value })}
                            className="bg-slate-900 border border-slate-800 rounded-lg px-2 py-1 text-slate-300 text-[10px] focus:outline-none"
                          >
                            {kanbanColumns.map((c) => (
                              <option key={c.id} value={c.id}>Move: {c.id}</option>
                            ))}
                          </select>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
