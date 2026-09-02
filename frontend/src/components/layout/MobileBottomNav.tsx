import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { 
  Home, 
  CheckSquare, 
  Clock, 
  Sparkles, 
  Menu, 
  X,
  Target,
  Calendar,
  Scale,
  TrendingUp,
  Layers,
  BookOpen,
  Briefcase,
  FileText,
  Mic,
  Settings,
  LogOut
} from 'lucide-react';
import { cn } from '@/lib/utils';

export function MobileBottomNav() {
  const [moreOpen, setMoreOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const mainTabs = [
    { label: 'Home', to: '/dashboard', icon: Home },
    { label: 'Tasks', to: '/tasks', icon: CheckSquare },
    { label: 'Focus', to: '/focus', icon: Clock },
    { label: 'AI Coach', to: '/ai', icon: Sparkles },
  ];

  const secondaryNavItems = [
    { label: 'Goals', to: '/goals', icon: Target, category: 'CORE' },
    { label: 'Planner', to: '/planner', icon: Calendar, category: 'EXECUTE' },
    { label: 'Decisions', to: '/decisions', icon: Scale, category: 'THINK' },
    { label: 'Progress', to: '/progress', icon: TrendingUp, category: 'THINK' },
    { label: 'Skills Graph', to: '/skills', icon: Layers, category: 'CAREER' },
    { label: 'Learning Roadmap', to: '/learning', icon: BookOpen, category: 'CAREER' },
    { label: 'Job Matching', to: '/jobs', icon: Briefcase, category: 'CAREER' },
    { label: 'Resume & ATS', to: '/resume', icon: FileText, category: 'CAREER' },
    { label: 'Interview Prep', to: '/interviews', icon: Mic, category: 'CAREER' },
    { label: 'Settings', to: '/settings', icon: Settings, category: 'SYSTEM' },
  ];

  const handleNavClick = (to: string) => {
    setMoreOpen(false);
    navigate(to);
  };

  return (
    <>
      {/* Slide-up "More" Sheet on Mobile */}
      {moreOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex flex-col justify-end animate-in fade-in">
          <div className="bg-slate-900 border-t border-slate-800 rounded-t-3xl max-h-[80vh] flex flex-col overflow-hidden shadow-2xl">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <span className="text-sm font-bold text-slate-100">All Modules & Tools</span>
              <button
                onClick={() => setMoreOpen(false)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 grid grid-cols-2 gap-2 overflow-y-auto max-h-[60vh]">
              {secondaryNavItems.map((item) => (
                <button
                  key={item.to}
                  onClick={() => handleNavClick(item.to)}
                  className="flex items-center space-x-3 p-3 rounded-2xl bg-slate-950/70 hover:bg-slate-800/80 border border-slate-800/80 text-left transition-colors cursor-pointer"
                >
                  <div className="p-2 rounded-xl bg-brand-600/10 border border-brand-500/20 text-brand-400">
                    <item.icon className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-semibold text-slate-200">{item.label}</span>
                </button>
              ))}
            </div>

            <div className="p-4 border-t border-slate-800 bg-slate-950">
              <button
                onClick={logout}
                className="w-full py-2.5 px-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-bold flex items-center justify-center space-x-2"
              >
                <LogOut className="w-4 h-4" />
                <span>Sign Out</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Persistent Bottom Tab Bar (Mobile only) */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 h-16 bg-slate-950/95 border-t border-slate-800/80 backdrop-blur-lg flex items-center justify-around px-2">
        {mainTabs.map((tab) => (
          <NavLink
            key={tab.to}
            to={tab.to}
            className={({ isActive }) =>
              cn(
                'flex flex-col items-center justify-center flex-1 py-1 text-[10px] font-medium transition-colors',
                isActive
                  ? 'text-brand-400 font-bold'
                  : 'text-slate-400 hover:text-slate-200'
              )
            }
          >
            <tab.icon className="w-5 h-5 mb-0.5" />
            <span>{tab.label}</span>
          </NavLink>
        ))}

        <button
          onClick={() => setMoreOpen(true)}
          className={cn(
            'flex flex-col items-center justify-center flex-1 py-1 text-[10px] font-medium transition-colors',
            moreOpen ? 'text-brand-400 font-bold' : 'text-slate-400 hover:text-slate-200'
          )}
        >
          <Menu className="w-5 h-5 mb-0.5" />
          <span>More</span>
        </button>
      </nav>
    </>
  );
}
