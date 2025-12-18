'use client';

import { useCallback, useEffect, useState } from 'react';
import { TrinityGlowCard } from './TrinityGlowCard';
import { useSpatialAudio } from '../hooks/useSpatialAudio';

interface SerenityProgress {
  status: 'idle' | 'generating' | 'capturing' | 'evaluating' | 'complete' | 'failed';
  iteration: number;
  maxIterations: number;
  trinityScore: number;
  riskScore: number;
  feedback: string;
  code?: string;
  screenshotUrl?: string;
}

interface SerenityMonitorProps {
  apiEndpoint?: string;
  onComplete?: (result: any) => void;
}

/**
 * SerenityMonitor - Project Serenity Frontend
 * 
 * Real-time visualization of autonomous UI creation:
 * - Progress through iteration loop
 * - Trinity/Risk scores with Glow animation
 * - Spatial audio feedback on state changes
 */
export function SerenityMonitor({ 
  apiEndpoint = '/api/serenity/create',
  onComplete 
}: SerenityMonitorProps) {
  const [prompt, setPrompt] = useState('');
  const [progress, setProgress] = useState<SerenityProgress>({
    status: 'idle',
    iteration: 0,
    maxIterations: 3,
    trinityScore: 0.85,
    riskScore: 0.15,
    feedback: '',
  });
  const [isCreating, setIsCreating] = useState(false);
  
  const { playTrinityUp, playRiskUp, initAudio } = useSpatialAudio();
  const [prevScore, setPrevScore] = useState(0.85);

  // Play audio on score changes
  useEffect(() => {
    if (progress.trinityScore > prevScore + 0.05) {
      playTrinityUp();
    } else if (progress.riskScore > 0.2) {
      playRiskUp();
    }
    setPrevScore(progress.trinityScore);
  }, [progress.trinityScore, progress.riskScore, prevScore, playTrinityUp, playRiskUp]);

  const startCreation = useCallback(async () => {
    if (!prompt.trim()) return;
    
    initAudio(); // Initialize audio on user interaction
    setIsCreating(true);
    
    try {
      // Simulate SSE connection for real-time updates
      setProgress(p => ({ ...p, status: 'generating', iteration: 1 }));
      
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      
      const result = await response.json();
      
      setProgress({
        status: result.success ? 'complete' : 'failed',
        iteration: result.iteration,
        maxIterations: 3,
        trinityScore: result.trinity_score,
        riskScore: result.risk_score,
        feedback: result.feedback,
        code: result.code,
        screenshotUrl: result.screenshot_url,
      });
      
      onComplete?.(result);
    } catch (error) {
      setProgress(p => ({
        ...p,
        status: 'failed',
        feedback: `Error: ${error}`,
      }));
    } finally {
      setIsCreating(false);
    }
  }, [prompt, apiEndpoint, initAudio, onComplete]);

  const getStatusIcon = () => {
    switch (progress.status) {
      case 'idle': return '💭';
      case 'generating': return '🎨';
      case 'capturing': return '📸';
      case 'evaluating': return '⚖️';
      case 'complete': return '✅';
      case 'failed': return '❌';
    }
  };

  const getStatusText = () => {
    switch (progress.status) {
      case 'idle': return 'Ready to create';
      case 'generating': return 'GenUI creating code...';
      case 'capturing': return 'Capturing screenshot...';
      case 'evaluating': return 'Chancellor evaluating...';
      case 'complete': return 'Creation complete!';
      case 'failed': return 'Creation failed';
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ 
        fontSize: '1.5rem', 
        fontWeight: 'bold', 
        color: 'white',
        marginBottom: '1rem',
        textAlign: 'center'
      }}>
        🌟 Project Serenity
      </h1>
      
      {/* Input */}
      <div style={{ marginBottom: '1.5rem' }}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe the UI you want to create..."
          disabled={isCreating}
          style={{
            width: '100%',
            padding: '1rem',
            borderRadius: '8px',
            background: 'rgba(255,255,255,0.1)',
            border: '1px solid rgba(255,255,255,0.2)',
            color: 'white',
            fontSize: '1rem',
            minHeight: '80px',
            resize: 'vertical',
          }}
        />
        <button
          onClick={startCreation}
          disabled={isCreating || !prompt.trim()}
          style={{
            width: '100%',
            padding: '0.75rem',
            marginTop: '0.5rem',
            borderRadius: '8px',
            background: isCreating ? '#4b5563' : '#22c55e',
            color: 'white',
            fontWeight: 'bold',
            cursor: isCreating ? 'wait' : 'pointer',
            border: 'none',
          }}
        >
          {isCreating ? '🔄 Creating...' : '✨ Create UI'}
        </button>
      </div>
      
      {/* Progress Display */}
      <TrinityGlowCard 
        trinityScore={progress.trinityScore} 
        riskScore={progress.riskScore}
      >
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
            {getStatusIcon()}
          </div>
          <div style={{ color: 'white', fontWeight: '600' }}>
            {getStatusText()}
          </div>
          {progress.iteration > 0 && (
            <div style={{ color: '#9ca3af', fontSize: '0.875rem', marginTop: '0.25rem' }}>
              Iteration {progress.iteration}/{progress.maxIterations}
            </div>
          )}
        </div>
        
        {/* Feedback */}
        {progress.feedback && (
          <div style={{
            marginTop: '1rem',
            padding: '0.75rem',
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '8px',
            color: '#d1d5db',
            fontSize: '0.875rem',
          }}>
            💬 {progress.feedback}
          </div>
        )}
      </TrinityGlowCard>
      
      {/* Screenshot Preview */}
      {progress.screenshotUrl && (
        <div style={{ marginTop: '1.5rem' }}>
          <h3 style={{ color: 'white', marginBottom: '0.5rem' }}>📸 Preview</h3>
          <img 
            src={progress.screenshotUrl}
            alt="Generated UI"
            style={{
              width: '100%',
              borderRadius: '8px',
              border: '1px solid rgba(255,255,255,0.2)'
            }}
          />
        </div>
      )}
    </div>
  );
}

export default SerenityMonitor;
