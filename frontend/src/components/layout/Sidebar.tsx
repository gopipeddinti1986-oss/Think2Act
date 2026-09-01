import { NavLink } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { 
  Home, 
  CheckSquare, 
  Calendar, 
  Clock, 
  Scale, 
  TrendingUp, 
  Layers, 
  BookOpen, 
  Briefcase, 
  FileText, 
  Mic, 
  Sparkles, 
  Settings, 
  LogOut,
  Target
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface NavItem {
  label: string;
  to: string;
  icon: typeof Home;
  badge?: string;
}

interface NavSection {
  title?: string;
  items: NavItem[];
}

export function Sidebar() {
  const { logout } = useAuth();

  const sections: NavSection[] = [
    {
      items: [
        { label: 'Dashboard', to: '/dashboard', icon: Home },
        { label: 'Goals', to: '/goals', icon: Target },
      ]
    },
    {
      title: 'EXECUTE',
      items: [
        { label: 'Tasks', to: '/tasks', icon: CheckSquare },
        { label: 'Planner', to: '/planner', icon: Calendar },
        { label: 'Focus Tracker', to: '/focus', icon: Clock },
      ]
    },
    {
      title: 'THINK',
      items: [
        { label: 'Decisions', to: '/decisions', icon: Scale },
        { label: 'Progress', to: '/progress', icon: TrendingUp },
      ]
    },
    {
      title: 'CAREER',
      items: [
        { label: 'Skills Graph', to: '/skills', icon: Layers },
        { label: 'Learning Roadmap', to: '/learning', icon: BookOpen },
        { label: 'Job Matching', to: '/jobs', icon: Briefcase },
        { label: 'Resume & ATS', to: '/resume', icon: FileText },
        { label: 'Interview Prep', to: '/interviews', icon: Mic },
      ]
    },
    {
      title: 'INTELLIGENCE',
      items: [
        { label: 'AI Coach', to: '/ai', icon: Sparkles, badge: 'Pro' },
      ]
    }
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950 flex flex-col justify-between h-screen sticky top-0 shrink-0">
      <div className="flex flex-col h-full overflow-y-auto">
        {/* Brand Header */}
        <div className="h-16 px-6 flex items-center space-x-3 border-b border-slate-850">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-brand-500/20 font-bold text-base">
            T
          </div>
          <div>
            <span className="font-bold text-slate-100 text-lg tracking-tight">Think2Act</span>
            <span className="text-[10px] ml-1.5 px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-400 font-semibold uppercase tracking-wider">v1.0</span>
          </div>
        </div>

        {/* Navigation list */}
        <nav className="p-4 space-y-6 flex-1">
          {sections.map((section, idx) => (
            <div key={idx} className="space-y-1">
              {section.title && (
                <div className="px-3 text-[11px] font-semibold tracking-wider text-slate-500 uppercase mb-2">
                  {section.title}
                </div>
              )}
              {section.items.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-all group',
                      isActive
                        ? 'bg-brand-600/15 text-brand-400 border border-brand-500/20 font-semibold'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                    )
                  }
                >
                  <div className="flex items-center space-x-3">
                    <item.icon className="w-4 h-4 transition-transform group-hover:scale-110" />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-400 font-bold">
                      {item.badge}
                    </span>
                  )}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>

        {/* Footer Actions */}
        <div className="p-4 border-t border-slate-850 space-y-1">
          <NavLink
            to="/settings"
            className={({ isActive }) =>
              cn(
                'flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-slate-900 text-slate-200'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
              )
            }
          >
            <Settings className="w-4 h-4" />
            <span>Settings</span>
          </NavLink>
          <button
            onClick={logout}
            className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium text-rose-400/80 hover:text-rose-300 hover:bg-rose-500/10 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
