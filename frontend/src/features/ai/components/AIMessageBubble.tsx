import { AIMessage } from '@/services/api/ai';
import { Sparkles, User as UserIcon } from 'lucide-react';

interface AIMessageBubbleProps {
  message: AIMessage;
}

export function AIMessageBubble({ message }: AIMessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 text-xs font-bold ${
        isUser
          ? 'bg-slate-800 text-slate-200 border border-slate-700'
          : 'bg-brand-600/30 text-brand-300 border border-brand-500/40 shadow-md shadow-brand-500/20'
      }`}>
        {isUser ? <UserIcon className="w-4 h-4" /> : <Sparkles className="w-4 h-4" />}
      </div>

      <div className={`p-4 rounded-2xl max-w-xl text-sm leading-relaxed ${
        isUser
          ? 'bg-brand-600 text-white rounded-tr-sm shadow-md shadow-brand-500/20 font-medium'
          : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-sm shadow-sm'
      }`}>
        <p className="whitespace-pre-wrap">{message.content}</p>
        <span className={`block text-[10px] mt-2 ${isUser ? 'text-brand-200' : 'text-slate-500'}`}>
          {new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  );
}
