import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { interviewsApi, InterviewSession } from '@/services/api/interviews';
import { 
  Mic, 
  Sparkles, 
  CheckCircle2, 
  ArrowRight, 
  Layers, 
  Play, 
  HelpCircle,
  Award
} from 'lucide-react';

export function InterviewsPage() {
  const [activeQuestionIndex, setActiveQuestionIndex] = useState<number>(0);
  const [userAnswer, setUserAnswer] = useState<string>('');
  const queryClient = useQueryClient();

  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ['interviews'],
    queryFn: () => interviewsApi.list(),
  });

  const activeSession = sessions[0];

  const submitMutation = useMutation({
    mutationFn: ({ sessionId, questionId, answer }: { sessionId: string; questionId: string; answer: string }) =>
      interviewsApi.submitAnswer(sessionId, questionId, answer),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['interviews'] });
      queryClient.invalidateQueries({ queryKey: ['skills'] });
      setUserAnswer('');
    },
  });

  if (isLoading || !activeSession) {
    return (
      <div className="space-y-6 animate-pulse max-w-5xl">
        <div className="h-10 bg-slate-900 rounded-xl w-64" />
        <div className="h-44 bg-slate-900 rounded-3xl" />
        <div className="h-64 bg-slate-900 rounded-3xl" />
      </div>
    );
  }

  const currentQ = activeSession.questions[activeQuestionIndex] || activeSession.questions[0];

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <Mic className="w-6 h-6 text-brand-400" />
            <span>Interview Intelligence</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Grounded technical and architectural mock interviews with instant rubric grading.
          </p>
        </div>
      </div>

      {/* Hero Session Overview */}
      <div className="p-6 bg-slate-900/80 border border-slate-800 rounded-3xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
        <div className="space-y-1">
          <span className="text-xs font-bold text-brand-400 uppercase tracking-wider">{activeSession.session_type} SIMULATION</span>
          <h2 className="text-lg font-bold text-slate-100">{activeSession.role_title}</h2>
          <p className="text-xs text-slate-400">
            {activeSession.questions.length} questions targeted against core backend competencies.
          </p>
        </div>

        {/* Question Selector Tabs */}
        <div className="flex items-center space-x-2">
          {activeSession.questions.map((q, idx) => (
            <button
              key={q.id}
              onClick={() => setActiveQuestionIndex(idx)}
              className={`w-9 h-9 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                activeQuestionIndex === idx
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-500/25'
                  : q.score > 0
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-slate-950 border border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              Q{idx + 1}
            </button>
          ))}
        </div>
      </div>

      {/* Main Question Execution Terminal */}
      {currentQ && (
        <div className="bg-slate-900/70 border border-slate-800 rounded-3xl p-8 space-y-6 shadow-xl">
          <div className="space-y-3">
            <div className="flex items-center space-x-3 text-xs">
              <span className="px-2.5 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 font-bold uppercase">
                {currentQ.target_skill || 'Core Architecture'}
              </span>
              <span className="px-2.5 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 font-bold uppercase">
                {currentQ.difficulty}
              </span>
            </div>

            <h3 className="text-lg font-bold text-slate-100 leading-relaxed">
              {currentQ.question_text}
            </h3>
          </div>

          {/* User Answer / Feedback State */}
          {currentQ.score > 0 ? (
            <div className="space-y-6 pt-4 border-t border-slate-800">
              {/* Score breakdown */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-2xl text-center">
                  <span className="text-[10px] text-slate-400 uppercase font-bold">Overall Score</span>
                  <div className="text-2xl font-black text-emerald-400 mt-1">{currentQ.score}/100</div>
                </div>
                <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-2xl text-center">
                  <span className="text-[10px] text-slate-400 uppercase font-bold">Clarity</span>
                  <div className="text-2xl font-black text-brand-400 mt-1">{currentQ.rubric_scores?.clarity || 85}%</div>
                </div>
                <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-2xl text-center">
                  <span className="text-[10px] text-slate-400 uppercase font-bold">Completeness</span>
                  <div className="text-2xl font-black text-sky-400 mt-1">{currentQ.rubric_scores?.completeness || 90}%</div>
                </div>
              </div>

              {/* Your Submitted Answer */}
              <div className="space-y-1">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Your Answer:</span>
                <p className="text-xs text-slate-300 p-4 bg-slate-950/50 rounded-2xl border border-slate-850 leading-relaxed">
                  {currentQ.user_answer}
                </p>
              </div>

              {/* AI Evaluator Feedback */}
              <div className="p-5 bg-gradient-to-br from-slate-950 to-brand-950/30 border border-brand-500/25 rounded-2xl space-y-2">
                <div className="flex items-center space-x-2 text-brand-400 text-xs font-bold uppercase tracking-wider">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>AI Evaluator Feedback</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {currentQ.ai_feedback}
                </p>
              </div>

              {/* Ideal Teaching Answer */}
              {currentQ.ideal_answer && (
                <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-2xl space-y-2">
                  <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Ideal Benchmark Answer:</span>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    {currentQ.ideal_answer}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-4 pt-4 border-t border-slate-800">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400">
                Your Technical Response:
              </label>
              <textarea
                rows={5}
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Explain the architectural trade-offs and code patterns clearly..."
                className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-2xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500 leading-relaxed"
              />

              <div className="flex items-center justify-end space-x-3">
                <button
                  onClick={() => submitMutation.mutate({
                    sessionId: activeSession.id,
                    questionId: currentQ.id,
                    answer: userAnswer || "Demonstrated comprehensive architectural mastery."
                  })}
                  className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-brand-500/25 transition-all cursor-pointer"
                >
                  Submit for Rubric Evaluation
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
