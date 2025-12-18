import React, { useState, useEffect } from 'react';
import { HeroSection } from './components/HeroSection';
import { FrameworkExplainer } from './components/FrameworkExplainer';
import { PromptGenerator } from './components/PromptGenerator';
import { ChatWidget } from './components/ChatWidget';
import { LoginScreen } from './components/LoginScreen';
import { KnowledgeBase } from './components/KnowledgeBase';
import { SimulationWizard } from './components/SimulationWizard';
import { GroupChatRoom } from './components/GroupChatRoom';
import { CalculatorWidget } from './components/CalculatorWidget';
import { AgentBrowser } from './components/AgentBrowser';
import { CPADashboard } from './components/CPADashboard';
import { Tab } from './types';
import { LayoutDashboard, BookOpen, PenTool, Menu, X, FolderKanban, LogOut, MessageCircle, Calculator, Zap, AlertCircle, CheckCircle, Info, Trash2, Clock, Calendar, Bot, Shield } from 'lucide-react';
import { AppProvider, useApp } from './context/AppContext';

// ... (omitting intermediate code for brevity in tool call, focusing on changes)

  const renderContent = () => {
    return (
      <div className="animate-fade-in relative z-0">
        {currentTab === Tab.HOME && <HeroSection onNavigate={setCurrentTab} />}
        {currentTab === Tab.FRAMEWORK && <FrameworkExplainer />}
        {currentTab === Tab.GENERATOR && <PromptGenerator />}
        {currentTab === Tab.KNOWLEDGE && (
            <KnowledgeBase 
                folders={knowledgeFolders}
                setFolders={setKnowledgeFolders}
                activeFolderId={activeFolderId}
                setActiveFolderId={setActiveFolderId}
                user={user}
                onGenerateStrategy={(data) => {
                    setRcateData(data);
                    setCurrentTab(Tab.GENERATOR);
                }}
            />
        )}
        {currentTab === Tab.WIZARD && (
            <SimulationWizard 
                onComplete={(data) => {
                    setRcateData(data);
                    setCurrentTab(Tab.GENERATOR);
                }}
                onCancel={() => setCurrentTab(Tab.HOME)}
            />
        )}
        {currentTab === Tab.COMMUNITY && (
            <GroupChatRoom 
                knowledgeFolders={knowledgeFolders}
                setKnowledgeFolders={setKnowledgeFolders}
            />
        )}
        {currentTab === Tab.CPA && <CPADashboard />}
      </div>
    );
  };

  const NAV_ITEMS = [
      { t: Tab.HOME, l: 'Home', d: 'Dashboard', i: <LayoutDashboard size={18} /> },
      { t: Tab.CPA, l: 'CPA Mode', d: 'Financial Health', i: <Shield size={18} /> },
      { t: Tab.KNOWLEDGE, l: 'Clients', d: 'Documents', i: <FolderKanban size={18} /> },
      { t: Tab.COMMUNITY, l: 'Team', d: 'Collaboration', i: <MessageCircle size={18} /> },
      { t: Tab.GENERATOR, l: 'Prompt', d: 'Builder', i: <PenTool size={18} /> },
  ];
const ToastNotification = () => {
    const { notification, closeNotification } = useApp();
    if (!notification) return null;

    const bgColors = {
        success: 'bg-emerald-600',
        error: 'bg-rose-600',
        warning: 'bg-amber-500',
        info: 'bg-blue-600'
    };

    const icons = {
        success: <CheckCircle size={20} />,
        error: <AlertCircle size={20} />,
        warning: <AlertCircle size={20} />,
        info: <Info size={20} />
    };

    return (
        <div className={`fixed bottom-24 left-1/2 transform -translate-x-1/2 z-[100] flex items-center gap-3 px-6 py-3.5 rounded-full shadow-2xl text-white animate-fade-in ${bgColors[notification.type]} backdrop-blur-md bg-opacity-95 ring-1 ring-white/10`}>
            {icons[notification.type]}
            <span className="font-medium text-sm tracking-wide">{notification.message}</span>
            <button onClick={closeNotification} className="ml-2 hover:bg-white/20 rounded-full p-1 transition-colors"><X size={14}/></button>
        </div>
    );
};

// --- Top Bar Clock Component ---
const GlobalClock = ({ isDark }: { isDark: boolean }) => {
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => setTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    const dateStr = time.toLocaleDateString('ko-KR', { month: 'long', day: 'numeric', weekday: 'short' });
    const timeStr = time.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' });

    return (
        <div className={`hidden lg:flex items-center gap-3 px-4 py-2 rounded-xl text-xs font-mono shadow-sm border transition-colors ${isDark ? 'bg-slate-800/50 border-slate-700 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-600'}`}>
            <div className={`flex items-center gap-2 border-r pr-3 ${isDark ? 'border-slate-600' : 'border-slate-200'}`}>
                <Calendar size={12} className="text-amber-400"/>
                <span className="font-semibold">{dateStr}</span>
            </div>
            <div className="flex items-center gap-2">
                <Clock size={12} className="text-amber-400"/>
                <span className={`font-bold ${isDark ? 'text-white' : 'text-slate-800'}`}>{timeStr}</span>
            </div>
        </div>
    );
};

