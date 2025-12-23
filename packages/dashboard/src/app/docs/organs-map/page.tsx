"use client";

import { motion } from "framer-motion";
import { SectionCard, MermaidDiagram, OrgansMapSVG } from "@/components/docs";
import OrgansMonitor from "@/components/royal/OrgansMonitor";

const organsMermaid = `graph TB
    subgraph Organs["🫀 오장육부 시스템 (11-Organ System)"]
        Brain[🧠 뇌 Brain<br/>PostgreSQL<br/>장기 기억]
        Heart[❤️ 심장 Heart<br/>Trinity-OS & Redis<br/>실시간 캐시]
        Lungs[🫁 폐 Lungs<br/>Observability & Qdrant<br/>벡터 검색]
        Digestive[🍽️ 소화기관 Digestive<br/>Ollama<br/>로컬 LLM]
        Gallbladder[💪 담 Gallbladder<br/>Testing Pytest<br/>검증 시스템]
    end
    
    Brain --> Heart
    Heart --> Lungs
    Lungs --> Digestive
    Digestive --> Gallbladder
    Gallbladder --> Brain
    
    style Brain fill:#667eea,stroke:#333,stroke-width:3px,color:#fff
    style Heart fill:#f093fb,stroke:#333,stroke-width:3px,color:#fff
    style Lungs fill:#4facfe,stroke:#333,stroke-width:3px,color:#fff
    style Digestive fill:#43e97b,stroke:#333,stroke-width:3px,color:#fff
    style Gallbladder fill:#fa709a,stroke:#333,stroke-width:3px,color:#fff`;

const organs = [
  {
    name: "🧠 뇌 (Brain)",
    component: "PostgreSQL",
    description: "왕국의 모든 지혜와 API 키를 암호화하여 저장하는 장기 기억 장치",
  },
  {
    name: "❤️ 심장 (Heart)",
    component: "Trinity-OS & Redis",
    description: "실시간 캐시와 대화 맥락을 보존하는 체크포인트를 관리하는 정신의 중심",
  },
  {
    name: "🫁 폐 (Lungs)",
    component: "Observability & Qdrant",
    description: "시스템 메트릭 관찰과 벡터 검색을 통해 지능적 호흡을 담당",
  },
  {
    name: "🍽️ 소화기관 (Digestive)",
    component: "Ollama",
    description: "로컬 LLM을 통해 외부 통신 없이도 스스로 사고하는 내부 지력을 제공",
  },
  {
    name: "💪 담 (Gallbladder)",
    component: "Testing (Pytest)",
    description: "모든 기능을 엄격히 판정하고 결단을 내리는 검증 시스템",
  },
];

export default function OrgansMapPage() {
  return (
    <div className="min-h-screen bg-[#e0e5ec] p-6 md:p-10 lg:p-12">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400 mb-4">
            🫀 오장육부(11-Organ System) 기술 매핑
          </h1>
          <p className="text-slate-500 text-lg">
            시스템 컴포넌트를 인간의 장기에 비유한 생체 균형 관리
          </p>
        </motion.header>

        {/* 실시간 건강 모니터 */}
        <SectionCard title="실시간 건강 모니터" badge="실시간">
          <OrgansMonitor />
        </SectionCard>

        {/* 인터랙티브 오장육부 지도 */}
        <SectionCard title="인터랙티브 오장육부 지도" badge="클릭 가능">
          <OrgansMapSVG />
        </SectionCard>

        {/* 오장육부 시스템 다이어그램 */}
        <SectionCard title="오장육부 시스템 구조" badge="핵심">
          <MermaidDiagram code={organsMermaid} title="오장육부 시스템 플로우" />
        </SectionCard>

        {/* 장기별 상세 설명 */}
        <SectionCard title="장기별 상세 설명" badge="상세">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {organs.map((organ, index) => (
              <motion.div
                key={organ.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-6 bg-white/50 backdrop-blur-sm rounded-2xl border border-white/60 shadow-sm hover:shadow-md transition-all"
              >
                <h3 className="text-xl font-bold text-slate-700 mb-2">{organ.name}</h3>
                <div className="text-sm font-semibold text-indigo-600 mb-3">{organ.component}</div>
                <p className="text-slate-600 text-sm leading-relaxed">{organ.description}</p>
              </motion.div>
            ))}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

