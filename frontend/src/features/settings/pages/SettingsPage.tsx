import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  User, 
  Briefcase, 
  Share2, 
  Sliders, 
  ShieldAlert, 
  Download, 
  Check, 
  Save, 
  Github, 
  Linkedin, 
  Code,
  Clock,
  Bell,
  Trash2,
  Sparkles
} from 'lucide-react';
import { settingsApi, UserSettingsData } from '@/services/api/settings';
import { useAuth } from '@/hooks/useAuth';

export function SettingsPage() {
  const { user, logout } = useAuth();
  const queryClient = useQueryClient();

  const [activeTab, setActiveTab] = useState<'profile' | 'career' | 'connections' | 'preferences' | 'privacy'>('profile');
  const [saveSuccess, setSaveSuccess] = useState<string | null>(null);

  // Settings query
  const { data: settings, isLoading } = useQuery({
    queryKey: ['settings'],
    queryFn: () => settingsApi.getSettings(),
  });

  // Local state for editable fields
  const [formData, setFormData] = useState<Partial<UserSettingsData>>({
    name: '',
    email: '',
    user_mode: 'student',
    timezone: 'UTC',
    bio: '',
    location: '',
    organization: '',
    target_role: 'Backend Software Engineer',
    target_companies: ['Google', 'Stripe', 'Databricks'],
    career_mode: 'ACTIVE_SEARCH',
    github_handle: '',
    linkedin_profile_url: '',
    leetcode_username: '',
  });

  // Preferences local state
  const [workingHoursStart, setWorkingHoursStart] = useState('09:00');
  const [workingHoursEnd, setWorkingHoursEnd] = useState('18:00');
  const [dailyFocusTarget, setDailyFocusTarget] = useState('4');
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);

  useEffect(() => {
    if (settings) {
      setFormData({
        name: settings.name || user?.name || '',
        email: settings.email || user?.email || '',
        user_mode: settings.user_mode || 'student',
        timezone: settings.timezone || 'UTC',
        bio: settings.bio || '',
        location: settings.location || '',
        organization: settings.organization || '',
        target_role: settings.target_role || 'Backend Software Engineer',
        target_companies: settings.target_companies || ['Google', 'Stripe', 'Databricks'],
        career_mode: settings.career_mode || 'ACTIVE_SEARCH',
        github_handle: settings.github_handle || '',
        linkedin_profile_url: settings.linkedin_profile_url || '',
        leetcode_username: settings.leetcode_username || '',
      });
    }
  }, [settings, user]);

  const profileMutation = useMutation({
    mutationFn: (data: Partial<UserSettingsData>) => settingsApi.updateProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      showSuccessFeedback('Profile details saved successfully.');
    },
  });

  const careerMutation = useMutation({
    mutationFn: (data: Partial<UserSettingsData>) => settingsApi.updateCareer(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      showSuccessFeedback('Career preferences updated.');
    },
  });

  const integrationsMutation = useMutation({
    mutationFn: (data: Partial<UserSettingsData>) => settingsApi.updateIntegrations(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      showSuccessFeedback('Connected accounts updated.');
    },
  });

  const showSuccessFeedback = (msg: string) => {
    setSaveSuccess(msg);
    setTimeout(() => setSaveSuccess(null), 3500);
  };

  const handleExportData = async () => {
    try {
      const data = await settingsApi.exportData();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `think2act_export_${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert('Failed to export data.');
    }
  };

  const handleDeleteAccount = async () => {
    if (confirm('Are you sure you want to permanently delete your account and all Think2Act data? This action cannot be undone.')) {
      try {
        await settingsApi.deleteAccount();
        logout();
      } catch (e) {
        alert('Failed to delete account.');
      }
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6 animate-pulse">
        <div className="h-10 bg-slate-900 rounded-2xl w-64" />
        <div className="h-96 bg-slate-900/60 rounded-3xl" />
      </div>
    );
  }

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'career', label: 'Career', icon: Briefcase },
    { id: 'connections', label: 'Connected Accounts', icon: Share2 },
    { id: 'preferences', label: 'Preferences', icon: Sliders },
    { id: 'privacy', label: 'Privacy & Data', icon: ShieldAlert },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
            Settings & Preferences
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Manage your personal profile, career targets, external handles, and data privacy.
          </p>
        </div>

        {saveSuccess && (
          <div className="px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold rounded-xl flex items-center space-x-2 animate-fade-in">
            <Check className="w-4 h-4" />
            <span>{saveSuccess}</span>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center space-x-2 transition-all cursor-pointer whitespace-nowrap ${
                isActive
                  ? 'bg-brand-600 text-white shadow-lg shadow-brand-500/20'
                  : 'bg-slate-900/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab 1: Profile */}
      {activeTab === 'profile' && (
        <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <h2 className="text-lg font-bold text-slate-100">Personal Profile</h2>
            <span className="text-xs text-slate-400">Used for Think2Act AI context personalization</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Full Name</label>
              <input
                type="text"
                value={formData.name || ''}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Email Address</label>
              <input
                type="email"
                disabled
                value={formData.email || ''}
                className="w-full px-4 py-2.5 bg-slate-950/50 border border-slate-800/60 rounded-xl text-xs text-slate-500 cursor-not-allowed"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">User Mode</label>
              <select
                value={formData.user_mode || 'student'}
                onChange={(e) => setFormData({ ...formData, user_mode: e.target.value as any })}
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
              >
                <option value="student">Student / Early Career</option>
                <option value="employee">Industry Professional / Employee</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Timezone</label>
              <select
                value={formData.timezone || 'UTC'}
                onChange={(e) => setFormData({ ...formData, timezone: e.target.value })}
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
              >
                <option value="UTC">UTC (Coordinated Universal Time)</option>
                <option value="America/New_York">America/New_York (EST)</option>
                <option value="America/Los_Angeles">America/Los_Angeles (PST)</option>
                <option value="Europe/London">Europe/London (GMT)</option>
                <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                <option value="Asia/Tokyo">Asia/Tokyo (JST)</option>
              </select>
            </div>

            <div className="sm:col-span-2 space-y-2">
              <label className="text-xs font-semibold text-slate-300">Bio & Goals Summary</label>
              <textarea
                rows={3}
                value={formData.bio || ''}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                placeholder="Share your primary focus, current initiatives, and learning goals..."
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-800">
            <button
              onClick={() => profileMutation.mutate(formData)}
              disabled={profileMutation.isPending}
              className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer"
            >
              <Save className="w-4 h-4" />
              <span>{profileMutation.isPending ? 'Saving...' : 'Save Profile Changes'}</span>
            </button>
          </div>
        </div>
      )}

      {/* Tab 2: Career */}
      {activeTab === 'career' && (
        <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <h2 className="text-lg font-bold text-slate-100">Career Targets & Matching</h2>
            <span className="text-xs text-slate-400">Drives Job Match & Skill Gap scanner</span>
          </div>

          <div className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Target Role</label>
              <input
                type="text"
                value={formData.target_role || ''}
                onChange={(e) => setFormData({ ...formData, target_role: e.target.value })}
                placeholder="e.g. Senior Backend Engineer, AI/ML Infrastructure Engineer"
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Career Search Mode</label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {[
                  { id: 'ACTIVE_SEARCH', title: 'Active Search', desc: 'Actively applying to roles this quarter' },
                  { id: 'SKILL_BUILDING', title: 'Skill Building', desc: 'Focusing on closing gaps & projects' },
                  { id: 'PASSIVE', title: 'Passive', desc: 'Open to exceptional opportunities' },
                ].map((mode) => (
                  <div
                    key={mode.id}
                    onClick={() => setFormData({ ...formData, career_mode: mode.id })}
                    className={`p-4 rounded-2xl border transition-all cursor-pointer ${
                      formData.career_mode === mode.id
                        ? 'bg-brand-950/40 border-brand-500 text-brand-300'
                        : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
                    }`}
                  >
                    <div className="text-xs font-bold text-slate-100">{mode.title}</div>
                    <div className="text-[11px] mt-1 text-slate-400">{mode.desc}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Target Companies (Comma separated)</label>
              <input
                type="text"
                value={(formData.target_companies || []).join(', ')}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    target_companies: e.target.value.split(',').map((s) => s.trim()).filter(Boolean),
                  })
                }
                placeholder="Google, Stripe, Databricks, Meta"
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-800">
            <button
              onClick={() => careerMutation.mutate(formData)}
              disabled={careerMutation.isPending}
              className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer"
            >
              <Save className="w-4 h-4" />
              <span>{careerMutation.isPending ? 'Saving...' : 'Update Career Preferences'}</span>
            </button>
          </div>
        </div>
      )}

      {/* Tab 3: Connected Accounts */}
      {activeTab === 'connections' && (
        <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <h2 className="text-lg font-bold text-slate-100">External Integrations & Portfolios</h2>
            <span className="text-xs text-slate-400">Verifies automated skill evidence & project sync</span>
          </div>

          <div className="space-y-4">
            <div className="flex items-center space-x-4 p-4 bg-slate-950/60 border border-slate-800 rounded-2xl">
              <div className="p-3 bg-slate-900 rounded-xl text-slate-200">
                <Github className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-bold text-slate-200">GitHub Username</div>
                <input
                  type="text"
                  value={formData.github_handle || ''}
                  onChange={(e) => setFormData({ ...formData, github_handle: e.target.value })}
                  placeholder="e.g. torvalds"
                  className="mt-1 w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>

            <div className="flex items-center space-x-4 p-4 bg-slate-950/60 border border-slate-800 rounded-2xl">
              <div className="p-3 bg-slate-900 rounded-xl text-slate-200">
                <Linkedin className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-bold text-slate-200">LinkedIn Profile URL</div>
                <input
                  type="text"
                  value={formData.linkedin_profile_url || ''}
                  onChange={(e) => setFormData({ ...formData, linkedin_profile_url: e.target.value })}
                  placeholder="https://linkedin.com/in/your-profile"
                  className="mt-1 w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>

            <div className="flex items-center space-x-4 p-4 bg-slate-950/60 border border-slate-800 rounded-2xl">
              <div className="p-3 bg-slate-900 rounded-xl text-slate-200">
                <Code className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-bold text-slate-200">LeetCode / Codeforces Handle</div>
                <input
                  type="text"
                  value={formData.leetcode_username || ''}
                  onChange={(e) => setFormData({ ...formData, leetcode_username: e.target.value })}
                  placeholder="e.g. algorithm_king"
                  className="mt-1 w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-800">
            <button
              onClick={() => integrationsMutation.mutate(formData)}
              disabled={integrationsMutation.isPending}
              className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer"
            >
              <Save className="w-4 h-4" />
              <span>{integrationsMutation.isPending ? 'Saving...' : 'Save Connections'}</span>
            </button>
          </div>
        </div>
      )}

      {/* Tab 4: Preferences */}
      {activeTab === 'preferences' && (
        <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <h2 className="text-lg font-bold text-slate-100">Schedule & Focus Preferences</h2>
            <span className="text-xs text-slate-400">Used by intelligent Planner schedule suggestions</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Daily Work Window (Start)</label>
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-brand-400" />
                <input
                  type="time"
                  value={workingHoursStart}
                  onChange={(e) => setWorkingHoursStart(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Daily Work Window (End)</label>
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-brand-400" />
                <input
                  type="time"
                  value={workingHoursEnd}
                  onChange={(e) => setWorkingHoursEnd(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Daily Focus Target (Hours)</label>
              <input
                type="number"
                min="1"
                max="12"
                value={dailyFocusTarget}
                onChange={(e) => setDailyFocusTarget(e.target.value)}
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-brand-500"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Smart Notifications</label>
              <div
                onClick={() => setNotificationsEnabled(!notificationsEnabled)}
                className="flex items-center justify-between p-3 bg-slate-950 border border-slate-800 rounded-xl cursor-pointer"
              >
                <div className="flex items-center space-x-2">
                  <Bell className="w-4 h-4 text-brand-400" />
                  <span className="text-xs text-slate-200">Execution Reminders</span>
                </div>
                <div className={`w-8 h-4 rounded-full transition-colors relative ${notificationsEnabled ? 'bg-brand-600' : 'bg-slate-800'}`}>
                  <div className={`w-3 h-3 bg-white rounded-full absolute top-0.5 transition-transform ${notificationsEnabled ? 'left-4' : 'left-1'}`} />
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-800">
            <button
              onClick={() => showSuccessFeedback('Planner preferences updated.')}
              className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer"
            >
              <Save className="w-4 h-4" />
              <span>Save Preferences</span>
            </button>
          </div>
        </div>
      )}

      {/* Tab 5: Privacy & Data */}
      {activeTab === 'privacy' && (
        <div className="space-y-6">
          {/* Export card */}
          <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-4 shadow-xl">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-brand-500/10 text-brand-400 rounded-xl">
                <Download className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-100">Export Your Think2Act Data</h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Download a complete portable JSON export of all your goals, tasks, skill evidence, focus records, and decisions.
                </p>
              </div>
            </div>

            <div className="pt-2">
              <button
                onClick={handleExportData}
                className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-xl flex items-center space-x-2 transition-colors cursor-pointer"
              >
                <Download className="w-4 h-4" />
                <span>Export JSON Payload</span>
              </button>
            </div>
          </div>

          {/* Danger zone */}
          <div className="bg-rose-950/20 border border-rose-900/30 rounded-3xl p-6 sm:p-8 space-y-4">
            <div className="flex items-center space-x-3 text-rose-400">
              <div className="p-3 bg-rose-500/10 rounded-xl">
                <Trash2 className="w-5 h-5 text-rose-400" />
              </div>
              <div>
                <h3 className="text-base font-bold text-rose-300">Danger Zone: Delete Account</h3>
                <p className="text-xs text-rose-400/80 mt-0.5">
                  Permanently erase your user profile, history, active goals, and skill graph. This action cannot be reversed.
                </p>
              </div>
            </div>

            <div className="pt-2">
              <button
                onClick={handleDeleteAccount}
                className="px-5 py-2.5 bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold rounded-xl flex items-center space-x-2 shadow-lg shadow-rose-600/25 transition-colors cursor-pointer"
              >
                <Trash2 className="w-4 h-4" />
                <span>Permanently Delete Account</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
