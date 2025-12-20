import React, { useState, useMemo, useCallback } from 'react';
import { RcateData, Template, TemplateVariable } from '../types';
import { 
    Zap, Sparkles, Terminal, PlayCircle, Wand2, 
    ChevronRight, Layout, Settings2, CheckCircle2, AlertTriangle, 
    TrendingUp, FileText, Briefcase, RefreshCw, Layers, RotateCcw,
    Save, X, Trash2, Bookmark, Quote, Plus, GripVertical, Crown
} from 'lucide-react';
import { runAgentDrafting, runAgentManagerReview, generateFieldOptions, optimizeRcatePrompt } from '../services/geminiService';
import { useApp } from '../context/AppContext';
import { ASSET_TEMPLATES } from '../assets'; 

// --- TYPES & INTERFACES ---
interface ReviewResult {
    score: number;
    summary: string;
    strengths: string[];
    weaknesses: string[];
    refined_suggestion: string;
}

// --- SUB-COMPONENTS ---

const SectionHeader: React.FC<{ title: string; icon: React.ReactNode; description?: string }> = ({ title, icon, description }) => (
    <div className="mb-5">
        <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
            {icon} {title}
        </h3>
        {description && <p className="text-xs text-slate-500 mt-1.5 ml-6 leading-relaxed">{description}</p>}
    </div>
);

const ScoreGauge: React.FC<{ score: number }> = ({ score }) => {
    const radius = 32;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;
    
    let color = 'stroke-rose-500';
    if (score > 60) color = 'stroke-emerald-500';
    if (score > 85) color = 'stroke-amber-400'; // Gold for high scores

    return (
        <div className="relative flex items-center justify-center w-24 h-24">
            <svg className="transform -rotate-90 w-24 h-24">
                <circle cx="48" cy="48" r={radius} stroke="#e2e8f0" strokeWidth="6" fill="transparent" />
                <circle cx="48" cy="48" r={radius} strokeLinecap="round" strokeWidth="6" fill="transparent" className={`transition-all duration-1000 ease-out ${color}`} strokeDasharray={circumference} strokeDashoffset={offset} />
            </svg>
            <div className="absolute flex flex-col items-center">
                <span className="text-2xl font-bold text-slate-800">{score}</span>
                <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Score</span>
            </div>
        </div>
    );
};

