import { createBrowserRouter, Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { AppShell } from '@/components/layout/AppShell';
import { LoginPage } from '@/features/auth/pages/LoginPage';
import { RegisterPage } from '@/features/auth/pages/RegisterPage';
import { ForgotPasswordPage } from '@/features/auth/pages/ForgotPasswordPage';
import { DashboardPage } from '@/features/dashboard/pages/DashboardPage';
import { GoalsPage } from '@/features/goals/pages/GoalsPage';
import { TasksPage } from '@/features/tasks/pages/TasksPage';
import { PlannerPage } from '@/features/planner/pages/PlannerPage';
import { FocusPage } from '@/features/focus/pages/FocusPage';
import { ProgressPage } from '@/features/progress/pages/ProgressPage';
import { SkillsPage } from '@/features/skills/pages/SkillsPage';
import { LearningPage } from '@/features/learning/pages/LearningPage';
import { AIPage } from '@/features/ai/pages/AIPage';
import { JobsPage } from '@/features/jobs/pages/JobsPage';
import { ResumePage } from '@/features/resume/pages/ResumePage';
import { InterviewsPage } from '@/features/interviews/pages/InterviewsPage';
import { DecisionsPage } from '@/features/decisions/pages/DecisionsPage';
import { FeaturePlaceholder } from '@/components/common/FeaturePlaceholder';
import { Settings } from 'lucide-react';

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
    path: '/forgot-password',
    element: <ForgotPasswordPage />,
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
        path: 'jobs',
        element: <JobsPage />,
      },
      {
        path: 'resume',
        element: <ResumePage />,
      },
      {
        path: 'interviews',
        element: <InterviewsPage />,
      },
      {
        path: 'decisions',
        element: <DecisionsPage />,
      },
      {
        path: 'settings',
        element: (
          <FeaturePlaceholder
            title="Settings & Connected Accounts"
            milestone="Platform Core"
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
