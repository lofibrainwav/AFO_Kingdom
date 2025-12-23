"use client";

import { Crown, Heart, Infinity, Palette, Shield } from 'lucide-react';
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';

interface TrinityRingChartProps {
  truthScore: number;
  goodnessScore: number;
  beautyScore: number;
  serenityScore: number;
  eternityScore: number;
  vetoTriggered?: boolean;
  vetoPillars?: string[];
  className?: string;
  onPillarClick?: (pillar: string) => void; // Ring→Log 딥링크
}

// 커스텀 툴팁 컴포넌트 (render 외부 선언)
const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    const IconComponent = data.icon;

    return (
      <div className="bg-gray-800 border border-gray-600 rounded-lg p-3 shadow-lg">
        <div className="flex items-center space-x-2 mb-2">
          <IconComponent className="w-4 h-4" style={{ color: data.color }} />
          <span className="font-semibold text-white">{data.label}</span>
          {data.isVetoed && (
            <span className="text-xs bg-red-500 text-white px-2 py-1 rounded">
              VETO
            </span>
          )}
        </div>
        <div className="space-y-1 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-400">점수:</span>
            <span className="text-white font-mono">{data.score}/100</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">가중치:</span>
            <span className="text-white font-mono">{data.displayValue.toFixed(1)}%</span>
          </div>
          <div className="text-xs text-gray-500 mt-2">
            {data.description}
          </div>
        </div>
      </div>
    );
  }
  return null;
};

// 헌법 v1.0 가중치 (런타임 계산용)
const TRINITY_WEIGHTS = {
  truth: 0.35,
  goodness: 0.35,
  beauty: 0.20,
  serenity: 0.08,
  eternity: 0.02,
};

// 5기둥별 색상 및 아이콘
const PILLAR_CONFIG = {
  truth: {
    color: '#3b82f6', // blue-500
    hoverColor: '#1d4ed8', // blue-700
    icon: Crown,
    label: '眞 Truth',
    description: '기술적 정확성'
  },
  goodness: {
    color: '#10b981', // emerald-500
    hoverColor: '#047857', // emerald-700
    icon: Shield,
    label: '善 Goodness',
    description: '윤리·안정성'
  },
  beauty: {
    color: '#8b5cf6', // violet-500
    hoverColor: '#7c3aed', // violet-700
    icon: Palette,
    label: '美 Beauty',
    description: '구조적 우아함'
  },
  serenity: {
    color: '#ec4899', // pink-500
    hoverColor: '#be185d', // pink-700
    icon: Heart,
    label: '孝 Serenity',
    description: '사용자 마찰 제거'
  },
  eternity: {
    color: '#06b6d4', // cyan-500
    hoverColor: '#0891b2', // cyan-700
    icon: Infinity,
    label: '永 Eternity',
    description: '영속성·기록 보존'
  },
};

export default function TrinityRingChart({
  truthScore,
  goodnessScore,
  beautyScore,
  serenityScore,
  eternityScore,
  vetoTriggered = false,
  vetoPillars = [],
  className = "",
  onPillarClick
}: TrinityRingChartProps) {

  // 헌법 가중치에 따른 Ring 데이터 생성
  const createRingData = () => {
    const scores = {
      truth: truthScore,
      goodness: goodnessScore,
      beauty: beautyScore,
      serenity: serenityScore,
      eternity: eternityScore,
    };

    return Object.entries(scores).map(([pillar, score]) => {
      const weight = TRINITY_WEIGHTS[pillar as keyof typeof TRINITY_WEIGHTS];
      const config = PILLAR_CONFIG[pillar as keyof typeof PILLAR_CONFIG];

      // Veto 상태 확인
      const isVetoed = vetoPillars.includes(pillar);

      return {
        name: pillar,
        value: weight * 100, // Ring 크기는 가중치로 결정
        score: Math.round(score),
        displayValue: weight * 100,
        color: isVetoed ? '#ef4444' : config.color, // Veto 시 붉은색
        hoverColor: isVetoed ? '#dc2626' : config.hoverColor,
        icon: config.icon,
        label: config.label,
        description: config.description,
        isVetoed,
      };
    });
  };

  const data = createRingData();

  // 커스텀 레이블 (아이콘 표시)
  const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, index }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    const item = data[index];
    const IconComponent = item.icon;

    return (
      <g>
        <IconComponent
          x={x - 8}
          y={y - 8}
          width={16}
          height={16}
          fill={item.color}
        />
      </g>
    );
  };

  return (
    <div className={`w-full h-80 ${className}`}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={120}
            paddingAngle={2}
            dataKey="value"
            label={renderCustomLabel}
            labelLine={false}
            onClick={(data: any) => {
              if (onPillarClick && data && data.name) {
                onPillarClick(data.name);
              }
            }}
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.color}
                stroke={entry.isVetoed ? '#ef4444' : '#374151'}
                strokeWidth={entry.isVetoed ? 3 : 1}
                style={{ cursor: onPillarClick ? 'pointer' : 'default' }}
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>

      {/* Veto 경고 표시 */}
      {vetoTriggered && (
        <div className="mt-4 p-3 bg-red-500/10 border border-red-500/50 rounded-lg">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
            <span className="text-red-400 font-semibold text-sm">
              Amendment 0001: Veto Triggered - Commander Approval Required
            </span>
          </div>
          <div className="text-xs text-red-300 mt-1">
            Low pillars: {vetoPillars.join(', ')}
          </div>
        </div>
      )}

      {/* 범례 */}
      <div className="mt-4 grid grid-cols-3 gap-2 text-xs">
        {data.map((item) => {
          const IconComponent = item.icon;
          return (
            <div key={item.name} className="flex items-center space-x-1">
              <IconComponent className="w-3 h-3" style={{ color: item.color }} />
              <span className={`font-medium ${item.isVetoed ? 'text-red-400' : 'text-gray-300'}`}>
                {item.label}
              </span>
              <span className="text-gray-500">
                {item.score}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