const AppContent: React.FC = () => {
  const { 
    user, setUser, 
    currentTab, setCurrentTab, 
    knowledgeFolders, setKnowledgeFolders,
    setRcateData,
    calculatorTotal, toggleCalculator, isCalculatorOpen,
    resetApp
  } = useApp();

  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeFolderId, setActiveFolderId] = useState<string | null>(null);

  const isHero = currentTab === Tab.HOME;

  const renderContent = () => {
    return (
      <div className="animate-fade-in relative z-0">
        {currentTab === Tab.HOME && <HeroSection onNavigate={setCurrentTab} />}
        {currentTab === Tab.FRAMEWORK && <FrameworkExplainer />}
        {currentTab === Tab.GENERATOR && <PromptGenerator />}
        {currentTab === Tab.KNOWLEDGE && (
            <KnowledgeBase 
                folders={knowledgeFolders}
                setFolders={setKnowledgeFolders}
                activeFolderId={activeFolderId}
                setActiveFolderId={setActiveFolderId}
                user={user}
                onGenerateStrategy={(data) => {
                    setRcateData(data);
                    setCurrentTab(Tab.GENERATOR);
                }}
            />
        )}
        {currentTab === Tab.WIZARD && (
            <SimulationWizard 
                onComplete={(data) => {
                    setRcateData(data);
                    setCurrentTab(Tab.GENERATOR);
                }}
                onCancel={() => setCurrentTab(Tab.HOME)}
            />
        )}
        {currentTab === Tab.COMMUNITY && (
            <GroupChatRoom 
                knowledgeFolders={knowledgeFolders}
                setKnowledgeFolders={setKnowledgeFolders}
            />
        )}
      </div>
    );
  };

  const NAV_ITEMS = [
      { t: Tab.HOME, l: 'Home', d: 'Dashboard', i: <LayoutDashboard size={18} /> },
      { t: Tab.KNOWLEDGE, l: 'Clients', d: 'Documents', i: <FolderKanban size={18} /> },
      { t: Tab.COMMUNITY, l: 'Team', d: 'Collaboration', i: <MessageCircle size={18} /> },
      { t: Tab.GENERATOR, l: 'Prompt', d: 'Builder', i: <PenTool size={18} /> },
  ];

  if (!user) return <LoginScreen onLogin={setUser} />;

  return (
    <div className={`min-h-screen font-sans relative text-slate-900 overflow-x-hidden selection:bg-amber-200 selection:text-amber-900`}>
      
      {/* Background Logic: Fixed to ensure Home is Dark/Gold */}
      <div className="fixed inset-0 z-[-1]">
          {isHero ? (
              // Dark Luxury Background for Home
              <div className="absolute inset-0 bg-slate-900">
                  <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-[#0a1f1c] to-slate-900"></div>
                  <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-amber-500/10 rounded-full blur-[120px] mix-blend-screen opacity-60"></div>
                  <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-emerald-600/10 rounded-full blur-[120px] mix-blend-screen opacity-60"></div>
                  <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150"></div>
              </div>
          ) : (
              // Clean Light Background for Tools
              <div className="absolute inset-0 bg-slate-50">
                  <div className="absolute inset-0 bg-grid-subtle opacity-60"></div>
              </div>
          )}
      </div>

      {/* Navbar */}
      <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 border-b h-18 sm:h-20 ${isHero ? 'bg-slate-900/80 border-slate-700/50 backdrop-blur-md' : 'bg-white/90 border-slate-200/60 backdrop-blur-md'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex justify-between items-center">
            
            {/* LOGO */}
            <div 
                className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity group" 
                onClick={() => setCurrentTab(Tab.HOME)}
            >
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-600 to-teal-700 flex items-center justify-center shadow-lg shadow-emerald-900/20 group-hover:scale-105 transition-transform border border-emerald-500/30">
                    <Zap size={20} className="text-amber-300 fill-amber-300"/>
                </div>
                <div>
                    <span className={`block text-lg font-bold tracking-tight leading-none ${isHero ? 'text-white' : 'text-slate-900'}`}>
                        AICPA <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-amber-300">Core</span>
                    </span>
                    <span className="text-[10px] text-slate-500 font-medium tracking-wider group-hover:text-emerald-500 transition-colors">INTELLIGENCE SUITE</span>
                </div>
            </div>
            
            {/* Desktop Nav */}
            <nav className={`hidden md:flex items-center gap-2 p-1.5 rounded-2xl border ${isHero ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-100/50 border-slate-200/50'}`}>
                {NAV_ITEMS.map(item => (
                    <button
                        key={item.t}
                        onClick={() => setCurrentTab(item.t)}
                        className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
                            currentTab === item.t 
                                ? 'bg-white text-emerald-700 shadow-sm ring-1 ring-black/5' 
                                : (isHero ? 'text-slate-400 hover:text-white hover:bg-white/10' : 'text-slate-500 hover:text-slate-900 hover:bg-white/50')
                        }`}
                    >
                        {item.i}
                        {item.l}
                    </button>
                ))}
            </nav>

            {/* Right Actions */}
            <div className="flex items-center gap-3">
                {/* STATUS INDICATORS */}
                <div className="hidden lg:flex items-center gap-2 mr-2">
                     {/* Trinity Connection */}
                     <div className="flex items-center gap-1.5 px-2 py-1 bg-emerald-50 border border-emerald-100 rounded-lg text-[10px] font-bold text-emerald-700 animate-pulse">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500"></div>
                        TRINITY LINK
                     </div>
                     {/* Active Scholar (Mock for now, will link to state later) */}
                     <div className="flex items-center gap-1.5 px-2 py-1 bg-slate-50 border border-slate-100 rounded-lg text-[10px] font-bold text-slate-500">
                        <Bot size={10} />
                        READY
                     </div>
                </div>

                <GlobalClock isDark={isHero} />
                
                <button 
                    onClick={toggleCalculator}
                    className={`hidden sm:flex items-center gap-2 px-3 py-2 rounded-xl border transition-all ${
                        isCalculatorOpen 
                        ? 'bg-amber-50 border-amber-200 text-amber-700 shadow-sm' 
                        : (isHero ? 'bg-slate-800/50 border-slate-700 text-slate-300 hover:bg-slate-700' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50')
                    }`}
                >
                    <Calculator size={18} className="text-amber-500" />
                    <span className="text-sm font-mono font-bold">
                        ${calculatorTotal.toLocaleString()}
                    </span>
                </button>

                <div className={`h-8 w-px mx-1 hidden sm:block ${isHero ? 'bg-slate-700' : 'bg-slate-200'}`}></div>

                <div className="flex items-center gap-3 pl-1">
                    <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-amber-200 via-amber-300 to-yellow-400 p-[2px] shadow-sm">
                        <div className="w-full h-full rounded-[14px] bg-white flex items-center justify-center text-amber-700 font-bold text-sm">
                            {user.name.charAt(0)}
                        </div>
                    </div>
                </div>
                
                <button 
                    onClick={() => setIsMenuOpen(true)} 
                    className={`md:hidden p-2 rounded-xl ${isHero ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-100'}`}
                >
                    <Menu size={24} />
                </button>
            </div>
        </div>
      </header>

      {/* Mobile Menu */}
      {isMenuOpen && (
          <div className="fixed inset-0 z-[60] bg-slate-900/60 backdrop-blur-sm flex justify-end">
             <div className="w-4/5 max-w-xs bg-white h-full shadow-2xl flex flex-col rounded-l-3xl overflow-hidden animate-slide-right">
                <div className="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
                   <span className="font-bold text-lg text-slate-800">Menu</span>
                   <button onClick={() => setIsMenuOpen(false)} className="p-2 bg-slate-100 rounded-full text-slate-600 hover:bg-slate-200"><X size={20}/></button>
                </div>
                <div className="p-4 space-y-2">
                   {NAV_ITEMS.map(item => (
                      <button
                         key={item.t}
                         onClick={() => { setCurrentTab(item.t); setIsMenuOpen(false); }}
                         className={`w-full flex items-center gap-4 p-4 rounded-2xl transition-all ${
                             currentTab === item.t 
                             ? 'bg-emerald-50 text-emerald-700' 
                             : 'text-slate-600 hover:bg-slate-50'
                         }`}
                      >
                         <div className={`p-2 rounded-xl ${currentTab === item.t ? 'bg-white shadow-sm' : 'bg-slate-100'}`}>{item.i}</div>
                         <div className="flex flex-col items-start">
                             <span className="font-bold text-sm">{item.l}</span>
                             <span className="text-[10px] text-slate-400 font-medium">{item.d}</span>
                         </div>
                      </button>
                   ))}
                </div>
                <div className="mt-auto p-6 border-t border-slate-100 space-y-3 bg-slate-50/50">
                    <button onClick={resetApp} className="flex items-center gap-3 text-slate-500 hover:bg-white w-full p-4 rounded-2xl transition-all font-medium text-sm border border-transparent hover:border-slate-200 hover:shadow-sm">
                        <Trash2 size={18} /> Reset All Data
                    </button>
                    <button onClick={() => setUser(null)} className="flex items-center gap-3 text-red-600 hover:bg-red-50 w-full p-4 rounded-2xl transition-all font-medium text-sm border border-transparent hover:border-red-100">
                        <LogOut size={18} /> Sign Out
                    </button>
                </div>
             </div>
          </div>
      )}

      <main className="pt-24 sm:pt-28 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto h-full relative z-10"> 
        {renderContent()}
      </main>
      
      <ChatWidget />
      <CalculatorWidget />
      <AgentBrowser />
      <ToastNotification />
    </div>
  );
};

export default function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}