export const PromptGenerator: React.FC = () => {
  const { rcateData, setRcateData, showNotification, userTemplates, saveUserTemplate, deleteUserTemplate } = useApp();
  
  // UI State
  const [activeTab, setActiveTab] = useState<'DESIGN' | 'SIMULATION'>('DESIGN');
  const [showVariables, setShowVariables] = useState(false);
  const [activeVariables, setActiveVariables] = useState<TemplateVariable[]>([]);
  
  // Save Template Modal State
  const [isSaveModalOpen, setIsSaveModalOpen] = useState(false);
  const [newTemplateName, setNewTemplateName] = useState('');
  const [newTemplateCategory, setNewTemplateCategory] = useState('Strategic Analysis');
  const [newTemplateDesc, setNewTemplateDesc] = useState('');
  
  // Logic State
  const [loading, setLoading] = useState(false);
  const [fieldLoading, setFieldLoading] = useState<string | null>(null);
  const [simulationState, setSimulationState] = useState<'IDLE' | 'DRAFTING' | 'REVIEWING' | 'DONE' | 'ERROR'>('IDLE');
  const [draftContent, setDraftContent] = useState('');
  const [reviewResult, setReviewResult] = useState<ReviewResult | null>(null);

  // Optimization: Memoize combined templates
  const allTemplates = useMemo(() => {
      // User templates first, then System templates
      return [...userTemplates.reverse(), ...ASSET_TEMPLATES];
  }, [userTemplates]);

  // --- HANDLERS ---

  const handleInputChange = useCallback((field: keyof RcateData, value: string) => {
    setRcateData(p => ({ ...p, [field]: value }));
  }, [setRcateData]);

  const handleMagicOptimize = async () => {
      setLoading(true);
      try {
          const optimized = await optimizeRcatePrompt(rcateData);
          if (optimized) {
              setRcateData(optimized);
              showNotification("전략이 전문가 수준으로 최적화되었습니다.", "success");
          }
      } catch (e) {
          showNotification("최적화 실패. 잠시 후 다시 시도해주세요.", "error");
      } finally {
          setLoading(false);
      }
  };

  const handleSuggest = async (f: keyof RcateData) => {
      setFieldLoading(f);
      try {
        const opts = await generateFieldOptions(f, rcateData);
        if(opts.length > 0) handleInputChange(f, opts[0]); 
      } finally {
        setFieldLoading(null);
      }
  };

  const handleTemplateSelect = (t: Template) => {
      let processedContext = t.data.context;
      
      // Robust Variable Replacement
      t.variables.forEach(v => {
          const regex = new RegExp(`{{${v.key}}}`, 'g');
          processedContext = processedContext.replace(regex, v.value);
      });

      setRcateData({ ...t.data, context: processedContext });
      setActiveVariables(t.variables);
      setShowVariables(true);
      showNotification(`"${t.name}" 템플릿이 적용되었습니다.`, 'success');
  };

  const handleSaveTemplate = () => {
      if (!newTemplateName.trim()) {
          showNotification('템플릿 이름을 입력해주세요.', 'warning');
          return;
      }
      const newTemplate: Template = {
          id: `user-${Date.now()}`,
          name: newTemplateName,
          category: newTemplateCategory,
          description: newTemplateDesc,
          data: { ...rcateData },
          variables: [], // Currently snapshot-only
          isUserCreated: true,
          badge: 'Custom'
      };
      saveUserTemplate(newTemplate);
      setIsSaveModalOpen(false);
      
      // Reset Form
      setNewTemplateName('');
      setNewTemplateDesc('');
      setNewTemplateCategory('Strategic Analysis');
      
      showNotification("나만의 전략 템플릿이 저장되었습니다.", "success");
  };

  const runSimulation = async () => {
      setActiveTab('SIMULATION');
      setSimulationState('DRAFTING');
      setDraftContent('');
      setReviewResult(null);

      try {
          // Step 1: Drafting (Stream)
          let fullDraft = "";
          for await (const chunk of runAgentDrafting(rcateData)) {
              fullDraft += chunk;
              setDraftContent(fullDraft);
          }
          
          setSimulationState('REVIEWING');

          // Step 2: Reviewing (Structured)
          const review = await runAgentManagerReview(fullDraft);
          setReviewResult(review);
          
          setSimulationState('DONE');
      } catch (e) {
          setSimulationState('ERROR');
          showNotification("시뮬레이션 중 오류가 발생했습니다.", "error");
      }
  };

  const renderInput = (field: keyof RcateData, label: string, rows: number = 3) => (
      <div className="relative group">
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wide flex items-center gap-1.5">
                {label}
            </label>
            <button 
                onClick={() => handleSuggest(field)} 
                className="opacity-0 group-hover:opacity-100 transition-all duration-200 text-[10px] flex items-center gap-1 text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full hover:bg-amber-100 font-medium border border-amber-200 shadow-sm"
                disabled={fieldLoading === field}
            >
                {fieldLoading === field ? <RefreshCw size={10} className="animate-spin"/> : <Sparkles size={10}/>} AI Suggestion
            </button>
          </div>
          <textarea
              value={rcateData[field]}
              onChange={(e) => handleInputChange(field, e.target.value)}
              className="w-full bg-slate-50 hover:bg-white focus:bg-white border border-slate-200 rounded-[1.2rem] p-4 text-sm focus:ring-4 focus:ring-emerald-500/10 focus:border-emerald-500 transition-all resize-none font-medium text-slate-800 leading-relaxed shadow-sm placeholder:text-slate-400"
              rows={rows}
              placeholder={`Enter ${field}...`}
          />
      </div>
  );

  return (
    <div className="flex flex-col h-full bg-[#f8fafc] relative overflow-hidden font-sans">
        
        {/* --- SAVE TEMPLATE MODAL (Mira Style + Gold) --- */}
        {isSaveModalOpen && (
            <div className="fixed inset-0 z-[60] bg-slate-900/20 backdrop-blur-sm flex items-center justify-center p-4">
                <div className="bg-white rounded-[2rem] shadow-2xl w-full max-w-md p-8 animate-slide-up ring-1 ring-slate-900/5">
                    <div className="flex justify-between items-start mb-8">
                        <div className="flex items-center gap-4">
                            <div className="bg-amber-50 p-3 rounded-2xl text-amber-600 shadow-sm border border-amber-100">
                                <Bookmark size={24} strokeWidth={2.5} />
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-slate-900 leading-tight">Save Template</h3>
                                <p className="text-xs text-slate-500 font-medium mt-1">Save current strategy configuration</p>
                            </div>
                        </div>
                        <button onClick={() => setIsSaveModalOpen(false)} className="text-slate-400 hover:text-slate-600 p-2 hover:bg-slate-50 rounded-full transition-colors">
                            <X size={20} />
                        </button>
                    </div>
                    
                    <div className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide ml-1">Template Name</label>
                            <input 
                                type="text" 
                                value={newTemplateName}
                                onChange={(e) => setNewTemplateName(e.target.value)}
                                placeholder="e.g. 2025 Audit Plan - Tech Corp"
                                className="w-full border border-slate-200 bg-slate-50 rounded-xl p-3.5 text-sm focus:bg-white focus:ring-4 focus:ring-amber-500/10 focus:border-amber-500 outline-none transition-all font-medium"
                                autoFocus
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide ml-1">Category</label>
                            <div className="relative">
                                <input 
                                    type="text"
                                    list="category-suggestions"
                                    value={newTemplateCategory}
                                    onChange={(e) => setNewTemplateCategory(e.target.value)}
                                    className="w-full border border-slate-200 bg-slate-50 rounded-xl p-3.5 text-sm focus:bg-white focus:ring-4 focus:ring-emerald-500/10 focus:border-emerald-500 outline-none transition-all"
                                />
                                <datalist id="category-suggestions">
                                    <option value="Strategic Analysis" />
                                    <option value="Compliance Review" />
                                    <option value="Audit Plan" />
                                    <option value="Tax Advisory" />
                                </datalist>
                            </div>
                        </div>
                        <div className="space-y-2">
                            <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide ml-1">Description</label>
                            <textarea 
                                value={newTemplateDesc}
                                onChange={(e) => setNewTemplateDesc(e.target.value)}
                                placeholder="Briefly describe the purpose..."
                                className="w-full border border-slate-200 bg-slate-50 rounded-xl p-3.5 text-sm focus:bg-white focus:ring-4 focus:ring-emerald-500/10 focus:border-emerald-500 outline-none resize-none h-24 transition-all"
                            />
                        </div>
                    </div>

                    <div className="flex gap-3 mt-10">
                        <button onClick={() => setIsSaveModalOpen(false)} className="flex-1 py-3.5 border border-slate-200 bg-white rounded-xl text-slate-600 font-bold text-sm hover:bg-slate-50 transition-colors">
                            Cancel
                        </button>
                        <button onClick={handleSaveTemplate} className="flex-1 py-3.5 bg-emerald-600 text-white rounded-xl font-bold text-sm hover:bg-emerald-700 shadow-lg shadow-emerald-500/30 transition-all transform active:scale-[0.98] flex items-center justify-center gap-2">
                            <Save size={18} /> Save Template
                        </button>
                    </div>
                </div>
            </div>
        )}

        {/* --- HEADER --- */}
        <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 px-6 py-3 flex justify-between items-center z-20 sticky top-0">
            <div>
                <h1 className="text-lg font-extrabold text-slate-900 flex items-center gap-2 tracking-tight">
                    <Terminal size={20} className="text-emerald-600 fill-emerald-100"/> 
                    Strategy Workstation
                </h1>
            </div>
            
            <div className="flex items-center gap-3">
                <div className="flex bg-slate-100/50 p-1 rounded-2xl border border-slate-200/50">
                    <button 
                        onClick={() => setActiveTab('DESIGN')}
                        className={`px-5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${activeTab === 'DESIGN' ? 'bg-white text-emerald-700 shadow-sm ring-1 ring-black/5' : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50'}`}
                    >
                        <Layout size={14}/> Design
                    </button>
                    <button 
                        onClick={() => setActiveTab('SIMULATION')}
                        className={`px-5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${activeTab === 'SIMULATION' ? 'bg-white text-purple-700 shadow-sm ring-1 ring-black/5' : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50'}`}
                    >
                        <PlayCircle size={14}/> Run
                    </button>
                </div>
                
                <div className="w-px h-6 bg-slate-200 mx-2"></div>

                <button 
                    onClick={() => setIsSaveModalOpen(true)}
                    className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-amber-50 text-slate-600 hover:text-amber-700 rounded-xl transition-all border border-slate-200 hover:border-amber-200 text-xs font-bold group shadow-sm hover:shadow"
                    title="Save Current Strategy"
                >
                    <Save size={14} className="group-hover:scale-110 transition-transform"/>
                    Save
                </button>

                <button 
                    onClick={() => setShowVariables(!showVariables)}
                    className={`p-2.5 rounded-xl transition-all border shadow-sm ${showVariables ? 'bg-emerald-50 text-emerald-600 border-emerald-200' : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-500'}`}
                    title="Templates & Variables"
                >
                    <Settings2 size={18}/>
                </button>
            </div>
        </header>

        {/* --- MAIN CONTENT SPLIT --- */}
        <div className="flex-1 flex overflow-hidden">
            
            {/* LEFT: INPUTS (DESIGN) */}
            <div className={`flex-1 overflow-y-auto p-6 transition-all duration-300 ${activeTab === 'SIMULATION' ? 'hidden md:block md:w-1/3 md:flex-none border-r border-slate-200' : 'w-full'}`}>
                
                {/* --- TEMPLATE & VARIABLE PANEL --- */}
                {showVariables && (
                    <div className="mb-8 animate-slide-down bg-white p-6 rounded-[2rem] border border-slate-200 shadow-sm ring-1 ring-slate-100/50">
                        <SectionHeader title="Templates & Variables" icon={<Layers size={16} className="text-slate-600"/>} />
                        
                        {/* Templates Horizontal List */}
                        <div className="flex gap-4 overflow-x-auto pb-4 mb-4 scrollbar-hide snap-x p-1">
                            {allTemplates.map(t => (
                                <div key={t.id} className="snap-start relative group flex-shrink-0 w-[200px]">
                                    <button 
                                        onClick={() => handleTemplateSelect(t)} 
                                        className={`w-full text-left p-5 rounded-[1.5rem] border transition-all duration-300 flex flex-col gap-3 h-full relative overflow-hidden ${
                                            t.isUserCreated 
                                            ? 'bg-amber-50/50 border-amber-100 hover:border-amber-300 hover:shadow-amber-100 hover:shadow-md' 
                                            : 'bg-white border-slate-200 hover:border-blue-300 hover:shadow-md'
                                        }`}
                                    >
                                        <div className="flex justify-between items-start w-full relative z-10">
                                            <span className={`text-[10px] font-bold px-2.5 py-1 rounded-lg tracking-wide uppercase ${
                                                t.isUserCreated ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-600'
                                            }`}>
                                                {t.category}
                                            </span>
                                        </div>
                                        <div className="relative z-10">
                                            <span className="font-bold text-sm text-slate-800 line-clamp-2 leading-snug">{t.name}</span>
                                            {t.description && <p className="text-[10px] text-slate-500 mt-2 line-clamp-2 leading-relaxed">{t.description}</p>}
                                        </div>
                                        
                                        {/* Decorative Icon for User Templates */}
                                        {t.isUserCreated && (
                                            <Bookmark className="absolute -bottom-4 -right-4 text-amber-100/80 w-24 h-24 opacity-50 rotate-[-15deg]" strokeWidth={1} />
                                        )}
                                    </button>
                                    
                                    {t.isUserCreated && (
                                        <button 
                                            onClick={(e) => { e.stopPropagation(); deleteUserTemplate(t.id); }}
                                            className="absolute -top-2 -right-2 bg-white rounded-full p-2 text-slate-400 hover:text-red-500 shadow-lg border border-slate-100 opacity-0 group-hover:opacity-100 transition-all hover:scale-110 z-20"
                                            title="Delete Template"
                                        >
                                            <Trash2 size={14} />
                                        </button>
                                    )}
                                </div>
                            ))}
                        </div>

                        {/* Active Variables Display */}
                        {activeVariables.length > 0 ? (
                            <div className="bg-slate-50/50 rounded-[1.5rem] p-5 border border-slate-200/50">
                                <h4 className="text-[10px] font-bold text-slate-400 uppercase mb-4 flex items-center gap-1.5 pl-1">
                                    <Quote size={12} className="text-slate-400" /> Smart Variables
                                </h4>
                                <div className="grid grid-cols-2 gap-x-6 gap-y-4">
                                    {activeVariables.map((v, i) => (
                                        <div key={i} className="group/var">
                                            <label className="text-[10px] font-bold text-slate-500 mb-1.5 block group-hover/var:text-emerald-600 transition-colors uppercase tracking-wide">{v.label}</label>
                                            <div className="text-xs font-mono font-medium text-slate-800 border-b border-slate-200 py-1.5 bg-transparent">{v.value}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                             <p className="text-xs text-slate-400 font-medium text-center py-4 bg-slate-50 rounded-2xl border border-dashed border-slate-200">
                                 Select a template to view adjustable variables.
                             </p>
                        )}
                    </div>
                )}

                <div className="space-y-8 max-w-3xl mx-auto pb-24">
                    {/* Optimize Banner */}
                    <div className="bg-gradient-to-br from-emerald-600 to-teal-700 rounded-[2rem] p-8 text-white shadow-xl shadow-emerald-900/10 relative overflow-hidden group border border-emerald-500/50">
                         {/* Gold Glow inside Banner */}
                        <div className="absolute top-0 right-0 w-32 h-32 bg-amber-400/20 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2"></div>

                        <div className="absolute -top-12 -right-12 p-8 opacity-10 group-hover:scale-110 transition-transform rotate-12 duration-1000">
                            <Wand2 size={180} />
                        </div>
                        <h3 className="text-xl font-bold mb-2 relative z-10 flex items-center gap-2">
                             <Sparkles size={20} className="text-amber-300" /> AI Strategy Optimizer
                        </h3>
                        <p className="text-emerald-50 text-sm mb-6 max-w-sm relative z-10 leading-relaxed font-medium opacity-90">
                            단편적인 아이디어를 전문가 수준의 구조화된 프롬프트(R.C.A.T.E.)로 자동 변환합니다.
                        </p>
                        <button 
                            onClick={handleMagicOptimize}
                            disabled={loading}
                            className="relative z-10 bg-white/10 backdrop-blur-md border border-white/20 text-white px-6 py-3 rounded-2xl text-xs font-bold hover:bg-white hover:text-emerald-700 transition-colors flex items-center gap-2 shadow-lg"
                        >
                            {loading ? <RefreshCw size={14} className="animate-spin"/> : <Wand2 size={14}/>} 
                            Run Magic Optimization
                        </button>
                    </div>

                    {/* Inputs */}
                    <section>
                        <SectionHeader title="1. Definition (정의)" icon={<Briefcase size={16} className="text-emerald-600"/>} description="누가, 누구를 위해 일하는지 명확히 정의합니다." />
                        <div className="grid grid-cols-1 gap-6">
                            {renderInput('role', 'R - Role (전문가 페르소나)', 2)}
                            {renderInput('audience', 'A - Audience (청중/독자)', 2)}
                        </div>
                    </section>
                    <div className="w-full h-px bg-slate-100 my-4"></div>
                    <section>
                        <SectionHeader title="2. Content (내용)" icon={<FileText size={16} className="text-teal-600"/>} description="분석할 데이터의 맥락과 구체적인 작업을 지시합니다." />
                        <div className="space-y-6">
                            {renderInput('context', 'C - Context (배경 및 제약사항)', 4)}
                            {renderInput('task', 'T - Task (수행 임무)', 3)}
                        </div>
                    </section>
                    <div className="w-full h-px bg-slate-100 my-4"></div>
                    <section>
                        <SectionHeader title="3. Output (결과물)" icon={<CheckCircle2 size={16} className="text-cyan-600"/>} description="최종 결과물의 형식과 검증 기준을 설정합니다." />
                        {renderInput('execution', 'E - Execution (실행 및 형식)', 2)}
                    </section>
                </div>
                
                {/* Mobile FAB */}
                <div className="md:hidden h-24"></div>
                <button 
                    onClick={runSimulation}
                    className="md:hidden fixed bottom-6 right-6 bg-emerald-600 text-white p-4 rounded-full shadow-2xl z-30 hover:scale-105 transition-transform ring-4 ring-emerald-600/20"
                >
                    <PlayCircle size={28} />
                </button>
            </div>

            {/* RIGHT: SIMULATION (RUN) */}
            <div className={`flex-1 bg-slate-50 flex flex-col overflow-hidden relative ${activeTab === 'DESIGN' ? 'hidden md:flex' : 'flex'}`}>
                
                {/* Simulation Toolbar */}
                <div className="bg-white/80 backdrop-blur-sm border-b border-slate-200 p-4 flex justify-between items-center shadow-sm sticky top-0 z-10">
                    <div className="flex items-center gap-3 px-2">
                        <div className={`w-2.5 h-2.5 rounded-full shadow-sm ${simulationState === 'IDLE' ? 'bg-slate-300' : simulationState === 'ERROR' ? 'bg-red-500' : simulationState === 'DONE' ? 'bg-emerald-500' : 'bg-emerald-500 animate-pulse'}`}></div>
                        <span className="text-xs font-bold text-slate-700 uppercase tracking-wide">
                            {simulationState === 'IDLE' ? 'Ready' : simulationState === 'ERROR' ? 'Failed' : simulationState === 'DRAFTING' ? 'Drafting Strategy...' : simulationState === 'REVIEWING' ? 'Reviewing...' : 'Complete'}
                        </span>
                    </div>
                    {simulationState !== 'DRAFTING' && simulationState !== 'REVIEWING' && (
                        <button 
                            onClick={runSimulation}
                            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 shadow-lg shadow-emerald-500/20 transition-all active:scale-95 hover:-translate-y-0.5"
                        >
                            {simulationState === 'IDLE' ? <PlayCircle size={14}/> : <RotateCcw size={14}/>} 
                            {simulationState === 'IDLE' ? 'Run Simulation' : 'Rerun'}
                        </button>
                    )}
                </div>

                {/* Simulation Output Area */}
                <div className="flex-1 overflow-y-auto p-4 sm:p-8 relative">
                    {simulationState === 'IDLE' && !draftContent ? (
                        <div className="h-full flex flex-col items-center justify-center text-slate-400 opacity-60">
                            <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center mb-6 shadow-sm border border-slate-100">
                                <Zap size={40} className="stroke-1 text-slate-300"/>
                            </div>
                            <p className="text-sm font-medium">Click 'Run Simulation' to execute strategy.</p>
                        </div>
                    ) : (
                        <div className="max-w-4xl mx-auto space-y-10 pb-20">
                            
                            {/* 1. DRAFT CARD */}
                            <div className="bg-white rounded-[2rem] shadow-sm border border-slate-200 overflow-hidden animate-slide-up ring-1 ring-slate-100/50">
                                <div className="bg-slate-50/50 border-b border-slate-100 px-8 py-5 flex justify-between items-center">
                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center font-bold text-sm shadow-sm border border-blue-100">A1</div>
                                        <div>
                                            <h4 className="text-sm font-bold text-slate-800">Draft Strategy</h4>
                                            <p className="text-[10px] text-slate-500 font-medium">Model: Gemini 2.5 Flash</p>
                                        </div>
                                    </div>
                                    {simulationState === 'DRAFTING' && <RefreshCw size={16} className="text-blue-500 animate-spin"/>}
                                </div>
                                <div className="p-10 max-h-[600px] overflow-y-auto bg-white custom-scrollbar">
                                    <div className="prose prose-sm prose-slate max-w-none prose-headings:font-bold prose-h1:text-2xl prose-h2:text-lg prose-p:leading-relaxed">
                                        <div className="whitespace-pre-wrap font-serif text-slate-800 leading-relaxed selection:bg-emerald-100">
                                            {draftContent || "Waiting for output..."}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* 2. ARROW CONNECTOR */}
                            {simulationState !== 'DRAFTING' && (
                                <div className="flex justify-center animate-fade-in">
                                    <div className="bg-white p-3 rounded-full shadow-sm border border-slate-200 text-slate-400">
                                        <ChevronRight size={24} className="rotate-90 sm:rotate-0"/>
                                    </div>
                                </div>
                            )}

                            {/* 3. REVIEW CARD */}
                            {reviewResult && (
                                <div className="bg-white rounded-[2rem] shadow-xl border border-emerald-100/50 overflow-hidden animate-slide-up ring-1 ring-emerald-50">
                                     <div className="bg-gradient-to-r from-emerald-50 to-teal-50 border-b border-emerald-100 px-8 py-5 flex justify-between items-center">
                                        <div className="flex items-center gap-4">
                                            <div className="w-10 h-10 bg-emerald-100 text-emerald-600 rounded-xl flex items-center justify-center font-bold text-sm shadow-sm border border-emerald-200">A2</div>
                                            <div>
                                                <h4 className="text-sm font-bold text-slate-800">Senior Partner Review</h4>
                                                <p className="text-[10px] text-slate-500 font-medium">Model: Gemini 3 Pro (Reasoning)</p>
                                            </div>
                                        </div>
                                        {reviewResult.score > 85 && (
                                            <div className="bg-amber-100 px-4 py-1.5 rounded-full text-[11px] font-bold text-amber-700 border border-amber-200 shadow-sm uppercase tracking-wide flex items-center gap-1">
                                                <Crown size={12} fill="currentColor"/> High Quality
                                            </div>
                                        )}
                                    </div>
                                    
                                    <div className="p-10 flex flex-col lg:flex-row gap-12">
                                        <div className="flex flex-col items-center justify-center lg:w-1/4 border-b lg:border-b-0 lg:border-r border-slate-100 pb-10 lg:pb-0 lg:pr-10">
                                            <ScoreGauge score={reviewResult.score} />
                                            <span className={`mt-4 px-4 py-1.5 rounded-full text-xs font-bold border ${
                                                reviewResult.score > 80 
                                                ? 'bg-emerald-50 text-emerald-700 border-emerald-100' 
                                                : 'bg-amber-50 text-amber-700 border-amber-100'
                                            }`}>
                                                {reviewResult.score > 80 ? 'Approved' : 'Needs Review'}
                                            </span>
                                        </div>
                                        <div className="flex-1 space-y-6">
                                            <div>
                                                <h5 className="text-xs font-bold text-slate-400 uppercase mb-3 tracking-wide flex items-center gap-2">
                                                    <Briefcase size={12}/> Executive Summary
                                                </h5>
                                                <p className="text-sm text-slate-700 leading-relaxed font-medium bg-slate-50 p-4 rounded-xl border border-slate-100">{reviewResult.summary}</p>
                                            </div>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                                <div className="bg-emerald-50/50 p-5 rounded-2xl border border-emerald-100/60">
                                                    <h6 className="text-xs font-bold text-emerald-700 mb-3 flex items-center gap-1.5"><CheckCircle2 size={14}/> Strengths</h6>
                                                    <ul className="text-xs text-emerald-800 space-y-2 list-disc pl-4 leading-relaxed font-medium">
                                                        {reviewResult.strengths.map((s, i) => <li key={i}>{s}</li>)}
                                                    </ul>
                                                </div>
                                                <div className="bg-rose-50/50 p-5 rounded-2xl border border-rose-100/60">
                                                    <h6 className="text-xs font-bold text-rose-700 mb-3 flex items-center gap-1.5"><AlertTriangle size={14}/> Risks & Weaknesses</h6>
                                                    <ul className="text-xs text-rose-800 space-y-2 list-disc pl-4 leading-relaxed font-medium">
                                                        {reviewResult.weaknesses.map((w, i) => <li key={i}>{w}</li>)}
                                                    </ul>
                                                </div>
                                            </div>
                                            <div className="bg-blue-50/50 p-5 rounded-2xl border border-blue-100 flex gap-4 items-start">
                                                <div className="p-2.5 bg-blue-100 rounded-xl text-blue-600 shrink-0">
                                                    <TrendingUp size={20} />
                                                </div>
                                                <div>
                                                    <h6 className="text-xs font-bold text-blue-700 mb-1.5">Strategic Refinement</h6>
                                                    <p className="text-xs text-blue-800 leading-relaxed font-medium">{reviewResult.refined_suggestion}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    </div>
  );
};