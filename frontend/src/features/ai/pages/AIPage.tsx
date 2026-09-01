import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { aiApi, AIConversation } from '@/services/api/ai';
import { AIMessageBubble } from '../components/AIMessageBubble';
import { AIActionCard } from '../components/AIActionCard';
import { Sparkles, Send, Plus, MessageSquare, ShieldCheck, ArrowRight } from 'lucide-react';

export function AIPage() {
  const [selectedConvId, setSelectedConvId] = useState<string | undefined>(undefined);
  const [inputMessage, setInputMessage] = useState('');
  const queryClient = useQueryClient();

  const { data: conversations = [], isLoading: convsLoading } = useQuery({
    queryKey: ['ai_conversations'],
    queryFn: () => aiApi.listConversations(),
  });

  const activeConvId = selectedConvId || conversations[0]?.id;

  const { data: activeConv, isLoading: activeConvLoading } = useQuery({
    queryKey: ['ai_conversation', activeConvId],
    queryFn: () => (activeConvId ? aiApi.getConversation(activeConvId) : null),
    enabled: !!activeConvId,
  });

  const chatMutation = useMutation({
    mutationFn: (msg: string) => aiApi.chat(msg, activeConvId),
    onSuccess: (res) => {
      setSelectedConvId(res.conversation_id);
      queryClient.invalidateQueries({ queryKey: ['ai_conversations'] });
      queryClient.invalidateQueries({ queryKey: ['ai_conversation', res.conversation_id] });
      setInputMessage('');
    },
  });

  const confirmActionMutation = useMutation({
    mutationFn: (actionId: string) => aiApi.confirmAction(actionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ai_conversation'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['planner'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });

  const rejectActionMutation = useMutation({
    mutationFn: (actionId: string) => aiApi.rejectAction(actionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ai_conversation'] });
    },
  });

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;
    await chatMutation.mutateAsync(inputMessage);
  };

  const samplePrompts = [
    'What should I work on today based on my goals?',
    'Why is my productivity score where it is?',
    'Help me create a practice task for my biggest skill gap.',
    'Plan a 2-hour evening focus block for me.',
  ];

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight flex items-center space-x-2.5">
            <Sparkles className="w-6 h-6 text-brand-400" />
            <span>Think2Act AI Coach</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Grounded operating intelligence reasoning over your goals, tasks, focus history, and skill evidence.
          </p>
        </div>

        <button
          onClick={() => {
            setSelectedConvId(undefined);
            setInputMessage('');
          }}
          className="px-4 py-2 bg-slate-900 hover:bg-slate-850 border border-slate-800 text-slate-200 text-xs font-semibold rounded-xl flex items-center space-x-2 transition-colors cursor-pointer shrink-0"
        >
          <Plus className="w-4 h-4" />
          <span>New Session</span>
        </button>
      </div>

      {/* Main Chat Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[600px]">
        {/* Left: Conversations History (4 cols) */}
        <div className="lg:col-span-4 bg-slate-900/60 border border-slate-800 rounded-3xl p-4 flex flex-col justify-between shadow-sm">
          <div className="space-y-3">
            <div className="flex items-center space-x-2 px-2 text-xs font-bold uppercase tracking-wider text-slate-400">
              <MessageSquare className="w-4 h-4" />
              <span>Coaching Sessions</span>
            </div>

            {conversations.length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-500 italic">
                No past sessions yet. Ask anything to start your first session.
              </div>
            ) : (
              <div className="space-y-1 overflow-y-auto max-h-96">
                {conversations.map((c) => (
                  <button
                    key={c.id}
                    onClick={() => setSelectedConvId(c.id)}
                    className={`w-full text-left p-3 rounded-xl text-xs font-semibold transition-all flex items-center justify-between cursor-pointer ${
                      activeConvId === c.id
                        ? 'bg-brand-600/20 text-brand-300 border border-brand-500/30 font-bold'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-950/40'
                    }`}
                  >
                    <span className="truncate pr-2">{c.title}</span>
                    <span className="text-[10px] text-slate-500 shrink-0">
                      {new Date(c.updated_at).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="p-3 bg-slate-950/40 border border-slate-800/80 rounded-2xl flex items-center space-x-2.5 text-[11px] text-slate-400">
            <ShieldCheck className="w-4 h-4 text-brand-400 shrink-0" />
            <span>Strict confirmation guardrails: AI never mutates your data without approval.</span>
          </div>
        </div>

        {/* Right: Active Chat & Interactive Action Cards (8 cols) */}
        <div className="lg:col-span-8 bg-slate-900/80 border border-slate-800 rounded-3xl flex flex-col justify-between p-6 shadow-xl backdrop-blur-sm">
          {/* Messages Area */}
          <div className="space-y-4 overflow-y-auto max-h-[460px] pr-2">
            {!activeConv || activeConv.messages.length === 0 ? (
              <div className="py-12 text-center space-y-6">
                <div className="w-12 h-12 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-brand-400 mx-auto flex items-center justify-center">
                  <Sparkles className="w-6 h-6" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-lg font-bold text-slate-100">How can I accelerate your execution today?</h3>
                  <p className="text-xs text-slate-400 max-w-md mx-auto">
                    I have live visibility into your goals, tasks, focus patterns, and skill gaps.
                  </p>
                </div>

                {/* Quick Prompts */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg mx-auto text-left">
                  {samplePrompts.map((prompt, i) => (
                    <button
                      key={i}
                      onClick={() => setInputMessage(prompt)}
                      className="p-3 bg-slate-950/60 hover:bg-slate-950 border border-slate-800/80 rounded-xl text-xs text-slate-300 hover:text-brand-300 transition-colors text-left flex items-center justify-between group cursor-pointer"
                    >
                      <span className="line-clamp-2">{prompt}</span>
                      <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-brand-400 shrink-0 ml-2" />
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              activeConv.messages.map((m) => (
                <AIMessageBubble key={m.id} message={m} />
              ))
            )}

            {/* Render any Active Proposed Actions in the Conversation */}
            {activeConv && activeConv.actions.length > 0 && (
              <div className="pt-2 border-t border-slate-800/80">
                <div className="text-[11px] font-bold text-brand-400 uppercase tracking-wider mb-2">
                  Action Proposals Ready For Review
                </div>
                {activeConv.actions.map((act) => (
                  <AIActionCard
                    key={act.id}
                    action={act}
                    onConfirm={(id) => confirmActionMutation.mutate(id)}
                    onReject={(id) => rejectActionMutation.mutate(id)}
                  />
                ))}
              </div>
            )}
          </div>

          {/* Input Box */}
          <form onSubmit={handleSend} className="pt-4 border-t border-slate-800 flex items-center space-x-3">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask for advice, schedule requests, or skill guidance..."
              className="flex-1 px-4 py-3 bg-slate-950 border border-slate-800 rounded-2xl text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 font-medium"
            />
            <button
              type="submit"
              disabled={chatMutation.isPending || !inputMessage.trim()}
              className="px-5 py-3 bg-brand-600 hover:bg-brand-500 text-white text-sm font-semibold rounded-2xl flex items-center space-x-2 shadow-lg shadow-brand-500/25 transition-all cursor-pointer disabled:opacity-50"
            >
              <span>Send</span>
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
