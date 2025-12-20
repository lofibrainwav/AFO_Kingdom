import React, { useState, useEffect, useRef } from 'react';
import { generateInterviewQuestion, generateRcateFromInterview } from '../services/geminiService';
import { RcateData } from '../types';
import { Bot, ArrowRight, CheckCircle2, Loader2, Sparkles, RefreshCw, ChevronLeft, Crown } from 'lucide-react';

interface SimulationWizardProps {
  onComplete: (data: RcateData) => void;
  onCancel: () => void;
}

const STEPS = [
  { id: 'ROLE', label: '역할 (Role)', description: '프로젝트에 필요한 전문가 페르소나 정의' },
  { id: 'CONTEXT', label: '상황 (Context)', description: '클라이언트 상황, 데이터, 법적 제약' },
  { id: 'AUDIENCE', label: '청중 (Audience)', description: '보고서를 받아볼 대상' },
  { id: 'TASK', label: '임무 (Task)', description: '수행해야 할 구체적인 작업' },
  { id: 'EXECUTION', label: '실행 (Execution)', description: '결과물 형식 및 검증 방법' },
];

export const SimulationWizard: React.FC<SimulationWizardProps> = ({ onComplete, onCancel }) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [inputs, setInputs] = useState<{ step: string; answer: string }[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [aiQuestion, setAiQuestion] = useState('시뮬레이션을 시작합니다. 이번 프로젝트의 주요 주제나 당신이 맡고 싶은 전문 분야는 무엇인가요? (예: 국제 조세, 내부 감사 등)');
  const [isLoading, setIsLoading] = useState(false);
  const [isCompiling, setIsCompiling] = useState(false);
  
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-focus input on step change
  useEffect(() => {
    if (!isCompiling) {
      inputRef.current?.focus();
    }
  }, [currentStepIndex, isCompiling]);

  const handleNext = async () => {
    if (!currentAnswer.trim()) return;

    const newInputs = [...inputs, { step: STEPS[currentStepIndex].id, answer: currentAnswer }];
    setInputs(newInputs);
    setCurrentAnswer('');

    if (currentStepIndex < STEPS.length - 1) {
      // Go to next step and fetch question
      setIsLoading(true);
      const nextStepIndex = currentStepIndex + 1;
      setCurrentStepIndex(nextStepIndex);
      
      try {
        const question = await generateInterviewQuestion(STEPS[nextStepIndex].label, newInputs);
        setAiQuestion(question);
      } catch (e) {
        setAiQuestion("다음 단계에 대한 구체적인 내용을 입력해주세요.");
      } finally {
        setIsLoading(false);
      }
    } else {
      // Finish
      handleFinish(newInputs);
    }
  };

  const handleFinish = async (finalInputs: { step: string; answer: string }[]) => {
    setIsCompiling(true);
    try {
      const rcateData = await generateRcateFromInterview(finalInputs);
      if (rcateData) {
        onComplete(rcateData);
      } else {
        alert("전략 생성에 실패했습니다. 다시 시도해주세요.");
        setIsCompiling(false);
      }
    } catch (e) {
      console.error(e);
      alert("오류가 발생했습니다.");
      setIsCompiling(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleNext();
    }
  };

  const progressPercentage = ((currentStepIndex + 1) / STEPS.length) * 100;

  if (isCompiling) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[80vh] animate-fade-in text-center p-8">
        <div className="w-24 h-24 bg-emerald-50 rounded-full flex items-center justify-center mb-8 relative">
          <div className="absolute inset-0 rounded-full border-4 border-emerald-100"></div>
          <div className="absolute inset-0 rounded-full border-4 border-t-emerald-600 border-r-transparent border-b-transparent border-l-transparent animate-spin"></div>
          <Sparkles size={40} className="text-emerald-600 animate-pulse" />
        </div>
        <h2 className="text-3xl font-bold text-slate-900 mb-4">전략 구축 중...</h2>
        <p className="text-slate-500 max-w-md leading-relaxed">
          AICPA Core가 인터뷰 내용을 바탕으로 <br/>
          최적화된 R.C.A.T.E. 프레임워크를 설계하고 있습니다.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-white relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-50/50 rounded-full blur-3xl -z-10 translate-x-1/2 -translate-y-1/2"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-teal-50/50 rounded-full blur-3xl -z-10 -translate-x-1/2 translate-y-1/2"></div>

      {/* Header / Nav */}
      <div className="px-8 py-6 flex justify-between items-center max-w-5xl mx-auto w-full">
        <button onClick={onCancel} className="text-slate-400 hover:text-slate-600 flex items-center gap-1 text-sm font-medium transition-colors">
          <ChevronLeft size={16} /> 나가기
        </button>
        <div className="flex flex-col items-end">
          <span className="text-xs font-bold text-emerald-600 uppercase tracking-widest mb-1.5">Step {currentStepIndex + 1} of {STEPS.length}</span>
          <div className="w-32 h-1.5 bg-slate-100 rounded-full overflow-hidden">
             {/* Gradient with Gold Tip */}
             <div 
                className="h-full bg-gradient-to-r from-emerald-500 via-emerald-400 to-amber-400 transition-all duration-500 ease-out"
                style={{ width: `${progressPercentage}%` }}
             ></div>
          </div>
        </div>
      </div>

      {/* Main Interaction Area */}
      <div className="flex-1 flex flex-col justify-center items-center max-w-3xl mx-auto w-full px-6 animate-slide-down">
        
        {/* Step Indicator */}
        <div className="mb-6 flex items-center gap-2">
            <span className="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs font-bold uppercase tracking-wide">
                {STEPS[currentStepIndex].id}
            </span>
            <span className="text-slate-400 text-sm font-medium">
                {STEPS[currentStepIndex].description}
            </span>
        </div>

        {/* AI Question Bubble */}
        <div className="bg-white border border-slate-200 shadow-xl shadow-emerald-900/5 rounded-[2rem] p-10 mb-8 w-full relative group transition-all hover:shadow-2xl hover:shadow-emerald-900/10 hover:-translate-y-1">
            <div className="absolute -top-6 left-8 bg-slate-900 text-amber-400 p-3 rounded-2xl shadow-lg flex items-center gap-2 border border-slate-800">
                <Bot size={20} />
                <span className="text-xs font-bold text-white">AI Interviewer</span>
            </div>
            
            <div className="mt-2">
                {isLoading ? (
                    <div className="flex items-center gap-2 text-slate-400 h-8">
                        <Loader2 size={20} className="animate-spin text-emerald-500" />
                        <span className="text-sm">다음 질문 생성 중...</span>
                    </div>
                ) : (
                    <h1 className="text-xl sm:text-2xl font-bold text-slate-800 leading-relaxed">
                        {aiQuestion}
                    </h1>
                )}
            </div>
        </div>

        {/* User Input */}
        <div className="w-full relative">
            <textarea
                ref={inputRef}
                value={currentAnswer}
                onChange={(e) => setCurrentAnswer(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="답변을 입력하세요... (Enter를 눌러 계속)"
                className="w-full bg-slate-50 border-2 border-slate-200 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 rounded-[1.5rem] p-6 text-lg text-slate-900 placeholder:text-slate-400 resize-none shadow-inner transition-all min-h-[120px]"
                autoFocus
                disabled={isLoading}
            />
            <div className="absolute bottom-4 right-4 flex items-center gap-2">
                 <span className="text-xs text-slate-400 hidden sm:inline">Press <strong>Enter</strong> to continue</span>
                 <button
                    onClick={handleNext}
                    disabled={!currentAnswer.trim() || isLoading}
                    className={`p-3 rounded-xl transition-all ${
                        currentAnswer.trim() && !isLoading
                        ? 'bg-emerald-600 text-white shadow-lg hover:bg-emerald-500 hover:scale-105' 
                        : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                    }`}
                >
                    {isLoading ? <Loader2 size={24} className="animate-spin" /> : <ArrowRight size={24} />}
                </button>
            </div>
        </div>
      </div>
    </div>
  );
};