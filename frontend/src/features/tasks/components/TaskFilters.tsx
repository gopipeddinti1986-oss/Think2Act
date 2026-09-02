import { TaskFilters as FilterType } from '@/services/api/tasks';
import { Goal } from '@/types';
import { Filter, Search } from 'lucide-react';

interface TaskFiltersProps {
  filters: FilterType;
  goals?: Goal[];
  searchTerm: string;
  activeTab: 'ALL' | 'TODAY' | 'UPCOMING' | 'COMPLETED';
  onFilterChange: (filters: FilterType) => void;
  onSearchChange: (val: string) => void;
  onTabChange: (tab: 'ALL' | 'TODAY' | 'UPCOMING' | 'COMPLETED') => void;
}

export function TaskFilters({
  filters,
  goals = [],
  searchTerm,
  activeTab,
  onFilterChange,
  onSearchChange,
  onTabChange
}: TaskFiltersProps) {
  const tabs = [
    { id: 'ALL', label: 'All' },
    { id: 'TODAY', label: 'Today' },
    { id: 'UPCOMING', label: 'Upcoming' },
    { id: 'COMPLETED', label: 'Completed' },
  ] as const;

  return (
    <div className="space-y-4">
      {/* Tabs & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Navigation Tabs (Section 4.2 exact: All | Today | Upcoming | Completed) */}
        <div className="flex items-center space-x-1 p-1 bg-slate-900 border border-slate-800 rounded-2xl">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`px-4 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                activeTab === tab.id
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-500/25'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search tasks..."
            className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>
      </div>

      {/* Filter row: Goal · Priority · Status · Skill */}
      <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
        <div className="flex items-center space-x-1.5 text-slate-400 mr-1 font-semibold">
          <Filter className="w-3.5 h-3.5 text-slate-500" />
          <span>Filters:</span>
        </div>

        {/* Goal filter */}
        <select
          value={filters.goal_id || ''}
          onChange={(e) => onFilterChange({ ...filters, goal_id: e.target.value || undefined })}
          className="px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-brand-500"
        >
          <option value="">All Goals</option>
          {goals.map((g) => (
            <option key={g.id} value={g.id}>
              {g.title}
            </option>
          ))}
        </select>

        {/* Priority filter */}
        <select
          value={filters.priority || ''}
          onChange={(e) => onFilterChange({ ...filters, priority: e.target.value || undefined })}
          className="px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-brand-500"
        >
          <option value="">All Priorities</option>
          <option value="HIGH">🔴 High</option>
          <option value="MEDIUM">🟡 Medium</option>
          <option value="LOW">🟢 Low</option>
          <option value="URGENT">🔴 Urgent</option>
        </select>

        {/* Status filter */}
        <select
          value={filters.status || ''}
          onChange={(e) => onFilterChange({ ...filters, status: e.target.value || undefined })}
          className="px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-brand-500"
        >
          <option value="">All Statuses</option>
          <option value="TODO">To Do</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="COMPLETED">Completed</option>
        </select>

        {/* Category / Skill filter */}
        <select
          value={filters.category || ''}
          onChange={(e) => onFilterChange({ ...filters, category: e.target.value || undefined })}
          className="px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-brand-500"
        >
          <option value="">All Skills/Categories</option>
          <option value="FastAPI">FastAPI</option>
          <option value="Python">Python</option>
          <option value="SQL & PostgreSQL">SQL & PostgreSQL</option>
          <option value="Docker & Containers">Docker</option>
          <option value="Backend">Backend</option>
          <option value="DSA">DSA</option>
        </select>
      </div>
    </div>
  );
}
