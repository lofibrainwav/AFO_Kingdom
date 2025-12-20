import React, { useState, useEffect, useRef } from 'react';
import { X, Globe, Lock, RotateCw, ChevronLeft, ChevronRight, FileText, FileSpreadsheet, CheckCircle, Loader2, MoreVertical, Star, MousePointer2, Cpu, BarChart3, AlertTriangle, Check, Terminal, Save, ArrowRight } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { runBrowserAgent } from '../services/geminiService';
import { TrinityService } from '../services/trinityService';
import { KnowledgeDoc } from '../types';

export const AgentBrowser: React.FC = () => {
  const { browserState, setBrowserState, setKnowledgeFolders, showNotification } = useApp();
  const [currentContent, setCurrentContent] = useState<string>('');
  const [currentUrl, setCurrentUrl] = useState<string>('about:blank');
  const [isTyping, setIsTyping] = useState(false);
  const [cursorPos, setCursorPos] = useState({ x: 50, y: 50 });
  
  const contentEndRef = useRef<HTMLDivElement>(null);
  const processingRef = useRef(false);
  const isMountedRef = useRef(true); // Safety for async operations

  const isComplete = browserState.activeStepIndex >= browserState.steps.length;

  // Track mount status
  useEffect(() => {
    isMountedRef.current = true;
    return () => { isMountedRef.current = false; };
  }, []);

  const moveCursor = async (x: number, y: number, waitMs: number = 500) => {
      if (!isMountedRef.current) return;
      setCursorPos({ x, y });
      await new Promise(r => setTimeout(r, waitMs));
  };

  const scrollToBottom = () => {
      if(contentEndRef.current) {
          contentEndRef.current.scrollTop = contentEndRef.current.scrollHeight;
      }
  };

  useEffect(() => {
    if (!browserState.isOpen || isComplete) return;

    const currentStep = browserState.steps[browserState.activeStepIndex];
    if (currentStep.status !== 'pending') return;
    if (processingRef.current) return;

    const executeWorkflow = async () => {
      processingRef.current = true;
      const stepIndex = browserState.activeStepIndex;
      const step = browserState.steps[stepIndex];
      
      // Update Status: Running
      setBrowserState(prev => {
          const newSteps = [...prev.steps];
          newSteps[stepIndex].status = 'running';
          return { ...prev, steps: newSteps };
      });
      
      if (step.url) setCurrentUrl(step.url);

      try {
          if (step.action === 'NAVIGATE') {
              await moveCursor(320, 45, 600);
              await moveCursor(400, 400, 800);
          } 
          
          else if (step.action === 'READ_EXCEL') {
              TrinityService.updateJulieStatus('WORKING', 'Bangtong parsing Excel data...');
              setIsTyping(true);
              setCurrentContent('');
              await moveCursor(600, 250, 400);

              const generator = runBrowserAgent(step.action, browserState.targetDocId || 'Doc', '');
              let fullContent = "";
              for await (const chunk of generator) {
                  if (!isMountedRef.current) break;
                  fullContent += chunk;
                  setCurrentContent(fullContent);
                  scrollToBottom();
              }
              
              if (isMountedRef.current) {
                  setBrowserState(prev => ({ 
                      ...prev, 
                      memory: { ...prev.memory, 'excelData': fullContent },
                      steps: prev.steps.map((s, i) => i === stepIndex ? { ...s, contentPreview: fullContent } : s)
                  }));
                  setIsTyping(false);
                  await new Promise(r => setTimeout(r, 600));
              }
          }
          
          else if (step.action === 'ANALYZE') {
               TrinityService.updateJulieStatus('AUDITING', 'Yukson performing financial analysis...');
               await moveCursor(500, 300, 400);
               setCurrentContent(''); 
               
               // Safe fallback if previous step failed
               const excelData = browserState.memory['excelData'] || "No Data Found";
               const generator = runBrowserAgent('ANALYZE', '', excelData);
               
               let analysis = "";
               for await (const chunk of generator) {
                   if (!isMountedRef.current) break;
                   analysis += chunk;
                   setCurrentContent(analysis);
                   scrollToBottom();
                   await new Promise(r => setTimeout(r, 10)); 
               }
               
               if (isMountedRef.current) {
                   setBrowserState(prev => ({ ...prev, memory: { ...prev.memory, 'analysis': analysis } }));
                   await new Promise(r => setTimeout(r, 1000));
               }
          }
          
          else if (step.action === 'WRITE_WORD') {
              TrinityService.updateJulieStatus('AUDITING', 'Zhaoyun drafting final memo...');
              setIsTyping(true);
              setCurrentContent('');
              await moveCursor(400, 180, 400); 
              
              const findings = browserState.memory['analysis'] || "Analysis Incomplete";
              const generator = runBrowserAgent('WRITE_WORD', browserState.targetDocId || 'Report', findings);
              
              let fullContent = "";
              for await (const chunk of generator) {
                  if (!isMountedRef.current) break;
                  fullContent += chunk;
                  setCurrentContent(fullContent);
                  scrollToBottom();
              }
              
              if (isMountedRef.current) {
                  setBrowserState(prev => ({ 
                      ...prev, 
                      steps: prev.steps.map((s, i) => i === stepIndex ? { ...s, contentPreview: fullContent } : s)
                  }));
                  setIsTyping(false);
                  await new Promise(r => setTimeout(r, 800));
              }
          }
          
          else if (step.action === 'SAVE') {
               TrinityService.updateJulieStatus('IDLE', 'Report saved. Task Complete.');
               await moveCursor(45, 135, 600);
               await moveCursor(150, 200, 400);
               
               const reportContent = browserState.steps.find(s => s.action === 'WRITE_WORD')?.contentPreview || "Empty Report";
               const docId = `report-${Date.now()}`;
               const newDoc: KnowledgeDoc = {
                   id: docId,
                   name: 'AI_Audit_Memo_Final.docx',
                   type: 'WORD',
                   size: '18 KB',
                   uploadDate: new Date(),
                   mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                   content: window.btoa(reportContent), 
                   summary: 'Auto-generated by Gemini Agent'
               };
               
               if (isMountedRef.current) {
                   setKnowledgeFolders(prev => {
                       if(prev.length === 0) return prev;
                       const newFolders = [...prev];
                       let targetFolderIdx = newFolders.findIndex(f => f.docs.some(d => d.id === browserState.targetDocId));
                       if (targetFolderIdx === -1) targetFolderIdx = 0;
                       newFolders[targetFolderIdx].docs.push(newDoc);
                       return newFolders;
                   });
                   showNotification("Audit Memo saved to Notebook", "success");
                   await new Promise(r => setTimeout(r, 1000));
               }
          }

          // Complete Step
          if (isMountedRef.current) {
              setBrowserState(prev => {
                  const newSteps = [...prev.steps];
                  newSteps[stepIndex].status = 'done';
                  return { ...prev, steps: newSteps, activeStepIndex: stepIndex + 1 };
              });
          }

      } catch (e) {
          console.error("Workflow Error", e);
      } finally {
          processingRef.current = false;
      }
    };

    executeWorkflow();
  }, [browserState.isOpen, browserState.activeStepIndex, isComplete, browserState.steps]);

  if (!browserState.isOpen) return null;

  const currentStep = browserState.steps[Math.min(browserState.activeStepIndex, browserState.steps.length - 1)];
  const isExcel = currentStep.url?.includes('excel');
  const isWord = currentStep.url?.includes('word');
  const isAnalyze = currentStep.action === 'ANALYZE';
  const isSaving = currentStep.action === 'SAVE';

  return (
    <div className="fixed inset-0 z-[100] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6 animate-fade-in font-sans">
      <div className="w-full max-w-6xl h-[90vh] sm:h-[85vh] bg-white rounded-xl shadow-2xl flex flex-col overflow-hidden border border-slate-600 relative ring-1 ring-white/10">
        
        {/* CHROME TOP BAR */}
        <div className="bg-[#dee1e6] flex flex-col pt-2 rounded-t-xl select-none">
            <div className="flex px-2 items-end space-x-2">
                <div className="w-56 bg-white rounded-t-lg px-3 py-2 text-xs flex items-center justify-between shadow-[0_0_5px_rgba(0,0,0,0.1)] relative z-10">
                    <div className="flex items-center gap-2 text-slate-700 truncate">
                        {isExcel ? <FileSpreadsheet size={14} className="text-green-600"/> : isWord ? <FileText size={14} className="text-blue-600"/> : isAnalyze ? <Cpu size={14} className="text-purple-600"/> : <Globe size={14} className="text-slate-500"/>}
                        <span className="truncate font-medium">
                            {isComplete ? 'Workflow Complete' : currentStep.description || 'New Tab'}
                        </span>
                    </div>
                    <X size={12} className="text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-200 p-0.5 cursor-pointer" onClick={() => setBrowserState(p => ({...p, isOpen: false}))}/>
                </div>
                <div className="w-8 h-8 flex items-center justify-center hover:bg-slate-300 rounded-full cursor-pointer transition-colors">
                    <PlusIcon size={16} className="text-slate-600" />
                </div>
            </div>

            <div className="bg-white py-2 px-3 flex items-center gap-3 border-b border-slate-200 shadow-sm z-20">
                <div className="flex gap-2 text-slate-500">
                    <ChevronLeft size={18} className="opacity-50" />
                    <ChevronRight size={18} className="opacity-50" />
                    <RotateCw size={16} className={`cursor-pointer hover:text-slate-700 ${isTyping || currentStep.status === 'running' ? 'animate-spin text-blue-500' : ''}`} />
                </div>
                
                <div className="flex-1 bg-[#f1f3f4] rounded-full px-4 py-1.5 text-xs text-slate-700 flex items-center gap-2 group focus-within:bg-white focus-within:shadow-md transition-all border border-transparent focus-within:border-blue-300">
                    <Lock size={10} className="text-green-600" />
                    <span className="flex-1 truncate select-all">{isComplete ? 'aicpa://workflow/success' : currentUrl}</span>
                    <Star size={12} className="text-slate-400 group-hover:text-amber-400 cursor-pointer" />
                </div>

                <div className="flex gap-3 text-slate-500 items-center">
                    <div className="w-7 h-7 rounded-full bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center text-purple-700 text-[10px] font-bold border border-purple-200 shadow-sm">AI</div>
                    <MoreVertical size={16} className="cursor-pointer hover:bg-slate-100 rounded-full" />
                </div>
            </div>
        </div>

        {/* BROWSER CONTENT AREA */}
        <div className="flex-1 bg-white relative overflow-hidden flex flex-col">
            <div className="flex flex-1 overflow-hidden relative">
                {/* Sidebar */}
                <div className="w-72 bg-[#f8f9fa] border-r border-[#e9ecef] flex flex-col hidden md:flex">
                     <div className="h-9 bg-[#f1f3f4] flex items-center px-3 text-[10px] font-bold text-slate-600 border-b border-[#dee2e6] gap-4">
                         <span className="border-b-2 border-blue-500 h-full flex items-center px-1 text-blue-600 cursor-pointer">Console</span>
                         <span className="text-slate-400 h-full flex items-center px-1 cursor-pointer hover:text-slate-600">Network</span>
                         <span className="text-slate-400 h-full flex items-center px-1 cursor-pointer hover:text-slate-600">Elements</span>
                     </div>
                     <div className="flex-1 overflow-y-auto p-2 space-y-2 font-mono text-[11px] bg-white">
                        {browserState.steps.map((step, idx) => (
                            <div key={idx} className={`p-2 rounded border-l-2 transition-all ${idx <= browserState.activeStepIndex ? (step.status === 'done' ? 'border-green-500 bg-green-50/50' : 'border-blue-500 bg-blue-50/50') : 'border-slate-200 text-slate-400'}`}>
                                <div className="flex items-center gap-2 mb-1">
                                    {step.status === 'running' && <Loader2 size={10} className="animate-spin text-blue-600"/>}
                                    {step.status === 'done' && <CheckCircle size={10} className="text-green-600"/>}
                                    {step.status === 'pending' && <div className="w-2.5 h-2.5 rounded-full border border-slate-300"></div>}
                                    <span className="font-bold">{step.action}</span>
                                </div>
                                <span className="text-[10px] opacity-80">{step.description}</span>
                            </div>
                        ))}
                     </div>
                </div>

                {/* Main Viewport */}
                <div className="flex-1 bg-white relative overflow-auto flex flex-col">
                    
                    {isComplete ? (
                        /* SUCCESS SCREEN */
                        <div className="flex-1 flex flex-col items-center justify-center bg-slate-50 animate-fade-in">
                            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-6 animate-slide-up shadow-sm">
                                <CheckCircle size={40} className="text-green-600" />
                            </div>
                            <h2 className="text-2xl font-bold text-slate-900 mb-2">Automation Completed</h2>
                            <p className="text-slate-500 mb-8 max-w-sm text-center">
                                The Audit Memo has been drafted, reviewed, and saved to your Knowledge Base.
                            </p>
                            <div className="flex gap-4">
                                <button 
                                    onClick={() => setBrowserState(p => ({...p, isOpen: false}))}
                                    className="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors shadow-sm"
                                >
                                    Close
                                </button>
                                <button 
                                    onClick={() => {
                                        setBrowserState(p => ({...p, isOpen: false}));
                                        showNotification("Document opened in Viewer", "info");
                                    }}
                                    className="px-6 py-2.5 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors shadow-md flex items-center gap-2"
                                >
                                    <FileText size={18} /> View Document
                                </button>
                            </div>
                        </div>

                    ) : isExcel ? (
                        /* EXCEL VIEW */
                        <div className="flex-1 flex flex-col bg-white animate-fade-in">
                             <div className="h-24 bg-[#f3f2f1] border-b border-[#e1dfdd] flex flex-col">
                                 <div className="h-9 bg-[#217346] flex items-center px-4 justify-between shadow-sm">
                                     <div className="flex items-center gap-4">
                                         <div className="grid grid-cols-3 gap-1 opacity-80">
                                             {[...Array(6)].map((_,i)=><div key={i} className="w-1 h-1 bg-white rounded-full"></div>)}
                                         </div>
                                         <span className="text-white text-xs font-bold tracking-wide">Excel Online</span>
                                         <span className="text-white/80 text-xs px-2 py-0.5 bg-black/10 rounded">{browserState.targetDocId}</span>
                                     </div>
                                     <div className="w-6 h-6 rounded-full bg-white/20 text-white flex items-center justify-center text-[10px] font-bold">A</div>
                                 </div>
                                 <div className="flex-1 flex items-center px-4 gap-5 text-xs text-slate-600">
                                     <span className="hover:bg-slate-200 px-2 py-1 rounded cursor-pointer">File</span> 
                                     <span className="font-bold border-b-2 border-[#217346] pb-2 cursor-pointer">Home</span> 
                                     <span className="hover:bg-slate-200 px-2 py-1 rounded cursor-pointer">Insert</span>
                                     <span className="hover:bg-slate-200 px-2 py-1 rounded cursor-pointer">Data</span> 
                                 </div>
                                 <div className="h-8 bg-[#f3f2f1] border-t border-[#e1dfdd] flex items-center px-2 gap-2 text-slate-500 font-mono">
                                     <div className="bg-white border border-slate-300 px-2 py-0.5 w-24 text-[10px] shadow-inner">A1</div>
                                     <div className="bg-white border border-slate-300 px-2 py-0.5 flex-1 text-[10px] flex items-center gap-2 shadow-inner"><span className="text-slate-400 font-serif italic">fx</span> {isTyping ? "Sum(Revenue)..." : ""}</div>
                                 </div>
                             </div>
                             <div className="flex-1 overflow-auto bg-white p-6" ref={contentEndRef}>
                                 <div className="prose prose-sm max-w-none" dangerouslySetInnerHTML={{ __html: currentContent || '' }} />
                                 {!currentContent && <div className="text-slate-300 text-sm italic p-4 flex items-center gap-2"><Loader2 size={14} className="animate-spin"/> Waiting for data stream...</div>}
                             </div>
                             <div className="h-8 bg-[#f3f2f1] border-t border-[#e1dfdd] flex items-center px-2 gap-1">
                                 <div className="bg-white text-[#217346] px-4 py-1 text-xs font-bold border-b-2 border-[#217346] shadow-sm">Sheet1</div>
                                 <div className="text-slate-500 px-2 text-lg cursor-pointer hover:bg-slate-200 rounded">+</div>
                             </div>
                        </div>

                    ) : isAnalyze ? (
                        /* ANALYZE VIEW */
                        <div className="flex-1 bg-slate-900 text-green-400 font-mono p-8 flex flex-col relative animate-fade-in overflow-hidden">
                            <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:20px_20px]"></div>
                            <div className="z-10 flex flex-col h-full max-w-3xl mx-auto w-full">
                                <div className="flex items-center gap-2 text-white mb-6 border-b border-slate-700 pb-4">
                                    <Terminal size={20} />
                                    <span className="font-bold tracking-wider">GEMINI REASONING ENGINE v2.5</span>
                                </div>
                                <div className="flex-1 overflow-y-auto space-y-2 text-sm leading-relaxed" ref={contentEndRef}>
                                    <div className="prose prose-invert prose-p:text-green-400 prose-li:text-green-400 prose-strong:text-white max-w-none" dangerouslySetInnerHTML={{ __html: currentContent || '' }} />
                                    <div className="w-3 h-5 bg-green-400 animate-pulse inline-block align-middle ml-1"></div>
                                </div>
                                <div className="mt-6 grid grid-cols-3 gap-4 border-t border-slate-700 pt-6">
                                    <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
                                        <div className="text-slate-400 text-xs uppercase mb-1">Risk Score</div>
                                        <div className="text-2xl font-bold text-red-400 flex items-center gap-2"><AlertTriangle size={20}/> High</div>
                                    </div>
                                    <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
                                        <div className="text-slate-400 text-xs uppercase mb-1">Anomalies</div>
                                        <div className="text-2xl font-bold text-yellow-400 flex items-center gap-2"><BarChart3 size={20}/> 3 Found</div>
                                    </div>
                                    <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
                                        <div className="text-slate-400 text-xs uppercase mb-1">Confidence</div>
                                        <div className="text-2xl font-bold text-blue-400 flex items-center gap-2"><Check size={20}/> 98.2%</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    ) : isWord ? (
                        /* WORD VIEW */
                        <div className="flex-1 bg-[#f3f2f1] p-8 overflow-y-auto flex justify-center animate-fade-in">
                            <div className="w-[816px] min-h-[1056px] bg-white shadow-xl p-[96px] relative animate-slide-up origin-top">
                                 <div className="prose prose-slate max-w-none" dangerouslySetInnerHTML={{ __html: currentContent || '' }} />
                                 {!currentContent && <div className="text-slate-300 text-sm italic flex items-center gap-2"><Loader2 size={14} className="animate-spin"/> Initializing document...</div>}
                            </div>
                        </div>

                    ) : isSaving ? (
                        <div className="flex-1 flex flex-col items-center justify-center bg-white animate-fade-in">
                            <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-6">
                                <Save size={32} className="text-blue-600 animate-pulse" />
                            </div>
                            <h2 className="text-xl font-bold text-slate-800">Saving to Knowledge Base...</h2>
                            <div className="w-64 h-2 bg-slate-100 rounded-full mt-4 overflow-hidden">
                                <div className="h-full bg-blue-600 animate-slide-right w-full origin-left"></div>
                            </div>
                            <style>{`
                                @keyframes slideRight { 0% { transform: translateX(-100%); } 100% { transform: translateX(0); } }
                                .animate-slide-right { animation: slideRight 1.5s ease-out; }
                            `}</style>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center h-full text-slate-300 bg-slate-50">
                            <Globe size={64} className="mb-4 opacity-20 animate-pulse" />
                            <p className="text-lg font-medium">Navigating secure environment...</p>
                        </div>
                    )}
                    
                    {/* Virtual Cursor */}
                    {!isComplete && (
                        <div 
                            className="absolute z-50 transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] pointer-events-none drop-shadow-xl"
                            style={{ left: cursorPos.x, top: cursorPos.y }}
                        >
                            <MousePointer2 size={24} className="text-black fill-black stroke-white stroke-2" />
                            <div className="ml-4 mt-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-[10px] px-3 py-1.5 rounded-full font-bold whitespace-nowrap opacity-90 shadow-lg flex items-center gap-1.5">
                                <Cpu size={10} className="animate-pulse" />
                                Gemini Agent
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
        
        {/* Close Button Overlay */}
        <button 
            onClick={() => setBrowserState(p => ({...p, isOpen: false}))} 
            className="absolute top-3 right-3 p-2 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg z-[60] transition-transform hover:scale-110 flex items-center justify-center group"
            title="Close Browser Session"
        >
            <X size={16} className="group-hover:rotate-90 transition-transform"/>
        </button>
      </div>
    </div>
  );
};

const PlusIcon = ({size, className}: {size:number, className?:string}) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
    </svg>
);