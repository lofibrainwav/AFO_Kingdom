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
    component: "Soul Engine (API Server)",
    description: "왕국의 모든 지능을 조율하고 지휘하는 중앙 관제 센터",
    x: 150,
    y: 80,
    r: 50,
    type: "circle",
  },
  {
    id: "heart",
    name: "❤️ 심장 (Heart)",
    component: "Redis (Cache)",
    description: "실시간 데이터 흐름과 대화 맥락을 보존하는 뜨거운 엔진",
    x: 150,
    y: 225,
    type: "path",
    path: "M 150 200 Q 130 180 120 200 Q 120 220 150 250 Q 180 220 180 200 Q 180 180 150 200",
  },
  {
    id: "lung-left",
    name: "🫁 폐 (Lungs - Left)",
    component: "Qdrant (Vector DB)",
    description: "지식의 공기를 빨아들여 고차원 벡터로 호흡하는 인지 기관",
    x: 120,
    y: 240,
    rx: 25,
    ry: 40,
    type: "ellipse",
  },
  {
    id: "lung-right",
    name: "🫁 폐 (Lungs - Right)",
    component: "Qdrant (Vector DB)",
    description: "지식의 공기를 빨아들여 고차원 벡터로 호흡하는 인지 기관",
    x: 180,
    y: 240,
    rx: 25,
    ry: 40,
    type: "ellipse",
  },
  {
    id: "liver",
    name: "🩹 간 (Liver)",
    component: "PostgreSQL (Memory)",
    description: "왕국의 모든 기록과 지혜를 축적하고 정화하는 장기 기억 저장소",
    x: 130,
    y: 300,
    rx: 30,
    ry: 35,
    type: "ellipse",
  },
  {
    id: "stomach",
    name: "脾 소화기관 (Spleen)",
    component: "Ollama (Local LLM)",
    description: "복잡한 생각을 소화하여 왕국 내부의 지력으로 변환하는 기관",
    x: 150,
    y: 350,
    rx: 25,
    ry: 30,
    type: "ellipse",
  },
  {
    id: "gallbladder",
    name: "💪 담 (Gallbladder)",
    component: "Evolution Gate",
    description: "진화의 위험을 판정하고 과감한 결단을 내리는 용기의 원천",
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

