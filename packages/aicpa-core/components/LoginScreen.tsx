import React, { useState, useEffect } from 'react';
import { ShieldCheck, User, AlertCircle, Key, ExternalLink, PlayCircle, Zap, Crown, Sparkles } from 'lucide-react';
import { AuthUser } from '../types';

interface LoginScreenProps {
  onLogin: (user: AuthUser) => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onLogin }) => {
  const [name, setName] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showKeyInput, setShowKeyInput] = useState(false);

  useEffect(() => {
    const init = async () => {
        const localKey = localStorage.getItem('gemini_api_key');
        if (localKey) {
            setApiKey(localKey);
            setShowKeyInput(true);
        } else {
            let hasEnvKey = false;
            try {
                if (typeof process !== 'undefined' && process.env && process.env.API_KEY) {
                    hasEnvKey = true;
                }
            } catch(e) {}

            const hasWindowAuth = window.aistudio && await window.aistudio.hasSelectedApiKey();

            if (!hasEnvKey && !hasWindowAuth) {
                setShowKeyInput(true);
            }
        }
    };
    init();
  }, []);

  const handleSignIn = async (e: React.FormEvent, isDemo: boolean = false) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    if (!name.trim()) {
        setError("이름을 입력해주세요.");
        setIsLoading(false);
        return;
    }

    try {
        if (!isDemo) {
            if (showKeyInput && apiKey.trim()) {
                localStorage.setItem('gemini_api_key', apiKey.trim());
            } else if (showKeyInput && !apiKey.trim()) {
                setError("API 키를 입력하거나 '게스트 체험'을 선택하세요.");
                setIsLoading(false);
                return;
            }
        }

        const user: AuthUser = {
            id: `user-${Date.now()}`,
            name: name.trim(),
            email: `${name.toLowerCase().replace(/\s/g, '.')}@aicpa.core`,
            isAuthenticated: true,
            avatarUrl: '' 
        };
        
        setTimeout(() => {
            onLogin(user);
        }, 800);

    } catch (err) {
        console.error(err);
        setError("로그인 중 오류가 발생했습니다.");
        setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center p-6 relative font-sans text-slate-900 overflow-hidden">
      
      {/* Background Decor with Gold Accents */}
      <div className="absolute inset-0 bg-slate-900 z-0">
          <div className="absolute inset-0 bg-gradient-to-b from-slate-900 via-[#0c1a24] to-slate-900"></div>
          <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] bg-emerald-600/20 rounded-full blur-[100px] opacity-60"></div>
          <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-teal-600/20 rounded-full blur-[100px] opacity-60"></div>
          {/* Gold Accent Orb */}
          <div className="absolute top-[20%] left-[15%] w-[300px] h-[300px] bg-amber-500/20 rounded-full blur-[80px] opacity-70 animate-pulse"></div>
          <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10 brightness-100 contrast-150"></div>
      </div>

      <div className="w-full max-w-[440px] flex flex-col items-center animate-fade-in relative z-10">
        
        {/* Logo Section */}
        <div className="mb-10 flex flex-col items-center text-center">
            <div className="w-24 h-24 bg-gradient-to-br from-emerald-600 to-teal-800 rounded-[2rem] flex items-center justify-center shadow-[0_0_40px_rgba(16,185,129,0.3)] mb-6 ring-4 ring-slate-800/50 border border-emerald-500/40 relative group">
                {/* Gold Sparkle on Logo */}
                <div className="absolute -top-2 -right-2 bg-gradient-to-br from-amber-300 to-amber-500 rounded-full p-2 shadow-lg border-2 border-slate-900 group-hover:scale-110 transition-transform">
                    <Crown size={14} className="text-white fill-white" />
                </div>
                <ShieldCheck size={48} className="text-white drop-shadow-md" />
            </div>
            <h1 className="text-4xl font-extrabold text-white tracking-tight leading-tight">
                AICPA <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-amber-300">Core</span>
            </h1>
            <p className="text-slate-400 text-sm mt-3 font-medium tracking-wide flex items-center gap-2">
                <Sparkles size={12} className="text-amber-400" />
                AI-Powered Strategy Workspace
                <Sparkles size={12} className="text-amber-400" />
            </p>
        </div>

        {/* Login Card */}
        <div className="w-full bg-white/90 rounded-[2rem] p-10 shadow-2xl border border-white/10 relative overflow-hidden backdrop-blur-xl ring-1 ring-white/20">
             
             {/* Gold Top Border Accent */}
             <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-emerald-500 via-amber-400 to-emerald-500"></div>

             <form onSubmit={(e) => handleSignIn(e, false)} className="space-y-6 mt-2">
                 
                 {/* Name Input */}
                 <div className="space-y-2">
                    <label className="text-[11px] font-bold text-slate-500 uppercase ml-1 flex items-center gap-1 tracking-wide">
                        Display Name <span className="text-amber-500">*</span>
                    </label>
                    <div className="relative group">
                        <div className="absolute left-4 top-4 text-slate-400 group-focus-within:text-emerald-600 transition-colors">
                            <User size={20} />
                        </div>
                        <input 
                            type="text" 
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Your Name or Firm"
                            className="w-full pl-12 pr-4 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 transition-all outline-none font-bold text-slate-800 placeholder:text-slate-400 text-sm"
                            autoFocus
                        />
                    </div>
                 </div>

                 {/* API Key Input */}
                 {showKeyInput && (
                     <div className="space-y-2 animate-slide-down">
                        <div className="flex justify-between items-center ml-1">
                            <label className="text-[11px] font-bold text-slate-500 uppercase flex items-center gap-1 tracking-wide">
                                Google Gemini API Key
                            </label>
                            <a 
                                href="https://aistudio.google.com/app/apikey" 
                                target="_blank" 
                                rel="noreferrer"
                                className="text-[10px] text-amber-600 font-bold hover:underline flex items-center gap-1 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-100"
                            >
                                Get Key <ExternalLink size={8} />
                            </a>
                        </div>
                        <div className="relative group">
                            <div className="absolute left-4 top-4 text-slate-400 group-focus-within:text-purple-500 transition-colors">
                                <Key size={20} />
                            </div>
                            <input 
                                type="password" 
                                value={apiKey}
                                onChange={(e) => setApiKey(e.target.value)}
                                placeholder="Paste your key here"
                                className="w-full pl-12 pr-4 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-purple-500 focus:ring-4 focus:ring-purple-500/10 transition-all outline-none font-mono text-xs text-slate-900 placeholder:text-slate-400"
                            />
                        </div>
                     </div>
                 )}

                 {/* Sign In Button */}
                 <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-4 px-4 rounded-2xl transition-all active:scale-[0.98] shadow-xl shadow-emerald-600/20 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2.5 mt-4 group relative overflow-hidden"
                 >
                    {/* Button Shine Effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                    
                    {isLoading ? (
                        <div className="flex items-center gap-2">
                             <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                             <span>Authenticating...</span>
                        </div>
                    ) : (
                        <>
                            <span>{showKeyInput ? 'Initialize Workspace' : 'Enter Workspace'}</span>
                            <Zap size={18} className="text-amber-200 group-hover:text-white transition-colors" />
                        </>
                    )}
                </button>

                 {/* Guest Mode Link */}
                 <div className="relative flex py-2 items-center">
                    <div className="flex-grow border-t border-slate-200"></div>
                    <span className="flex-shrink-0 mx-4 text-slate-400 text-[10px] font-medium uppercase tracking-widest">or</span>
                    <div className="flex-grow border-t border-slate-200"></div>
                 </div>

                 <button
                    type="button"
                    onClick={(e) => handleSignIn(e, true)}
                    className="w-full bg-white border border-slate-200 hover:bg-amber-50 hover:border-amber-200 hover:text-amber-700 text-slate-600 font-bold py-3.5 px-4 rounded-2xl transition-all flex items-center justify-center gap-2 text-xs group"
                 >
                    <PlayCircle size={16} className="text-slate-400 group-hover:text-amber-500 transition-colors" />
                    Guest Mode (No API Key)
                 </button>

                 {/* Error Message */}
                 {error && (
                    <div className="flex items-center gap-2 text-rose-600 bg-rose-50 px-4 py-3 rounded-2xl text-xs font-bold animate-fade-in border border-rose-100">
                        <AlertCircle size={16} className="flex-shrink-0" /> {error}
                    </div>
                 )}
             </form>
        </div>
        
        <div className="mt-8 text-center text-slate-500 text-[10px] max-w-xs leading-relaxed opacity-70">
            <p>Professional Grade Security. Local Key Storage.</p>
        </div>

      </div>
    </div>
  );
};