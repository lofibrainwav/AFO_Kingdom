/**
 * KingdomChronicleTimeline.tsx
 * 
 * AFO 왕국 92커밋 연대기 타임라인 위젯
 * "역사를 모르는 자는 미래를 만들 수 없다." — 孫子
 * 
 * Design: Glassmorphism + Gradient + Timeline
 */
'use client';

import React from 'react';

interface Phase {
  phase: string;
  title: string;
  desc: string;
  commits?: string;
  color: string;
  icon: string;
}

const phases: Phase[] = [
  { phase: "0", title: "Genesis", desc: "초심 설정 · 승상 탄생", commits: "5", color: "#9333EA", icon: "🌟" },
  { phase: "1", title: "Security Hardening", desc: "善의 방패 · GitHub Actions", commits: "10", color: "#EF4444", icon: "🛡️" },
  { phase: "2", title: "CI/CD Stabilization", desc: "眞의 기반 · 290 테스트", commits: "30", color: "#3B82F6", icon: "⚙️" },
  { phase: "3", title: "MCP Ecosystem", desc: "孝의 연결 · Context7", commits: "10", color: "#22C55E", icon: "🔗" },
  { phase: "4-6", title: "Trinity Governance", desc: "균형의 통치 · 라우팅", commits: "15", color: "#06B6D4", icon: "⚖️" },
  { phase: "7-9", title: "Autonomous Kingdom", desc: "永의 자율 · GenUI", commits: "15", color: "#10B981", icon: "🤖" },
  { phase: "10", title: "Final Polish", desc: "美의 광택 · 100% Clean", commits: "7", color: "#EC4899", icon: "✨" },
  { phase: "現", title: "SSOT 100.0", desc: "왕국 완성", color: "#FBBF24", icon: "👑" },
];

export function KingdomChronicleTimeline() {
  return (
    <div 
      className="chronicle-timeline"
      style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(88, 28, 135, 0.3))',
        backdropFilter: 'blur(20px)',
        borderRadius: '24px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '32px',
        maxWidth: '800px',
        margin: '0 auto',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
      }}
    >
      {/* Header */}
      <h2 
        style={{
          fontSize: '28px',
          fontWeight: 'bold',
          textAlign: 'center',
          background: 'linear-gradient(to right, #22D3EE, #A855F7)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          marginBottom: '8px',
        }}
      >
        🏰 AFO 왕국 진화 연대기
      </h2>
      <p style={{ textAlign: 'center', color: 'rgba(255,255,255,0.7)', marginBottom: '32px', fontStyle: 'italic' }}>
        "역사를 모르는 자는 미래를 만들 수 없다." — 孫子
      </p>

      {/* Timeline */}
      <div style={{ position: 'relative', paddingLeft: '40px' }}>
        {/* Vertical Line */}
        <div 
          style={{
            position: 'absolute',
            left: '16px',
            top: '0',
            bottom: '0',
            width: '2px',
            background: 'linear-gradient(to bottom, #22D3EE, #A855F7, #FBBF24)',
          }}
        />

        {phases.map((p, i) => (
          <div 
            key={i}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '20px',
              marginBottom: '24px',
              position: 'relative',
            }}
          >
            {/* Circle Node */}
            <div 
              style={{
                position: 'absolute',
                left: '-32px',
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                background: p.color,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '16px',
                boxShadow: `0 0 20px ${p.color}50`,
                zIndex: 1,
              }}
            >
              {p.icon}
            </div>

            {/* Content Card */}
            <div 
              style={{
                flex: 1,
                background: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '12px',
                padding: '16px 20px',
                border: `1px solid ${p.color}30`,
                transition: 'all 0.3s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                e.currentTarget.style.transform = 'translateX(8px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)';
                e.currentTarget.style.transform = 'translateX(0)';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span 
                  style={{
                    background: p.color,
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    fontWeight: 'bold',
                  }}
                >
                  Phase {p.phase}
                </span>
                {p.commits && (
                  <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: '12px' }}>
                    {p.commits} commits
                  </span>
                )}
              </div>
              <h3 style={{ color: 'white', fontSize: '18px', fontWeight: 'bold', marginTop: '8px' }}>
                {p.title}
              </h3>
              <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '14px', marginTop: '4px' }}>
                {p.desc}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Footer Stats */}
      <div 
        style={{
          marginTop: '32px',
          padding: '20px',
          background: 'linear-gradient(135deg, rgba(34, 211, 238, 0.1), rgba(168, 85, 247, 0.1))',
          borderRadius: '16px',
          border: '1px solid rgba(255,255,255,0.1)',
          textAlign: 'center',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'center', gap: '40px', flexWrap: 'wrap' }}>
          <div>
            <div style={{ color: '#22D3EE', fontSize: '32px', fontWeight: 'bold' }}>92</div>
            <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '14px' }}>Total Commits</div>
          </div>
          <div>
            <div style={{ color: '#A855F7', fontSize: '32px', fontWeight: 'bold' }}>100.0</div>
            <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '14px' }}>SSOT Score</div>
          </div>
          <div>
            <div style={{ color: '#22C55E', fontSize: '32px', fontWeight: 'bold' }}>290+</div>
            <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '14px' }}>Tests Passing</div>
          </div>
        </div>
        <p style={{ color: '#FBBF24', marginTop: '16px', fontWeight: 'bold', fontSize: '16px' }}>
          眞善美孝永 — 다섯 기둥이 왕국을 지탱합니다
        </p>
      </div>
    </div>
  );
}

export default KingdomChronicleTimeline;
