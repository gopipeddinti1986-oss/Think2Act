import { useAuth } from '@/hooks/useAuth';
import { Bell, Search, User as UserIcon, Sparkles } from 'lucide-react';

export function Header() {
  const { user } = useAuth();

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/50 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center space-x-4 w-96">
        <div className="relative w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search tasks, goals, skills... (Ctrl+K)"
            className="w-full pl-9 pr-4 py-1.5 bg-slate-950/60 border border-slate-800 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-colors"
          />
        </div>
      </div>

      <div className="flex items-center space-x-4">
        {/* Quick AI status pill */}
        <div className="hidden sm:flex items-center space-x-2 px-3 py-1 bg-brand-500/10 border border-brand-500/20 rounded-full text-xs text-brand-300 font-medium">
          <Sparkles className="w-3.5 h-3.5 text-brand-400" />
          <span>AI Coach Active</span>
        </div>

        {/* Notifications */}
        <button
          title="Notifications"
          className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg relative transition-colors"
        >
          <Bell className="w-5 h-5" />
          <span className="w-2 h-2 bg-brand-500 rounded-full absolute top-1.5 right-1.5" />
        </button>

        {/* User Profile avatar */}
        <div className="flex items-center space-x-3 border-l border-slate-800 pl-4">
          <div className="w-8 h-8 rounded-full bg-brand-600/30 border border-brand-500/40 flex items-center justify-center text-brand-300 font-semibold text-xs">
            {user?.name ? user.name.charAt(0).toUpperCase() : <UserIcon className="w-4 h-4" />}
          </div>
          <div className="hidden md:block">
            <p className="text-sm font-medium text-slate-200 leading-none">{user?.name || 'User'}</p>
            <p className="text-xs text-slate-500 leading-none mt-1">{user?.email}</p>
          </div>
        </div>
      </div>
    </header>
  );
}
