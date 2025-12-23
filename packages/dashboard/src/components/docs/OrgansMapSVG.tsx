"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Modal } from "./Modal";

interface OrganInfo {
  id: string;
  name: string;
  component: string;
  description: string;
  x: number;
  y: number;
  width?: number;
  height?: number;
  type: "circle" | "ellipse" | "path" | "rect";
  path?: string;
  rx?: number;
  ry?: number;
  r?: number;
}

const organs: OrganInfo[] = [
  {
    id: "head",
    name: "🧠 뇌 (Brain)",
    component: "PostgreSQL",
    description: "왕국의 모든 지혜와 API 키를 암호화하여 저장하는 장기 기억 장치",
    x: 150,
    y: 80,
    r: 50,
    type: "circle",
  },
  {
    id: "heart",
    name: "❤️ 심장 (Heart)",
    component: "Trinity-OS & Redis",
    description: "실시간 캐시와 대화 맥락을 보존하는 체크포인트를 관리하는 정신의 중심",
    x: 150,
    y: 225,
    type: "path",
    path: "M 150 200 Q 130 180 120 200 Q 120 220 150 250 Q 180 220 180 200 Q 180 180 150 200",
  },
  {
    id: "lung-left",
    name: "🫁 폐 (Lungs - Left)",
    component: "Observability & Qdrant",
    description: "시스템 메트릭 관찰과 벡터 검색을 통해 지능적 호흡을 담당",
    x: 120,
    y: 240,
    rx: 25,
    ry: 40,
    type: "ellipse",
  },
  {
    id: "lung-right",
    name: "🫁 폐 (Lungs - Right)",
    component: "Observability & Qdrant",
    description: "시스템 메트릭 관찰과 벡터 검색을 통해 지능적 호흡을 담당",
    x: 180,
    y: 240,
    rx: 25,
    ry: 40,
    type: "ellipse",
  },
  {
    id: "liver",
    name: "간 (Liver)",
    component: "System Cache",
    description: "시스템 캐시를 관리하는 간 기능",
    x: 130,
    y: 300,
    rx: 30,
    ry: 35,
    type: "ellipse",
  },
  {
    id: "stomach",
    name: "🍽️ 소화기관 (Digestive)",
    component: "Ollama",
    description: "로컬 LLM을 통해 외부 통신 없이도 스스로 사고하는 내부 지력을 제공",
    x: 150,
    y: 350,
    rx: 25,
    ry: 30,
    type: "ellipse",
  },
  {
    id: "gallbladder",
    name: "💪 담 (Gallbladder)",
    component: "Testing (Pytest)",
    description: "모든 기능을 엄격히 판정하고 결단을 내리는 검증 시스템",
    x: 150,
    y: 400,
    rx: 20,
    ry: 25,
    type: "ellipse",
  },
];

/**
 * 인터랙티브 오장육부 지도 SVG
 * 
 * 각 장기를 클릭하면 상세 정보를 모달로 표시합니다.
 */
export function OrgansMapSVG() {
  const [selectedOrgan, setSelectedOrgan] = useState<OrganInfo | null>(null);
  const [hoveredOrgan, setHoveredOrgan] = useState<string | null>(null);

  const handleOrganClick = (organ: OrganInfo) => {
    setSelectedOrgan(organ);
  };

  const renderOrgan = (organ: OrganInfo) => {
    const isHovered = hoveredOrgan === organ.id;
    const baseProps = {
      onClick: () => handleOrganClick(organ),
      onMouseEnter: () => setHoveredOrgan(organ.id),
      onMouseLeave: () => setHoveredOrgan(null),
      className: "cursor-pointer transition-all",
      style: {
        fill: isHovered ? "#667eea" : "var(--bg-secondary)",
        stroke: isHovered ? "#667eea" : "var(--border-color)",
        strokeWidth: isHovered ? 3 : 2,
        opacity: isHovered ? 0.8 : 1,
      },
    };

    switch (organ.type) {
      case "circle":
        return (
          <circle
            key={organ.id}
            id={organ.id}
            cx={organ.x}
            cy={organ.y}
            r={organ.r}
            {...baseProps}
          />
        );
      case "ellipse":
        return (
          <ellipse
            key={organ.id}
            id={organ.id}
            cx={organ.x}
            cy={organ.y}
            rx={organ.rx}
            ry={organ.ry}
            {...baseProps}
          />
        );
      case "path":
        return (
          <path key={organ.id} id={organ.id} d={organ.path} {...baseProps} />
        );
      default:
        return null;
    }
  };

  return (
    <>
      <svg
        viewBox="0 0 300 600"
        className="w-full h-auto max-w-md mx-auto"
        style={{ minHeight: "400px" }}
      >
        {/* 배경 */}
        <rect
          width="300"
          height="600"
          fill="var(--bg-card)"
          stroke="var(--border-color)"
          strokeWidth="2"
          rx="10"
        />

        {/* 장기들 */}
        {organs.map(renderOrgan)}

        {/* 장기 라벨 */}
        {organs.map((organ) => (
          <text
            key={`${organ.id}-label`}
            x={organ.x}
            y={organ.y + (organ.r || organ.ry || 0) + 15}
            textAnchor="middle"
            fontSize="10"
            fill="var(--text-primary)"
            className="pointer-events-none"
          >
            {organ.name.split(" ")[0]}
          </text>
        ))}
      </svg>

      {/* 장기 상세 모달 */}
      {selectedOrgan && (
        <Modal
          isOpen={!!selectedOrgan}
          onClose={() => setSelectedOrgan(null)}
          title={selectedOrgan.name}
          size="md"
        >
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-slate-500 mb-1">
                컴포넌트
              </h3>
              <p className="text-lg font-bold text-indigo-600">
                {selectedOrgan.component}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-slate-500 mb-1">
                설명
              </h3>
              <p className="text-slate-600 leading-relaxed">
                {selectedOrgan.description}
              </p>
            </div>
          </div>
        </Modal>
      )}
    </>
  );
}

