/**
 * KingdomMessageBoard.tsx
 * 
 * Royal Command Decrees 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useMemo, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Bell, CheckCircle, Clock } from 'lucide-react';
import ErrorBoundary from '@/components/common/ErrorBoundary';

interface Message {
  id: string;
  title: string;
  content: string;
  type?: 'info' | 'warning';
}

const mockMessages: Message[] = [
  { id: '1', title: 'Decree #1: Trinity Expansion', content: 'All agents must ensure 眞善美 metrics are above 90%.' },
  { id: '2', title: 'Decree #2: Serenity Protocol', content: 'GenUI loop activation is now mandatory for all sub-kingdoms.', type: 'warning' },
  { id: '3', title: 'Decree #3: Eternal Archive', content: 'Session logs must be persisted in the Shadow Vault.' },
];

function KingdomMessageBoardContent({
  messages = mockMessages,
}: {
  messages?: Message[];
}) {
  // Memoize messages
  const memoizedMessages = useMemo(() => messages, [messages]);

  // Memoize handlers
  const handleArchive = useCallback(() => {
    console.log('Archive decree');
    // In a real app, this would archive the decree
  }, []);

  const handleAcknowledgeAll = useCallback(() => {
    console.log('Acknowledge all decrees');
    // In a real app, this would acknowledge all decrees
  }, []);

  // Memoize message styles
  const getMessageStyles = useCallback((type?: 'info' | 'warning') => {
    return {
      iconBg: type === 'warning' ? 'bg-amber-500/20' : 'bg-indigo-500/20',
      iconColor: type === 'warning' ? 'text-amber-400' : 'text-indigo-400',
      titleColor: type === 'warning' ? 'text-amber-300' : 'text-white group-hover:text-indigo-300',
    };
  }, []);

  return (
    <div
      className="bg-gradient-to-br from-indigo-950 via-purple-900 to-indigo-950 flex items-center justify-center p-8 rounded-3xl overflow-hidden min-h-[500px] w-full border border-white/10 shadow-2xl"
      role="region"
      aria-labelledby="message-board-title"
    >
      <Card className="w-full max-w-2xl bg-white/5 backdrop-blur-2xl border-white/10 shadow-2xl rounded-3xl overflow-hidden">
        <CardHeader className="text-center border-b border-white/10 pb-6 bg-white/5">
          <CardTitle
            id="message-board-title"
            className="text-3xl font-bold text-white flex items-center justify-center gap-3"
          >
            <Bell className="w-8 h-8 text-yellow-500 animate-pulse" aria-hidden="true" />
            Royal Command Decrees
          </CardTitle>
          <p className="text-indigo-200/50 text-xs mt-2 uppercase tracking-[0.2em] font-light">
            Commander's Daily Intelligence
          </p>
        </CardHeader>

        <CardContent className="p-0">
          <div
            className="max-h-[350px] overflow-y-auto scrollbar-hide p-6 space-y-4"
            role="list"
            aria-label="Royal decrees"
          >
            {memoizedMessages.map((message) => {
              const styles = getMessageStyles(message.type);
              return (
                <div
                  key={message.id}
                  className="group relative flex items-start p-5 hover:bg-white/10 bg-white/5 rounded-2xl transition-all duration-300 border border-white/5 hover:border-white/20 shadow-lg"
                  role="listitem"
                  aria-label={`Decree: ${message.title}`}
                >
                  <div className="flex-shrink-0 mt-1">
                    <div className={`p-2 rounded-full ${styles.iconBg}`} aria-hidden="true">
                      <Clock className={`w-5 h-5 ${styles.iconColor}`} aria-hidden="true" />
                    </div>
                  </div>
                  <div className="ml-4 flex-grow">
                    <h3 className={`font-semibold text-lg transition-colors ${styles.titleColor}`}>
                      {message.title}
                    </h3>
                    <p className="text-sm text-slate-300/80 mt-1.5 leading-relaxed font-light">
                      {message.content}
                    </p>
                    <div
                      className="flex items-center mt-3.5 opacity-60 group-hover:opacity-100 transition-opacity"
                      aria-label="Acknowledged by Scholars"
                    >
                      <CheckCircle className="w-4 h-4 text-emerald-400" aria-hidden="true" />
                      <span className="text-[10px] text-emerald-400 ml-2 uppercase tracking-widest font-bold">
                        Acknowledged by Scholars
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>

        <CardFooter className="flex justify-between items-center p-6 bg-black/20 border-t border-white/10">
          <div className="flex flex-col" aria-label="Protocol information">
            <span className="text-[10px] text-indigo-400/70 uppercase tracking-widest font-black">
              5 Pillars Protocol
            </span>
            <span className="text-[9px] text-indigo-400/40 font-mono">HASH: 0x7E3A...F219</span>
          </div>
          <div className="flex gap-4" role="group" aria-label="Actions">
            <Button
              variant="ghost"
              onClick={handleArchive}
              aria-label="Archive Decree"
              className="text-white/60 hover:text-white hover:bg-white/5 rounded-full px-6 text-xs uppercase tracking-widest transition-all"
            >
              Archive
            </Button>
            <Button
              onClick={handleAcknowledgeAll}
              aria-label="Acknowledge all Decrees"
              className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-full px-8 shadow-xl shadow-indigo-500/20 text-xs uppercase tracking-widest font-bold transition-all border-none"
            >
              Acknowledge All
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}

export default function KingdomMessageBoard({
  messages = mockMessages,
}: {
  messages?: Message[];
}) {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error('KingdomMessageBoard error:', error, errorInfo);
      }}
      fallback={
        <div
          className="bg-gradient-to-br from-indigo-950 via-purple-900 to-indigo-950 flex items-center justify-center p-8 rounded-3xl border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center">Kingdom Message Board를 불러올 수 없습니다.</p>
        </div>
      }
    >
      <KingdomMessageBoardContent messages={messages} />
    </ErrorBoundary>
  );
}
