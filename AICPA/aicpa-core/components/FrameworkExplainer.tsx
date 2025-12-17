import React, { useState } from 'react';
import { ShieldCheck, MessageSquare, Target, UserCheck, ScrollText, ChevronDown, ChevronUp, CheckCircle, BrainCircuit } from 'lucide-react';

interface StepProps {
  id: string;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  description: string;
  exampleRole: string;
  exampleText: string;
  color: string;
  bgColor: string;
  borderColor: string;
  isOpen: boolean;
  onClick: () => void;
}

const FrameworkStep: React.FC<StepProps> = ({ 
  title, subtitle, icon, description, exampleRole, exampleText, color, bgColor, borderColor, isOpen, onClick 
}) => {
  return (
    <div 
      className={`border rounded-[1.5rem] transition-all duration-300 overflow-hidden ${isOpen ? `shadow-lg ring-1 ring-offset-2 ring-offset-slate-50 ${borderColor}` : 'border-slate-200 hover:border-slate-300 bg-white'}`}
    >
      <button 
        onClick={onClick}
        className="w-full flex items-center justify-between p-6 text-left focus:outline-none"
      >
        <div className="flex items-center gap-5">
          <div className={`flex-shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center transition-colors ${isOpen ? color + ' text-white shadow-md' : 'bg-slate-100 text-slate-500'}`}>
            {icon}
          </div>
          <div>
            <h3 className={`text-lg font-bold transition-colors ${isOpen ? 'text-slate-900' : 'text-slate-600'}`}>{title}</h3>
            <p className="text-sm text-slate-500 font-medium">{subtitle}</p>
          </div>
        </div>
        <div className={`transform transition-transform duration-300 ${isOpen ? 'rotate-180 text-emerald-600' : 'text-slate-400'}`}>
            <ChevronDown size={24} />
        </div>
      </button>

      <div 
        className={`transition-[max-height,opacity] duration-300 ease-in-out ${isOpen ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0'}`}
      >
        <div className="p-6 pt-0 border-t border-slate-100">
          <div className="flex flex-col md:flex-row gap-6 mt-4">
             {/* Concept */}
             <div className="flex-1">
                <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wide mb-2 flex items-center gap-2">
                    <BrainCircuit size={14} /> Core Concept
                </h4>
                <p className="text-slate-600 leading-relaxed text-sm">
                    {description}
                </p>
             </div>
             
             {/* Example */}
             <div className={`flex-1 rounded-2xl p-5 border ${bgColor} ${borderColor}`}>
                <h4 className="text-xs font-bold uppercase tracking-wide mb-2 flex items-center gap-2" style={{ color: borderColor.replace('border-', 'text-').replace('200', '700') }}>
                    <CheckCircle size={12} /> CPA Practical Example
                </h4>
                <div className="space-y-2">
                    <p className="text-xs font-semibold text-slate-900">{exampleRole}</p>
                    <p className="text-sm font-mono text-slate-700 bg-white/50 p-3 rounded-xl border border-black/5 leading-relaxed">
                        "{exampleText}"
                    </p>
                </div>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export const FrameworkExplainer: React.FC = () => {
  const [openStep, setOpenStep] = useState<string>('R');

  const steps = [
    {
      id: 'R',
      title: 'R - Role',
      subtitle: '전문가 페르소나 정의',
      icon: <UserCheck size={24} />,
      color: 'bg-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      description: 'AI에게 단순한 "도우미"가 아닌, 구체적인 전문 자격과 경력을 부여합니다. 이는 AI가 사용하는 어휘의 수준, 지식의 깊이, 그리고 문제 해결에 접근하는 태도를 결정짓는 가장 중요한 첫 단추입니다.',
      exampleRole: 'Forensic Accountant Scenario',
      exampleText: '당신은 20년 경력의 포렌식 회계사(Forensic Accountant)입니다. 재무제표의 미세한 이상 징후를 탐지하고, 부정 위험(Fraud Risk) 관점에서 데이터를 비판적으로 검토하십시오.'
    },
    {
      id: 'C',
      title: 'C - Context & Constraints',
      subtitle: '맥락 및 제약 설정',
      icon: <ShieldCheck size={24} />,
      color: 'bg-indigo-600',
      bgColor: 'bg-indigo-50',
      borderColor: 'border-indigo-200',
      description: 'AI의 환각(Hallucination)을 통제하는 핵심 단계입니다. 분석해야 할 구체적인 데이터(Input)를 제공하고, 반드시 준수해야 할 법적 규제나 회계 기준(K-IFRS, US GAAP 등)을 명확히 제약 조건으로 겁니다.',
      exampleRole: 'K-IFRS Compliance Check',
      exampleText: '분석 대상은 첨부된 2023년 시산표(Trial Balance)입니다. 모든 분석은 K-IFRS 제1115호 기준을 엄격히 준수해야 하며, 제공된 데이터 외의 외부 추측을 포함하지 마십시오.'
    },
    {
      id: 'A',
      title: 'A - Audience & Tone',
      subtitle: '청중 및 어조 설정',
      icon: <MessageSquare size={24} />,
      color: 'bg-emerald-600',
      bgColor: 'bg-emerald-50',
      borderColor: 'border-emerald-200',
      description: '결과물을 누가 읽느냐에 따라 AI의 출력 스타일을 조정합니다. 이사회를 위해서는 "전략적이고 직관적인" 톤을, 감사 팀을 위해서는 "실무적이고 상세한" 톤을 요구하여 추가 편집 시간을 줄입니다.',
      exampleRole: 'Board Meeting Briefing',
      exampleText: '대상 독자: 회계 지식이 부족한 이사회(Board of Directors). 어조: 전문용어 사용을 지양하고, 재무적 영향(Financial Impact) 중심으로 직관적이고 전략적인 어조를 유지하십시오.'
    },
    {
      id: 'T',
      title: 'T - Task & Target',
      subtitle: '임무 및 목표 정의',
      icon: <Target size={24} />,
      color: 'bg-amber-600',
      bgColor: 'bg-amber-50',
      borderColor: 'border-amber-200',
      description: 'AI가 수행해야 할 작업의 범위와 최종 목표를 명시합니다. "Think hard"와 같은 넛지(Nudge) 프롬프트를 사용하여 AI가 단순 나열이 아닌 심층적인 인과관계 분석을 수행하도록 유도합니다.',
      exampleRole: 'Risk Identification Task',
      exampleText: '주요 임무: 전년 대비 변동폭이 10% 이상인 계정과목을 식별하고, 잠재적인 리스크 요인을 3가지 시나리오로 요약하십시오. 이 문제에 대해 깊이 생각(Think hard)하십시오.'
    },
    {
      id: 'E',
      title: 'E - Execution',
      subtitle: '실행 및 감사 추적',
      icon: <ScrollText size={24} />,
      color: 'bg-rose-600',
      bgColor: 'bg-rose-50',
      borderColor: 'border-rose-200',
      description: 'AI를 블랙박스에서 꺼내는 단계입니다. CoT(Chain-of-Thought) 기법을 강제하여, 결론에 도달한 논리적 과정을 단계별로 출력하게 함으로써 인간 전문가가 결과를 검증(Verify)할 수 있게 합니다.',
      exampleRole: 'Audit Trail Requirement',
      exampleText: '결론을 제시하기 전에, 당신의 추론 과정을 단계별로(Step-by-step) 기술하십시오. 각 판단의 근거가 된 데이터 포인트와 회계 기준을 명시하여 교차 검증(Cross-check)할 수 있도록 하십시오.'
    }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <span className="text-emerald-600 font-bold tracking-wider uppercase text-xs bg-emerald-50 px-3 py-1 rounded-full mb-4 inline-block border border-emerald-100">
            Standard Operating Procedure
        </span>
        <h2 className="text-3xl font-extrabold text-slate-900 sm:text-4xl mb-4">
          R.C.A.T.E. Framework
        </h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          CPA의 전문성을 AI에 이식하는 5단계 프로토콜입니다.<br/>
          각 단계를 클릭하여 상세 가이드와 프롬프트 예시를 확인하십시오.
        </p>
      </div>

      <div className="space-y-4">
        {steps.map((step) => (
            <FrameworkStep 
                key={step.id}
                {...step}
                isOpen={openStep === step.id}
                onClick={() => setOpenStep(openStep === step.id ? '' : step.id)}
            />
        ))}
      </div>

      <div className="mt-16 bg-slate-900 rounded-[2rem] p-10 text-white shadow-xl relative overflow-hidden group">
        {/* Decorative Grid */}
        <div className="absolute inset-0 opacity-10 pointer-events-none">
            <svg className="h-full w-full" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <pattern id="framework-grid" width="20" height="20" patternUnits="userSpaceOnUse">
                        <circle cx="2" cy="2" r="1" fill="currentColor" />
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#framework-grid)" />
            </svg>
        </div>

        <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-8">
            <div>
                <h3 className="text-2xl font-bold mb-2">Ready to Apply?</h3>
                <p className="text-slate-400 leading-relaxed">
                    이론을 실전에 적용해 보십시오. <br/>
                    AICPA Core의 프롬프트 생성기가 R.C.A.T.E. 구조를 자동으로 설계해 드립니다.
                </p>
            </div>
            {/* Visual indicator handled by global navigation, no button needed here strictly but clearer call to action is nice */}
            <div className="flex items-center gap-3 text-sm font-mono text-emerald-300 bg-emerald-900/30 px-6 py-3 rounded-xl border border-emerald-800">
                <span>System Status:</span>
                <span className="flex items-center gap-2 text-emerald-400 font-bold">
                    <span className="h-2 w-2 bg-emerald-400 rounded-full animate-pulse shadow-[0_0_5px_#34d399]"></span>
                    Online
                </span>
            </div>
        </div>
      </div>
    </div>
  );
};