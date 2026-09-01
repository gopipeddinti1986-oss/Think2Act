import { TaskFilters as FilterType } from '@/services/api/tasks';
import { Filter, Search } from 'lucide-react';

interface TaskFiltersProps {
  filters: FilterType;
  searchTerm: string;
  activeTab: 'ALL' | 'TODAY' | 'COMPLETED';
  onFilterChange: (filters: FilterType) => void;
  onSearchChange: (val: string) => void;
  onTabChange: (tab: 'ALL' | 'TODAY' | 'COMPLETED') => void;
}

export function TaskFilters({
  filters,
  searchTerm,
  activeTab,
  onFilterChange,
  onSearchChange,
  onTabChange
}: TaskFiltersProps) {
  const tabs = [
    { id: 'ALL', label: 'All Tasks' },
    { id: 'TODAY', label: 'Today / Pending' },
    { id: 'COMPLETED', label: 'Completed' },
  ] as const;

  return (
    <div className="space-y-4">
      {/* Tabs & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Navigation Tabs */}
        <div className="flex items-center space-x-1 p-1 bg-slate-900 border border-slate-800 rounded-xl">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
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
            placeholder="Search by title..."
            className="w-full pl-9 pr-4 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>
      </div>

      {/* Filter dropdowns */}
      <div className="flex flex-wrap items-center gap-3 pt-2">
        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <Filter className="w-3.5 h-3.5 text-slate-500" />
          <span>Filters:</span>
        </div>

        <select
          value={filters.priority || ''}
          onChange={(e) => onFilterChange({ ...filters, priority: e.target.value || undefined })}
          className="px-3 py-1 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500"
        >
          <option value="">All Priorities</option>
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
          <option value="URGENT">Urgent</option>
        </select>

        <select
          value={filters.category || ''}
          onChange={(e) => onFilterChange({ ...filters, category: e.target.value || undefined })}
          className="px-3 py-1 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500"
        >
          <option value="">All Categories</option>
          <option value="Study">Study</option>
          <option value="Project">Project</option>
          <option value="Career">Career</option>
          <option value="DSA">DSA</option>
          <option value="Personal">Personal</option>
        </select>
      </div>
    </div>
  );
}
