import { createBrowserRouter, Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { AppShell } from '@/components/layout/AppShell';
import { LoginPage } from '@/features/auth/pages/LoginPage';
import { RegisterPage } from '@/features/auth/pages/RegisterPage';
import { DashboardPage } from '@/features/dashboard/pages/DashboardPage';
import { GoalsPage } from '@/features/goals/pages/GoalsPage';
import { TasksPage } from '@/features/tasks/pages/TasksPage';
import { PlannerPage } from '@/features/planner/pages/PlannerPage';
import { FocusPage } from '@/features/focus/pages/FocusPage';
import { ProgressPage } from '@/features/progress/pages/ProgressPage';
import { SkillsPage } from '@/features/skills/pages/SkillsPage';
import { LearningPage } from '@/features/learning/pages/LearningPage';
import { AIPage } from '@/features/ai/pages/AIPage';
import { FeaturePlaceholder } from '@/components/common/FeaturePlaceholder';
import { 
  Scale, Briefcase, FileText, Mic, Settings 
} from 'lucide-react';

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
          <span className="text-xs font-medium tracking-wider uppercase">Loading Think2Act...</span>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <AppShell />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: <DashboardPage />,
      },
      {
        path: 'goals',
        element: <GoalsPage />,
      },
      {
        path: 'tasks',
        element: <TasksPage />,
      },
      {
        path: 'planner',
        element: <PlannerPage />,
      },
      {
        path: 'focus',
        element: <FocusPage />,
      },
      {
        path: 'progress',
        element: <ProgressPage />,
      },
      {
        path: 'skills',
        element: <SkillsPage />,
      },
      {
        path: 'learning',
        element: <LearningPage />,
      },
      {
        path: 'ai',
        element: <AIPage />,
      },
      {
        path: 'decisions',
        element: (
          <FeaturePlaceholder
            title="Decision Simulator"
            milestone="Phase 2"
            description="Structured multi-factor decision analysis (Time, Risk, Effort, Career Impact)."
            icon={Scale}
            features={[
              'Multi-option weighted criteria scoring',
              'Transparent deterministic scoring algorithm',
              'Explainable trade-off analysis',
              'Long-term decision history and outcome evaluation',
            ]}
          />
        ),
      },
      {
        path: 'jobs',
        element: (
          <FeaturePlaceholder
            title="Job Matching & Applications"
            milestone="Milestone 6"
            description="Personalized job fit matching against real market requirements."
            icon={Briefcase}
            features={[
              'Weighted percentage match against user Skill Graph',
              'Missing skill breakdown per job listing',
              'Kanban application tracker (Saved, Applied, OA, Interview, Offer)',
              'Application event timeline',
            ]}
          />
        ),
      },
      {
        path: 'resume',
        element: (
          <FeaturePlaceholder
            title="Resume & ATS Optimizer"
            milestone="Milestone 7"
            description="ATS analysis and evidence-aligned resume bullet optimization."
            icon={FileText}
            features={[
              'PDF / DOCX resume parsing and section extraction',
              'Profile consistency check against Skill Graph evidence',
              'Job-specific ATS alignment and missing keyword alerts',
              'Verified bullet suggestion generator',
            ]}
          />
        ),
      },
      {
        path: 'interviews',
        element: (
          <FeaturePlaceholder
            title="Interview Intelligence"
            milestone="Milestone 8"
            description="Tailored technical & behavioral mock interviews testing weak skill areas."
            icon={Mic}
            features={[
              'Target role & weak-skill targeted questions',
              'Rubric-based answer evaluation (Correctness, Clarity, Completeness)',
              'Ideal answer breakdown & teaching insights',
              'Interview outcome feedback into Skill Graph',
            ]}
          />
        ),
      },
      {
        path: 'settings',
        element: (
          <FeaturePlaceholder
            title="Settings & Connected Accounts"
            milestone="Milestone 1"
            description="Profile configuration, account preferences, and future API integrations."
            icon={Settings}
            features={[
              'Profile details (Student vs. Employee mode, Target role, Timezone)',
              'Identity & Data Hub (GitHub, LeetCode, LinkedIn connectors)',
              'Data export & privacy controls',
              'Notification preferences',
            ]}
          />
        ),
      },
    ],
  },
  {
    path: '*',
    element: <Navigate to="/dashboard" replace />,
  },
]);
