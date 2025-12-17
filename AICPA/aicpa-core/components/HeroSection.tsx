import React, { useState, useEffect } from 'react';
import { ArrowRight, Clock, ShieldAlert, Cpu, CheckCircle2, TrendingUp, MapPin, RefreshCw, BookOpen, PenTool, ExternalLink, Globe, MessageSquare, Briefcase, ChevronRight, Calendar as CalendarIcon, ListTodo, Sun, Moon, Sunrise, Sunset, CheckSquare, Square, LogIn, Link2, Plus, X, Trash2, Crown, Sparkles } from 'lucide-react';
import { Tab, BriefingItem } from '../types';
import { generateDailyBriefing } from '../services/geminiService';
import { useApp } from '../context/AppContext';

interface HeroSectionProps {
  onNavigate: (tab: Tab) => void;
}

// Glassmorphic Card for Briefing
const BriefingCard = ({ title, icon, color, category, items, handleDiscuss }: { 
    title: string, icon: any, color: string, category: string, items: BriefingItem[], handleDiscuss: (i: BriefingItem) => void 
}) => {
    const displayItems = items.filter(i => i.category === category).slice(0, 2);
    // Determine gradient for icon background
    const iconBg = color.includes('amber') ? 'bg-amber-500/20 text-amber-300' : color.includes('emerald') ? 'bg-emerald-500/20 text-emerald-300' : 'bg-blue-500/20 text-blue-300';
    const borderColor = color.includes('amber') ? 'border-amber-500/30' : color.includes('emerald') ? 'border-emerald-500/30' : 'border-blue-500/30';

    return (
        <div className={`bg-slate-800/40 backdrop-blur-md border ${borderColor} rounded-[2rem] p-6 hover:bg-slate-800/60 hover:border-amber-500/50 transition-all flex flex-col h-full group shadow-lg duration-300 relative overflow-hidden`}>
            {/* Glossy Reflection */}
            <div className="absolute top-0 left-0 w-full h-1/2 bg-gradient-to-b from-white/5 to-transparent pointer-events-none"></div>
            
            <div className={`flex items-center gap-2 mb-4 text-xs font-bold uppercase tracking-wider ${color}`}>
                <div className={`p-1.5 rounded-lg ${iconBg} backdrop-blur-sm transition-colors`}>
                    {icon}
                </div>
                <span className="drop-shadow-sm">{title}</span>
            </div>
            <div className="flex-1 space-y-4">
              {displayItems.length > 0 ? displayItems.map((item, i) => (
                  <div key={i} className="group/item relative pl-4 border-l-2 border-slate-600 hover:border-amber-400 transition-colors">
                      <a href={item.url} target="_blank" rel="noreferrer" className="text-sm text-slate-300 font-medium group-hover/item:text-white line-clamp-2 leading-relaxed block mb-1.5 transition-colors">
                          {item.headline}
                      </a>
                      <div className="flex gap-3 opacity-0 group-hover/item:opacity-100 transition-opacity translate-y-1 group-hover/item:translate-y-0 duration-200">
                          <button onClick={() => handleDiscuss(item)} className="text-[10px] text-amber-400 hover:text-amber-300 flex items-center gap-1 font-bold bg-amber-900/30 px-2 py-0.5 rounded-full border border-amber-500/30 hover:border-amber-400/50 backdrop-blur-sm">
                              <MessageSquare size={10} /> Discuss
                          </button>
                      </div>
                  </div>
              )) : (
                  <div className="text-slate-500 text-xs italic flex items-center gap-2 py-4">
                      <RefreshCw size={12} className="animate-spin text-emerald-500" /> Connecting to Intel Feed...
                  </div>
              )}
            </div>
        </div>
    );
};

