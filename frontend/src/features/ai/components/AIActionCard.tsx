import { AIAction } from '@/services/api/ai';
import { Check, X, Sparkles, CheckSquare, Calendar, ArrowRight } from 'lucide-react';

interface AIActionCardProps {
  action: AIAction;
  onConfirm: (actionId: string) => void;
  onReject: (actionId: string) => void;
}

export function AIActionCard({ action, onConfirm, onReject }: AIActionCardProps) {
  const isPending = action.status === 'PENDING';
  const isExecuted = action.status === 'EXECUTED';
  const isRejected = action.status === 'REJECTED';

  const actionTitle = {
    CREATE_TASK: 'Proposed New Task',
    SCHEDULE_TASK: 'Proposed Schedule Block',
    COMPLETE_TASK: 'Proposed Task Completion',
    CREATE_ROADMAP: 'Proposed Learning Path',
  }[action.action_type] || 'AI Proposal';

  const icon = {
    CREATE_TASK: CheckSquare,
    SCHEDULE_TASK: Calendar,
    COMPLETE_TASK: Check,
    CREATE_ROADMAP: Sparkles,
  }[action.action_type] || Sparkles;

  const IconComponent = icon;

  return (
    <div className={`p-4 rounded-2xl border transition-all my-3 ${
      isExecuted
        ? 'bg-emerald-950/20 border-emerald-500/30'
        : isRejected
        ? 'bg-rose-950/20 border-rose-500/30 opacity-70'
        : 'bg-slate-900 border-brand-500/40 shadow-lg shadow-brand-950/30'
    }`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start space-x-3 min-w-0">
          <div className={`p-2 rounded-xl shrink-0 ${
            isExecuted ? 'bg-emerald-500/20 text-emerald-400' : 'bg-brand-500/20 text-brand-300'
          }`}>
            <IconComponent className="w-4 h-4" />
          </div>

          <div className="space-y-1 min-w-0 text-xs">
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-200 uppercase tracking-wide">{actionTitle}</span>
              <span className={`text-[10px] font-bold px-2 py-0.2 rounded-full uppercase ${
                isExecuted ? 'bg-emerald-500/20 text-emerald-400' :
                isRejected ? 'bg-rose-500/20 text-rose-400' :
                'bg-brand-500/20 text-brand-300 animate-pulse'
              }`}>
                {action.status}
              </span>
            </div>

            {action.payload && (
              <div className="text-slate-300 font-medium pt-0.5">
                {action.payload.title && <p className="text-sm font-semibold text-slate-100">{action.payload.title}</p>}
                {action.payload.task_title && <p className="text-sm font-semibold text-slate-100">{action.payload.task_title}</p>}
                {action.payload.start_at && (
                  <p className="text-slate-400 text-[11px] mt-0.5">
                    Slot: {new Date(action.payload.start_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} — {new Date(action.payload.end_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                )}
                {action.payload.description && (
                  <p className="text-slate-400 text-[11px] mt-0.5 line-clamp-2">{action.payload.description}</p>
                )}
              </div>
            )}
          </div>
        </div>

        {isPending && (
          <div className="flex items-center space-x-2 shrink-0">
            <button
              onClick={() => onReject(action.id)}
              className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-rose-300 transition-colors cursor-pointer"
              title="Reject action"
            >
              <X className="w-4 h-4" />
            </button>
            <button
              onClick={() => onConfirm(action.id)}
              className="px-3 py-1.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs flex items-center space-x-1 shadow-md shadow-brand-500/25 transition-all cursor-pointer"
            >
              <Check className="w-3.5 h-3.5" />
              <span>Confirm</span>
            </button>
          </div>
        )}

        {isExecuted && (
          <span className="text-xs font-semibold text-emerald-400 flex items-center space-x-1 shrink-0">
            <Check className="w-4 h-4" />
            <span>Applied</span>
          </span>
        )}
      </div>
    </div>
  );
}
