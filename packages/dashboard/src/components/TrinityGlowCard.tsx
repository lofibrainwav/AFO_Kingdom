'use client';

import { useEffect, useState } from 'react';

// Breakdown Interface
export interface TrinityBreakdown {
  truth: number;
  goodness: number;
  beauty: number;
  filial_serenity: number;
  eternity: number;
}

interface TrinityGlowCardProps {
  trinityScore: number; // 0.0 - 1.0
  riskScore: number;    // 0.0 - 1.0
  breakdown?: TrinityBreakdown;
  children?: React.ReactNode;
}

/**
 * TrinityGlowCard - Phase 7 Sensory Integration
 * 
 * Displays a pulsing glow based on Trinity/Risk scores:
 * - Trinity ≥ 0.9: Bright green pulse (Safe)
 * - Trinity 0.7-0.9: Yellow steady glow (Caution)
 * - Trinity < 0.7: Red warning pulse (Alert)
 * - High Risk: Dark red aura overlay
 */
export function TrinityGlowCard({ trinityScore, riskScore, breakdown, children }: TrinityGlowCardProps) {
  const [pulseScale, setPulseScale] = useState(1);

  // Animate pulse
  useEffect(() => {
    const interval = setInterval(() => {
      setPulseScale(prev => prev === 1 ? 1.02 : 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Determine glow color based on score
  const getGlowColor = (): string => {
    if (trinityScore >= 0.9) return '#22c55e'; // Green
    if (trinityScore >= 0.7) return '#eab308'; // Yellow
    return '#ef4444'; // Red
  };

  const glowColor = getGlowColor();
  const glowStrength = Math.round(trinityScore * 30);
  const riskOverlay = riskScore > 0.1 ? riskScore * 0.3 : 0;

  return (
    <div style={{
      position: 'relative',
      padding: '1.5rem',
      borderRadius: '16px',
      background: 'rgba(0, 0, 0, 0.8)',
      boxShadow: `0 0 ${glowStrength}px ${glowColor}, 0 0 ${glowStrength * 2}px ${glowColor}`,
      transform: `scale(${pulseScale})`,
      transition: 'all 1s ease-in-out',
      minHeight: '200px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between'
    }}>
      {/* Risk Overlay */}
      {riskScore > 0.1 && (
        <div style={{
          position: 'absolute',
          inset: 0,
          borderRadius: '16px',
          background: `rgba(239, 68, 68, ${riskOverlay})`,
          pointerEvents: 'none',
        }} />
      )}
      
      {/* Content */}
      <div style={{ position: 'relative', zIndex: 1 }}>
        {children}
      </div>

      {/* Breakdown Display */}
      {breakdown && (
          <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: '1rem',
              borderTop: '1px solid rgba(255,255,255,0.1)',
              paddingTop: '0.5rem',
              fontSize: '0.7rem',
              color: '#d1d5db'
          }}>
              <div title="Truth (35%)" style={{textAlign: 'center'}}>
                 <div style={{color: '#3b82f6'}}>眞</div>
                 <div>{(breakdown.truth * 100).toFixed(0)}</div>
              </div>
              <div title="Goodness (35%)" style={{textAlign: 'center'}}>
                 <div style={{color: '#22c55e'}}>善</div>
                 <div>{(breakdown.goodness * 100).toFixed(0)}</div>
              </div>
              <div title="Beauty (20%)" style={{textAlign: 'center'}}>
                 <div style={{color: '#ec4899'}}>美</div>
                 <div>{(breakdown.beauty * 100).toFixed(0)}</div>
              </div>
              <div title="Serenity (8%)" style={{textAlign: 'center'}}>
                 <div style={{color: '#a855f7'}}>孝</div>
                 <div>{(breakdown.filial_serenity * 100).toFixed(0)}</div>
              </div>
              <div title="Eternity (2%)" style={{textAlign: 'center'}}>
                 <div style={{color: '#f59e0b'}}>永</div>
                 <div>{(breakdown.eternity * 100).toFixed(0)}</div>
              </div>
          </div>
      )}

      {/* Score Display (Summary) */}
      {!breakdown && (
        <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginTop: '1rem',
            fontFamily: 'monospace',
            fontSize: '0.875rem',
        }}>
            <span style={{ color: glowColor, fontWeight: 600 }}>
            ⚖️ {(trinityScore * 100).toFixed(0)}%
            </span>
            {riskScore > 0.1 && (
            <span style={{ color: '#ef4444', fontWeight: 600 }}>
                ⚠️ Risk: {(riskScore * 100).toFixed(0)}%
            </span>
            )}
        </div>
      )}
    </div>
  );
}

export default TrinityGlowCard;
