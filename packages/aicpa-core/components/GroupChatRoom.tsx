import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, Plus, User, Hash, Bot, ShieldCheck, Briefcase } from 'lucide-react';
import { ChatRoom, ChatMessage, AgentRole } from '../types';
import { generateAgentReply } from '../services/geminiService';
import { useApp } from '../context/AppContext';

interface GroupChatRoomProps {
  knowledgeFolders: any; // Kept for prop compatibility, but we use Context mostly
  setKnowledgeFolders: any;
}

const SAMPLE_ROOMS: ChatRoom[] = [
  {
    id: 'ai-council-room',
    name: '🤖 AI Strategy Council',
    type: 'ai_council',
    lastMessage: 'Ready to assist.',
    updatedAt: new Date(),
    participants: 4,
    messages: [
        { id: 'intro-1', sender: 'System', text: 'AI 전략 위원회입니다. 현재 작성 중인 전략(R.C.A.T.E.)을 기반으로 조언해드립니다.', timestamp: new Date(), isMe: false, type: 'text' },
    ]
  },
];

export const GroupChatRoom: React.FC<GroupChatRoomProps> = () => {
  const { rcateData } = useApp(); // Access Global Strategy
  const [rooms, setRooms] = useState<ChatRoom[]>(SAMPLE_ROOMS);
  const [activeRoomId, setActiveRoomId] = useState<string>(SAMPLE_ROOMS[0].id);
  const [input, setInput] = useState('');
  const [aiTypingRole, setAiTypingRole] = useState<AgentRole | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const activeRoom = rooms.find(r => r.id === activeRoomId);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeRoom?.messages, aiTypingRole]);

  const addMessage = (roomId: string, message: ChatMessage) => {
    setRooms(prev => prev.map(room => {
      if (room.id === roomId) {
        return {
          ...room,
          messages: [...room.messages, message],
          lastMessage: message.text,
          updatedAt: new Date()
        };
      }
      return room;
    }));
  };

  const handleSendMessage = async () => {
    if (!input.trim() || !activeRoom) return;
    
    const userText = input;
    const newMessage: ChatMessage = { id: Date.now().toString(), sender: 'Me', text: userText, timestamp: new Date(), isMe: true, type: 'text', role: 'USER' };

    addMessage(activeRoomId, newMessage);
    setInput('');

    if (activeRoom.type === 'ai_council') {
        // Inject Strategy Context into Agent Prompt
        const strategyContext = `[Current Project Strategy]:\n${JSON.stringify(rcateData)}\n\n`;
        const historyText = strategyContext + activeRoom.messages.slice(-5).map(m => `${m.sender}: ${m.text}`).join('\n') + `\nMe: ${userText}`;
        
        // Chain of Thought: Drafter -> Manager -> Auditor
        setAiTypingRole('DRAFTER');
        const drafterReply = await generateAgentReply('DRAFTER', historyText);
        setAiTypingRole(null);
        addMessage(activeRoomId, { id: `ai-d-${Date.now()}`, sender: 'Drafter', text: drafterReply, timestamp: new Date(), isMe: false, type: 'text', role: 'DRAFTER' });

        setAiTypingRole('MANAGER');
        const managerHistory = historyText + `\nDrafter: ${drafterReply}`;
        const managerReply = await generateAgentReply('MANAGER', managerHistory);
        setAiTypingRole(null);
        addMessage(activeRoomId, { id: `ai-m-${Date.now()}`, sender: 'Manager', text: managerReply, timestamp: new Date(), isMe: false, type: 'text', role: 'MANAGER' });
    }
  };

  const getAgentIcon = (role: string) => {
      switch(role) {
          case 'DRAFTER': return <Bot size={20} />;
          case 'MANAGER': return <Briefcase size={20} />;
          case 'AUDITOR': return <ShieldCheck size={20} />;
          default: return <User size={20} />;
      }
  };

  const getAgentColor = (role: string) => {
      switch(role) {
          case 'DRAFTER': return 'bg-blue-100 text-blue-600';
          case 'MANAGER': return 'bg-purple-100 text-purple-600';
          case 'AUDITOR': return 'bg-rose-100 text-rose-600';
          default: return 'bg-slate-200 text-slate-500';
      }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] bg-white">
      <div className="w-80 bg-slate-50 border-r border-slate-200 flex flex-col">
        <div className="p-4 border-b border-slate-200 bg-white sticky top-0">
           <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4 flex items-center gap-2">
             <MessageCircle size={16} /> Team & Clients
           </h2>
        </div>
        <div className="flex-1 overflow-y-auto">
          {rooms.map(room => (
            <button key={room.id} onClick={() => setActiveRoomId(room.id)} className={`w-full flex items-start gap-3 p-4 border-b border-slate-100 transition-all hover:bg-white ${activeRoomId === room.id ? 'bg-white border-l-4 border-l-emerald-500 shadow-sm' : 'bg-transparent border-l-4 border-l-transparent'}`}>
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${room.type === 'ai_council' ? 'bg-indigo-100 text-indigo-600' : 'bg-emerald-100 text-emerald-600'}`}>
                 {room.type === 'ai_council' ? <Bot size={20} /> : <Hash size={20} />}
              </div>
              <div className="flex-1 text-left overflow-hidden">
                  <h3 className="font-bold text-slate-800 truncate text-sm">{room.name}</h3>
                  <p className="text-xs text-slate-500 truncate">{room.lastMessage}</p>
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 flex flex-col bg-[#eef2f6]/50"> 
        {activeRoom ? (
          <>
            <div className="bg-white/90 backdrop-blur-sm border-b border-slate-200 px-6 py-3 flex justify-between items-center shadow-sm sticky top-0 z-10">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  {activeRoom.name}
                  {activeRoom.type === 'ai_council' && <span className="text-[10px] bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full flex items-center gap-1 border border-indigo-100"><Bot size={10} /> Strategy Connected</span>}
              </h2>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-5">
               {activeRoom.messages.map((msg, idx) => (
                   <div key={msg.id} className={`flex gap-3 ${msg.isMe ? 'justify-end' : 'justify-start'} animate-fade-in`}>
                      {!msg.isMe && (
                          <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xs font-bold shadow-sm ${msg.role ? getAgentColor(msg.role) : 'bg-slate-200 text-slate-500'}`}>
                              {msg.role ? getAgentIcon(msg.role) : msg.sender.substring(0, 2)}
                          </div>
                      )}
                      <div className={`flex flex-col ${msg.isMe ? 'items-end' : 'items-start'} max-w-[70%]`}>
                          {!msg.isMe && <span className="text-xs text-slate-500 mb-1 ml-1 font-semibold">{msg.sender}</span>}
                          <div className={`px-5 py-3 rounded-[1.5rem] text-sm leading-relaxed shadow-sm whitespace-pre-wrap ${msg.isMe ? 'bg-emerald-600 text-white rounded-tr-none' : 'bg-white text-slate-800 rounded-tl-none border border-slate-100'}`}>
                              {msg.text}
                          </div>
                      </div>
                   </div>
               ))}
               {aiTypingRole && (
                    <div className="flex gap-3 justify-start animate-fade-in">
                        <div className={`w-10 h-10 rounded-xl flex items-center justify-center shadow-sm ${getAgentColor(aiTypingRole)}`}>{getAgentIcon(aiTypingRole)}</div>
                        <div className="bg-white px-4 py-3 rounded-2xl rounded-tl-none border border-slate-100 shadow-sm flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
                            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-75"></span>
                            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-150"></span>
                        </div>
                    </div>
               )}
               <div ref={messagesEndRef} />
            </div>

            <div className="bg-white p-4 border-t border-slate-200">
                <div className="flex items-end gap-2 bg-slate-50 border border-slate-200 rounded-[1.2rem] p-2 focus-within:ring-2 focus-within:ring-emerald-100 focus-within:border-emerald-400 transition-all">
                    <textarea 
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="전략에 대해 질문하세요..."
                        className="flex-1 bg-transparent border-none focus:ring-0 resize-none max-h-32 min-h-[44px] py-2.5 px-2 text-sm text-slate-800 font-medium"
                        rows={1}
                        disabled={aiTypingRole !== null}
                    />
                    <button onClick={handleSendMessage} disabled={!input.trim() || aiTypingRole !== null} className={`p-2.5 rounded-xl transition-all ${input.trim() && !aiTypingRole ? 'bg-emerald-600 text-white hover:bg-emerald-700 shadow-sm' : 'bg-slate-200 text-slate-400'}`}>
                        <Send size={18} />
                    </button>
                </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
             <MessageCircle size={48} className="mb-4 opacity-50" />
             <p className="text-sm">채팅방을 선택하세요.</p>
          </div>
        )}
      </div>
    </div>
  );
};