export const HeroSection: React.FC<HeroSectionProps> = ({ onNavigate }) => {
  const { setBriefingItems, addToChat, user, calendarEvents, todoList, addTodo, toggleTodo, deleteTodo, isGoogleConnected, connectGoogle, showNotification } = useApp();
  const [localBriefing, setLocalBriefing] = useState<BriefingItem[]>([]);
  const [location, setLocation] = useState<string>("United States");
  const [loading, setLoading] = useState<boolean>(true);
  const [language, setLanguage] = useState<'ko' | 'en'>('ko'); 
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isConnecting, setIsConnecting] = useState(false);
  const [newTaskText, setNewTaskText] = useState('');

  // Update time every minute for greeting logic
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const getLocationAndFetch = async () => {
        setLoading(true);
        try {
            const getPosition = () => new Promise<GeolocationPosition>((resolve, reject) => {
                if (!navigator.geolocation) return reject("Geolocation not supported");
                navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 });
            });

            const position = await Promise.race([
                getPosition(),
                new Promise<null>((resolve) => setTimeout(() => resolve(null), 5000))
            ]);

            let searchLoc = "United States";
            if (position) {
                searchLoc = `${position.coords.latitude}, ${position.coords.longitude}`;
                if (language === 'ko') setLocation("현재 위치");
                else setLocation("Current Location");
            } else {
                 if (language === 'ko') setLocation("서울 (기본값)");
                 else setLocation("United States (Default)");
            }

            await fetchBriefing(searchLoc, language);

        } catch (e) {
            await fetchBriefing("United States", language);
        } finally {
            setLoading(false);
        }
    };

    getLocationAndFetch();
  }, [language]); 

  const fetchBriefing = async (loc: string, lang: 'ko' | 'en') => {
    const items = await generateDailyBriefing(loc, lang);
    setLocalBriefing(items);
    setBriefingItems(items);
  };

  const handleDiscuss = (item: BriefingItem) => {
      addToChat(`이 뉴스에 대해 더 자세히 알려줘: "${item.headline}"`, 'user');
  };

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'ko' ? 'en' : 'ko');
  };

  const handleGoogleConnect = () => {
      setIsConnecting(true);
      // Simulate Auth Delay
      setTimeout(() => {
          connectGoogle();
          setIsConnecting(false);
          showNotification("Google Workspace Connected", "success");
      }, 1000);
  };

  const openGoogleCalendar = () => {
      window.open('https://calendar.google.com/calendar/u/0/r', '_blank');
  };

  const handleAddTask = (e: React.FormEvent) => {
      e.preventDefault();
      if (!newTaskText.trim()) return;
      addTodo(newTaskText.trim());
      setNewTaskText('');
  };

  // Dynamic Greeting Logic
  const getGreetingData = () => {
      const hour = currentTime.getHours();
      if (hour >= 5 && hour < 12) {
          return { text: language === 'ko' ? "좋은 아침입니다," : "Good Morning,", icon: <Sunrise size={24} className="text-amber-300" /> };
      } else if (hour >= 12 && hour < 17) {
          return { text: language === 'ko' ? "즐거운 오후입니다," : "Good Afternoon,", icon: <Sun size={24} className="text-amber-400" /> };
      } else if (hour >= 17 && hour < 21) {
          return { text: language === 'ko' ? "편안한 저녁입니다," : "Good Evening,", icon: <Sunset size={24} className="text-orange-400" /> };
      } else {
          return { text: language === 'ko' ? "늦은 밤입니다," : "Good Night,", icon: <Moon size={24} className="text-indigo-300" /> };
      }
  };

  const greeting = getGreetingData();
  
  // Calculate Progress
  const completedTasks = todoList.filter(t => t.completed).length;
  const totalTasks = todoList.length;

  return (
    <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12 gap-6 text-white">
            <div className="animate-fade-in">
                <div className="flex items-center gap-2 text-amber-300 text-xs font-bold uppercase tracking-wider mb-2.5 bg-slate-800/50 w-fit px-3 py-1 rounded-full border border-slate-700/50 backdrop-blur-sm shadow-sm">
                    {greeting.icon} {currentTime.toLocaleDateString(language === 'ko' ? 'ko-KR' : 'en-US', { weekday: 'long' })} Status
                </div>
                <h1 className="text-4xl md:text-5xl font-extrabold text-white tracking-tight leading-tight mb-3 drop-shadow-lg">
                    {greeting.text} <br className="hidden md:block"/>
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-200 via-white to-amber-200 animate-pulse">{user?.name || 'AICPA Partner'}.</span>
                </h1>
                <p className="text-slate-300 text-sm flex items-center gap-2 font-medium">
                    <MapPin size={14} className="text-emerald-400" /> 
                    Intel Region: <span className="text-white">{location}</span>
                </p>
            </div>
            
            <div className="flex flex-col items-end gap-3 animate-fade-in" style={{ animationDelay: '0.1s' }}>
                <div className="flex gap-3">
                    <button onClick={toggleLanguage} className="h-10 px-4 bg-slate-800/50 hover:bg-slate-700/50 border border-slate-600 rounded-full text-xs font-bold text-white transition-all flex items-center gap-2 shadow-lg backdrop-blur-md">
                        <Globe size={14} className="text-amber-400"/> {language === 'ko' ? 'EN' : 'KR'}
                    </button>
                    <button onClick={() => fetchBriefing(location, language)} className="h-10 w-10 bg-slate-800/50 hover:bg-slate-700/50 border border-slate-600 rounded-full text-white transition-all flex items-center justify-center shadow-lg group backdrop-blur-md">
                        <RefreshCw size={16} className={`group-hover:rotate-180 transition-transform duration-500 text-amber-400 ${loading ? "animate-spin" : ""}`} />
                    </button>
                </div>
                
                {/* Schedule Integration Indicator */}
                {isGoogleConnected ? (
                    <div className="flex items-center gap-2 bg-emerald-900/30 px-3 py-1.5 rounded-lg border border-emerald-500/30 backdrop-blur-sm">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_5px_#34d399]"></div>
                        <span className="text-[10px] text-emerald-100 font-mono font-bold">Google Workspace Active</span>
                    </div>
                ) : (
                    <div className="flex items-center gap-2 bg-slate-800/50 px-3 py-1.5 rounded-lg border border-slate-700/50 backdrop-blur-sm">
                        <div className="w-1.5 h-1.5 rounded-full bg-slate-400"></div>
                        <span className="text-[10px] text-slate-400 font-mono">Local Mode</span>
                    </div>
                )}
            </div>
        </div>

        {/* BENTO GRID LAYOUT */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
            
            {/* 1. Main Action: New Project (Large) */}
            <div 
                onClick={() => onNavigate(Tab.GENERATOR)}
                className="md:col-span-2 bg-gradient-to-br from-emerald-800 to-slate-900 rounded-[2rem] p-8 text-white relative overflow-hidden group cursor-pointer shadow-2xl hover:shadow-[0_0_30px_rgba(16,185,129,0.3)] transition-all duration-500 animate-slide-down border border-emerald-500/30 ring-1 ring-white/5"
            >
                {/* Gold Glow */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-amber-500/20 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2 mix-blend-screen"></div>
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-[80px] translate-y-1/2 -translate-x-1/2"></div>
                
                <div className="absolute -top-10 -right-10 p-10 opacity-10 group-hover:opacity-20 group-hover:scale-110 transition-all duration-700 rotate-12">
                    <PenTool size={180} className="text-white"/>
                </div>
                <div className="relative z-10 flex flex-col h-full justify-between">
                    <div>
                        <div className="bg-amber-500/20 backdrop-blur-md w-fit px-3 py-1 rounded-full text-xs font-bold mb-5 border border-amber-400/40 text-amber-200 flex items-center gap-2 shadow-[0_0_10px_rgba(245,158,11,0.2)]">
                            <Crown size={12} className="text-amber-300 fill-amber-300" /> Strategy Engine
                        </div>
                        <h3 className="text-3xl font-extrabold mb-3 tracking-tight text-white drop-shadow-md">Start New Strategy</h3>
                        <p className="text-slate-300 text-sm max-w-sm leading-relaxed font-medium">
                            {language === 'ko' 
                                ? 'R.C.A.T.E. 프레임워크를 사용하여 전문적인 클라이언트 전략을 설계하세요.' 
                                : 'Build a professional client strategy using the R.C.A.T.E. framework.'}
                        </p>
                    </div>
                    <div className="flex items-center gap-2 font-bold text-sm mt-8 group-hover:translate-x-2 transition-transform bg-white/10 w-fit px-5 py-3 rounded-xl backdrop-blur-md hover:bg-amber-500 hover:text-white border border-white/10 hover:border-amber-400 hover:shadow-lg text-amber-100">
                        Create Project <ArrowRight size={16} />
                    </div>
                </div>
            </div>

            {/* 2. Google Integration / Schedule Widget */}
            <div 
                className={`md:col-span-1 md:row-span-2 border rounded-[2rem] p-6 text-white group transition-all animate-slide-down shadow-lg flex flex-col relative overflow-hidden backdrop-blur-sm ${isGoogleConnected ? 'bg-slate-800/60 border-slate-600/50' : 'bg-slate-800/40 border-slate-700/50'}`}
                style={{ animationDelay: '0.1s' }}
            >
                {/* NOT CONNECTED STATE */}
                {!isGoogleConnected && (
                     <div className="absolute inset-0 z-10 flex flex-col items-center justify-center p-6 text-center bg-slate-900/90 backdrop-blur-sm">
                        <div className="w-16 h-16 bg-slate-800 rounded-2xl flex items-center justify-center mb-5 border border-slate-700 shadow-inner">
                            <CalendarIcon size={32} className="text-slate-400" />
                        </div>
                        <h3 className="text-white font-bold text-lg mb-2">Connect Workspace</h3>
                        <p className="text-slate-400 text-xs mb-8 leading-relaxed max-w-[200px]">
                            Sync your Google Calendar & Tasks to manage deadlines directly.
                        </p>
                        <button 
                            onClick={handleGoogleConnect}
                            disabled={isConnecting}
                            className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 text-white py-3.5 rounded-xl text-sm font-bold shadow-lg hover:shadow-emerald-500/30 transition-all flex items-center justify-center gap-2 border border-emerald-500/50"
                        >
                            {isConnecting ? <RefreshCw size={16} className="animate-spin" /> : <Link2 size={16} />}
                            {isConnecting ? "Connecting..." : "Connect Google"}
                        </button>
                     </div>
                )}

                {/* CONNECTED STATE HEADER */}
                <div className="flex items-center justify-between mb-5">
                     <div className="h-8 w-8 bg-indigo-500/20 rounded-lg flex items-center justify-center text-indigo-300 cursor-pointer hover:bg-indigo-500/30 transition-colors border border-indigo-500/20" onClick={openGoogleCalendar} title="Open Google Calendar">
                        <CalendarIcon size={16} />
                    </div>
                    <button onClick={openGoogleCalendar} className="text-[10px] font-bold bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 px-2 py-1 rounded transition-colors flex items-center gap-1 border border-slate-600">
                        <ExternalLink size={10} /> Open Cal
                    </button>
                </div>
                
                {/* Schedule Feed */}
                <div className="flex-1 overflow-y-auto max-h-[160px] pr-2 scrollbar-thin scrollbar-thumb-slate-600 mb-4">
                    {calendarEvents.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-full text-slate-500 space-y-3 py-6 border-2 border-dashed border-slate-700/50 rounded-xl bg-slate-800/30">
                            <CalendarIcon size={24} className="opacity-30"/>
                            <p className="text-[11px] text-center font-medium">일정이 없습니다.<br/>(No events)</p>
                        </div>
                    ) : (
                        calendarEvents.map((evt) => (
                            <a 
                                key={evt.id} 
                                href={evt.link} 
                                target="_blank" 
                                rel="noreferrer"
                                className={`block relative pl-4 border-l-2 transition-all hover:pl-5 group/evt mb-3 ${evt.status === 'active' ? 'border-amber-500' : 'border-slate-600'}`}
                            >
                                <span className="text-[10px] text-slate-400 font-mono block mb-0.5">{evt.time}</span>
                                <p className={`text-sm font-bold leading-tight ${evt.status === 'active' ? 'text-amber-200' : 'text-slate-300 group-hover/evt:text-white'}`}>{evt.title}</p>
                                <p className="text-[10px] text-slate-500 mt-0.5">{evt.subtitle}</p>
                            </a>
                        ))
                    )}
                </div>
                
                {/* Task Input & Progress */}
                <div className="pt-4 border-t border-slate-700/50 relative">
                    <div className="flex items-center justify-between text-xs text-slate-400 mb-3">
                        <div className="flex items-center gap-2 font-bold"><ListTodo size={14} /> <span>Tasks</span></div>
                        <span className="text-[10px] bg-slate-700 px-1.5 py-0.5 rounded text-slate-300">{completedTasks}/{totalTasks}</span>
                    </div>
                    
                    {/* Add Task Input */}
                    <form onSubmit={handleAddTask} className="flex gap-2 mb-3">
                        <input 
                            type="text" 
                            value={newTaskText} 
                            onChange={(e) => setNewTaskText(e.target.value)}
                            placeholder="Add new task..." 
                            className="flex-1 bg-slate-900/50 border border-slate-600 rounded-lg text-xs px-3 py-2 text-white placeholder:text-slate-600 focus:border-emerald-500 outline-none transition-colors"
                        />
                        <button type="submit" disabled={!newTaskText.trim()} className="bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg px-2 disabled:opacity-50 transition-colors">
                            <Plus size={16} />
                        </button>
                    </form>

                    {/* Task List */}
                    <div className="space-y-1 max-h-[120px] overflow-y-auto scrollbar-thin scrollbar-thumb-slate-600 pr-1">
                        {todoList.length === 0 && <p className="text-[10px] text-slate-600 text-center italic py-2">No active tasks.</p>}
                        {todoList.map(task => (
                            <div key={task.id} className="flex items-center justify-between group/task hover:bg-slate-700/50 rounded-lg px-2 py-1.5 transition-colors">
                                <button 
                                    onClick={() => toggleTodo(task.id)}
                                    className="flex items-center gap-3 text-left flex-1 overflow-hidden"
                                >
                                    {task.completed ? <CheckSquare size={14} className="text-emerald-500 flex-shrink-0" /> : <Square size={14} className="text-slate-500 group-hover/task:text-emerald-400 flex-shrink-0" />}
                                    <span className={`text-xs truncate transition-colors ${task.completed ? 'text-slate-500 line-through decoration-slate-600' : 'text-slate-300 group-hover/task:text-white'}`}>{task.text}</span>
                                </button>
                                <button onClick={() => deleteTodo(task.id)} className="text-slate-600 hover:text-red-400 opacity-0 group-hover/task:opacity-100 transition-opacity p-1">
                                    <Trash2 size={12} />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* 3. News Card 1 */}
            <div className="md:col-span-1 animate-slide-down" style={{ animationDelay: '0.2s' }}>
                <BriefingCard 
                    title={language === 'ko' ? "성공 사례 & 팁" : "Success Stories & Tips"} 
                    category="Tip" 
                    icon={<CheckCircle2 size={14} className="text-amber-500"/>} 
                    color="text-amber-300" 
                    items={localBriefing}
                    handleDiscuss={handleDiscuss}
                />
            </div>

            {/* 4. News Card 2 */}
            <div className="md:col-span-1 animate-slide-down" style={{ animationDelay: '0.3s' }}>
                <BriefingCard 
                    title={language === 'ko' ? "경제 동향" : "Economy"} 
                    category="Local" 
                    icon={<TrendingUp size={14} className="text-emerald-500"/>} 
                    color="text-emerald-300" 
                    items={localBriefing}
                    handleDiscuss={handleDiscuss}
                />
            </div>

             {/* 5. News Card 3 */}
             <div className="md:col-span-1 animate-slide-down" style={{ animationDelay: '0.4s' }}>
                <BriefingCard 
                    title="CPA News" 
                    category="CPA" 
                    icon={<BookOpen size={14} className="text-blue-500"/>} 
                    color="text-blue-300" 
                    items={localBriefing}
                    handleDiscuss={handleDiscuss}
                />
            </div>
            
            {/* 6. Method Card */}
            <div 
                onClick={() => onNavigate(Tab.FRAMEWORK)}
                className="md:col-span-1 bg-slate-800/40 backdrop-blur-md rounded-[2rem] p-6 text-white relative overflow-hidden group cursor-pointer shadow-lg hover:shadow-xl hover:bg-slate-800/60 transition-all border border-slate-600/50 hover:border-amber-500/30 animate-slide-down"
                style={{ animationDelay: '0.5s' }}
            >
                <div className="absolute -bottom-8 -right-8 text-slate-700 opacity-50 group-hover:scale-110 transition-transform duration-500">
                    <ShieldAlert size={120} />
                </div>
                <div className="relative z-10 flex flex-col h-full justify-between">
                    <div className="flex items-center gap-2 mb-2 text-slate-400 text-xs font-bold uppercase tracking-wider">
                        <BookOpen size={14} /> Methodology
                    </div>
                    <div>
                        <h3 className="text-xl font-bold mb-2 text-amber-100 group-hover:text-amber-300 transition-colors">R.C.A.T.E.</h3>
                        <p className="text-slate-400 text-xs leading-relaxed opacity-90 font-medium group-hover:text-slate-300">
                            Master the 5-step prompt engineering framework.
                        </p>
                    </div>
                    <div className="mt-6 flex items-center gap-1 text-xs font-bold text-amber-400 group-hover:text-amber-300 transition-colors">
                        Learn Framework <ChevronRight size={14} />
                    </div>
                </div>
            </div>

        </div>
    </div>
  );
};