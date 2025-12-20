import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Minimize2, Maximize2, Bot, User, Sparkles, RefreshCw, Paperclip, FolderOpen, FileText } from 'lucide-react';
import { createChatSession } from '../services/geminiService';
import { ChatSession } from "@google/generative-ai";
import { useApp } from '../context/AppContext';

export const ChatWidget: React.FC = () => {
  const { knowledgeFolders, rcateData, briefingItems, chatHistory, setChatHistory, calculatorTotal } = useApp();
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [activeNotebookId, setActiveNotebookId] = useState<string>('');
  
  const chatSessionRef = useRef<ChatSession | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // If chat history updates (e.g. from Home), open the widget
  useEffect(() => {
      if (chatHistory.length > 1) { 
          setIsOpen(true);
      }
  }, [chatHistory.length]);

  // Init Session
  useEffect(() => {
    if (isOpen && !chatSessionRef.current) {
      chatSessionRef.current = createChatSession();
    }
  }, [isOpen]);

  // Scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, isOpen, isMinimized, isStreaming]);

  const handleSend = async () => {
    if (!input.trim() || !chatSessionRef.current || isStreaming) return;

    const userMsg = input;
    setInput('');
    setChatHistory(prev => [...prev, { role: 'user', text: userMsg }]);
    setIsStreaming(true);

    try {
      const parts: any[] = []; // In new SDK, array of strings or Part objects

      // 1. INJECT GLOBAL CONTEXT
      let systemContext = `[System Context]\nYou are the central AI for AICPA Core. You have access to the user's current environment.`;
      
      if (rcateData.task || rcateData.context) {
          systemContext += `\n\n[Current Strategy Draft]:\n${JSON.stringify(rcateData)}`;
      }
      
      if (calculatorTotal !== 0) {
          systemContext += `\n\n[User's Calculator Value]: $${calculatorTotal.toLocaleString()}\n(If the user asks about 'the total' or 'the calculated number', refer to this value.)`;
      }
      
      if (briefingItems.length > 0) {
          systemContext += `\n\n[Today's Briefing News]:\n${briefingItems.map(b => `- ${b.headline || b.title || 'News Item'}`).join('\n')}`;
      }

      parts.push({ text: systemContext });

      // 2. INJECT NOTEBOOK DOCUMENTS
      if (activeNotebookId) {
        const notebook = knowledgeFolders.find(f => f.id === activeNotebookId);
        if (notebook && notebook.docs.length > 0) {
            parts.push({ text: `\n[Active Notebook]: "${notebook.name}". Use these docs as primary source.` });
            notebook.docs.forEach(doc => {
                parts.push({ text: `\n--- Doc: ${doc.name} (${doc.mimeType}) ---\n` });
                if (doc.content) {
                    parts.push({
                        inlineData: {
                            mimeType: doc.mimeType,
                            data: doc.content
                        }
                    });
                }
            });
        }
      }

      // 3. User Query
      parts.push({ text: userMsg });

      // 4. Placeholder for stream
      setChatHistory(prev => [...prev, { role: 'model', text: '🔄 Processing via LLM Router (Ollama → API)...' }]);
      
      // === NEW: Call Backend LLM Router instead of direct Gemini SDK ===
      const fullSystemPrompt = parts.map(p => (p as any).text || '').join('\n');
      try {
        const response = await fetch('http://localhost:8010/api/chat/message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: userMsg,
            provider: 'auto',  // Ollama-first, fallback to API
            quality_tier: 'standard',
            max_tokens: 2048,
            system_prompt: fullSystemPrompt,
          }),
        });
        
        const data = await response.json();
        
        if (data.success && data.response) {
          const providerInfo = data.routing?.provider ? ` [via ${data.routing.provider}]` : '';
          setChatHistory(prev => {
            const newMsgs = [...prev];
            newMsgs[newMsgs.length - 1] = { role: 'model', text: data.response + providerInfo };
            return newMsgs;
          });
        } else {
          throw new Error(data.error || 'Unknown error from LLM Router');
        }
      } catch (backendError) {
        console.warn('Backend LLM Router failed, falling back to direct SDK:', backendError);
        
        // Fallback: Try direct Gemini SDK if backend fails
        if (chatSessionRef.current) {
          const result = await chatSessionRef.current.sendMessageStream(parts);
          let fullText = "";
          for await (const chunk of result.stream) {
            const text = chunk.text();
            if (text) {
              fullText += text;
              setChatHistory(prev => {
                const newMsgs = [...prev];
                newMsgs[newMsgs.length - 1] = { role: 'model', text: fullText + ' [fallback: Gemini SDK]' };
                return newMsgs;
              });
            }
          }
        } else {
          throw backendError;
        }
      }
    } catch (error: any) {
      console.error(error);
      const errorMsg = error?.message?.includes('429') || error?.message?.includes('Quota')
        ? '⚠️ Daily Quota Exceeded. Try again later.'
        : `Error: ${error?.message || 'Connection interrupted'}`;
      setChatHistory(prev => {
          const newMsgs = [...prev];
          newMsgs[newMsgs.length - 1] = { role: 'model', text: errorMsg };
          return newMsgs;
      });
    } finally {
      setIsStreaming(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleReset = () => {
    setChatHistory([{ role: 'model', text: 'Conversation reset.' }]);
    chatSessionRef.current = createChatSession();
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-full shadow-2xl shadow-emerald-600/30 flex items-center justify-center text-white hover:scale-110 transition-all duration-300 z-50 group border border-emerald-500/50"
      >
        <MessageSquare size={24} className="group-hover:animate-pulse fill-white/20" />
        <span className="absolute -top-1 -right-1 w-3.5 h-3.5 bg-red-500 rounded-full border-2 border-white animate-bounce"></span>
      </button>
    );
  }

  const activeNotebookName = knowledgeFolders.find(f => f.id === activeNotebookId)?.name;

  return (
    <div className={`fixed bottom-6 right-6 bg-white/95 backdrop-blur-xl rounded-[2rem] shadow-2xl border border-slate-200/50 z-50 flex flex-col overflow-hidden transition-all duration-500 ease-in-out font-sans ${isMinimized ? 'w-72 h-16' : 'w-[90vw] sm:w-[450px] h-[650px] max-h-[80vh]'}`}>
      <div 
        className="bg-slate-900 p-4 flex justify-between items-center text-white cursor-pointer select-none" 
        onClick={() => !isMinimized && setIsMinimized(!isMinimized)}
      >
        <div className="flex items-center gap-3">
          <div className="bg-emerald-600 p-1.5 rounded-lg shadow-lg border border-emerald-500"><Bot size={18} className="text-white" /></div>
          <div>
             <span className="text-sm font-bold tracking-wide block">AICPA Co-pilot</span>
             {!isMinimized && <span className="text-[10px] text-emerald-400 font-medium flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>Active</span>}
          </div>
        </div>
        <div className="flex items-center gap-1">
          <button onClick={(e) => { e.stopPropagation(); handleReset(); }} className="hover:bg-white/10 p-1.5 rounded-md text-slate-400 hover:text-white transition-colors"><RefreshCw size={14} /></button>
          <button onClick={(e) => { e.stopPropagation(); setIsMinimized(!isMinimized); }} className="hover:bg-white/10 p-1.5 rounded-md text-slate-400 hover:text-white transition-colors">{isMinimized ? <Maximize2 size={16} /> : <Minimize2 size={16} />}</button>
          <button onClick={(e) => { e.stopPropagation(); setIsOpen(false); }} className="hover:bg-white/10 p-1.5 rounded-md text-slate-400 hover:text-red-400 transition-colors"><X size={16} /></button>
        </div>
      </div>

      {!isMinimized && (
        <>
          <div className="bg-slate-50 border-b border-slate-200 px-4 py-3">
             <div className="flex items-center gap-2 mb-2">
                <FolderOpen size={12} className="text-slate-500" />
                <span className="text-[10px] font-bold text-slate-500 uppercase">Context Source</span>
             </div>
             <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-1">
                 <button onClick={() => setActiveNotebookId('')} className={`text-xs px-3 py-1.5 rounded-full transition-all flex items-center gap-1 flex-shrink-0 border ${!activeNotebookId ? 'bg-slate-800 text-white border-slate-800 shadow-sm' : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300'}`}>
                    <Sparkles size={10} /> Global Context
                 </button>
                 {knowledgeFolders.map(folder => (
                     <button key={folder.id} onClick={() => setActiveNotebookId(folder.id)} className={`text-xs px-3 py-1.5 rounded-full transition-all flex items-center gap-1.5 flex-shrink-0 border ${activeNotebookId === folder.id ? 'bg-emerald-600 text-white border-emerald-600 shadow-md' : 'bg-white text-slate-600 border-slate-200 hover:border-emerald-300 hover:text-emerald-600'}`}>
                        <FileText size={10} /> {folder.name}
                     </button>
                 ))}
             </div>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-5 bg-slate-50/50 scrollbar-thin scrollbar-thumb-slate-200">
            {chatHistory.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
                <div className={`flex items-end gap-2 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm border ${msg.role === 'user' ? 'bg-white border-slate-200' : 'bg-slate-900 border-slate-800'}`}>
                        {msg.role === 'user' ? <User size={14} className="text-slate-600" /> : <Sparkles size={14} className="text-emerald-400" />}
                    </div>
                    <div className={`rounded-2xl px-4 py-3 text-sm shadow-sm whitespace-pre-wrap leading-relaxed ${msg.role === 'user' ? 'bg-emerald-600 text-white rounded-br-sm' : 'bg-white border border-slate-200 text-slate-800 rounded-bl-sm'}`}>
                        {msg.text}
                        {msg.role === 'model' && msg.text === '' && (
                            <div className="flex space-x-1.5 py-1">
                                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
                                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-75"></span>
                                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-150"></span>
                            </div>
                        )}
                    </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {activeNotebookId && (
            <div className="px-4 py-2 bg-emerald-50/80 backdrop-blur-sm border-t border-emerald-100 flex items-center justify-between animate-slide-down">
                <span className="text-[11px] text-emerald-700 font-medium flex items-center gap-1.5"><Paperclip size={12} /> Connected: <strong>{activeNotebookName}</strong></span>
                <button onClick={() => setActiveNotebookId('')} className="text-emerald-400 hover:text-emerald-600"><X size={12} /></button>
            </div>
          )}

          <div className="p-4 bg-white border-t border-slate-100">
            <div className="flex items-center gap-2 relative bg-slate-50 border border-slate-200 rounded-[1.2rem] px-3 py-2 focus-within:ring-2 focus-within:ring-emerald-500/20 focus-within:border-emerald-500 transition-all shadow-inner">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about strategy, news, or docs..."
                className="flex-1 bg-transparent border-none focus:ring-0 text-sm resize-none py-2 px-1 max-h-32 outline-none text-slate-700 placeholder:text-slate-400 font-medium"
                rows={1}
                style={{ minHeight: '44px' }}
              />
              <button onClick={handleSend} disabled={isStreaming || !input.trim()} className={`p-2.5 rounded-xl transition-all duration-200 flex-shrink-0 ${input.trim() ? 'bg-emerald-600 text-white hover:bg-emerald-700 shadow-md' : 'bg-slate-200 text-slate-400 cursor-not-allowed'}`}>
                <Send size={18} />
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};