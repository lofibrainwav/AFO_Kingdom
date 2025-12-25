"use client";

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface VisualAgentAction {
  type: 'click' | 'type' | 'scroll' | 'wait' | 'goto' | 'done';
  bbox?: { x: number; y: number; w: number; h: number };
  text?: string;
  confidence: number;
  why: string;
  safety: 'safe' | 'confirm' | 'block';
}

interface VisualAgentPlan {
  goal: string;
  actions: VisualAgentAction[];
  stop: boolean;
  summary: string;
}

interface VisualAgentOverlayProps {
  plan?: VisualAgentPlan;
  onAnalyzeScreenshot: (goal: string) => Promise<void>;
  onExecuteAction: (actionIndex: number) => Promise<void>;
  onExecutePlan: () => Promise<void>;
  onPause: () => void;
  isRunning: boolean;
  currentStep: number;
  screenshot?: string;
  executionResults?: Array<{
    action: VisualAgentAction;
    status: 'executed' | 'blocked' | 'error' | 'failed';
    reason?: string;
  }>;
}

export const VisualAgentOverlay: React.FC<VisualAgentOverlayProps> = ({
  plan,
  onAnalyzeScreenshot,
  onExecuteAction,
  onExecutePlan,
  onPause,
  isRunning,
  currentStep,
  screenshot,
  executionResults = []
}) => {
  const [goal, setGoal] = useState('');
  const [selectedAction, setSelectedAction] = useState<number | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // 캔버스에 bbox 오버레이 그리기
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !plan) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // 캔버스 초기화
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 각 액션에 대한 bbox 그리기
    plan.actions.forEach((action, index) => {
      if (!action.bbox) return;

      const alpha = action.safety === 'block' ? 0.3 : action.safety === 'confirm' ? 0.7 : 1.0;

      // bbox 색상 (안전도에 따라)
      let color = '#10b981'; // green for safe
      if (action.safety === 'confirm') color = '#f59e0b'; // yellow for confirm
      if (action.safety === 'block') color = '#ef4444'; // red for block

      // Denormalize bbox for canvas (0-1 -> screen coordinates)
      const screenX = action.bbox.x * canvas.width;
      const screenY = action.bbox.y * canvas.height;
      const screenW = action.bbox.w * canvas.width;
      const screenH = action.bbox.h * canvas.height;

      // bbox 사각형 그리기
      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.globalAlpha = alpha;
      ctx.strokeRect(screenX, screenY, screenW, screenH);

      // 신뢰도 텍스트
      ctx.fillStyle = color;
      ctx.font = '12px Arial';
      ctx.fillText(
        `${Math.round(action.confidence * 100)}%`,
        screenX + 5,
        screenY - 5
      );

      // 액션 타입 표시
      ctx.fillStyle = color;
      ctx.fillText(
        action.type.toUpperCase(),
        screenX + screenW - 30,
        screenY + 15
      );
    });

    ctx.globalAlpha = 1.0;
  }, [plan]);

  const handleAnalyze = async () => {
    if (!goal.trim()) return;
    await onAnalyzeScreenshot(goal);
  };

  const getSafetyColor = (safety: string) => {
    switch (safety) {
      case 'safe': return 'text-green-400 border-green-400';
      case 'confirm': return 'text-yellow-400 border-yellow-400';
      case 'block': return 'text-red-400 border-red-400';
      default: return 'text-gray-400 border-gray-400';
    }
  };

  const getSafetyIcon = (safety: string) => {
    switch (safety) {
      case 'safe': return '✅';
      case 'confirm': return '⚠️';
      case 'block': return '🚫';
      default: return '❓';
    }
  };

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'executed': return 'text-green-400';
      case 'blocked': return 'text-red-400';
      case 'error': return 'text-red-500';
      case 'failed': return 'text-yellow-500';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="fixed inset-0 pointer-events-none z-50">
      {/* 스크린샷 배경 (있는 경우) */}
      {screenshot && (
        <img
          src={screenshot}
          alt="Current screen"
          className="w-full h-full object-contain"
        />
      )}

      {/* Canvas 오버레이 */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full"
        width={1920}
        height={1080}
      />

      {/* 메인 컨트롤 패널 */}
      <motion.div
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        className="absolute bottom-4 left-1/2 transform -translate-x-1/2 pointer-events-auto"
      >
        <div className="bg-black/80 backdrop-blur-sm rounded-lg p-4 border border-gray-700 min-w-96">
          <div className="flex items-center space-x-2 mb-3">
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Enter goal for Visual Agent..."
              className="flex-1 px-3 py-2 bg-gray-800 border border-gray-600 rounded text-white text-sm focus:outline-none focus:border-blue-400"
              onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
            />
            <button
              onClick={handleAnalyze}
              disabled={!goal.trim() || isRunning}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded font-medium transition-colors"
            >
              Analyze
            </button>
          </div>

          {plan && (
            <div className="text-center mb-3">
              <div className="text-white text-sm font-medium">{plan.goal}</div>
              <div className="text-gray-400 text-xs">{plan.summary}</div>
            </div>
          )}

          <div className="flex space-x-2">
            <button
              onClick={() => onExecuteAction(currentStep)}
              disabled={!plan || isRunning || currentStep >= (plan?.actions.length || 0)}
              className="px-3 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded font-medium transition-colors text-sm"
            >
              Step ({currentStep + 1}/{plan?.actions.length || 0})
            </button>

            <button
              onClick={isRunning ? onPause : onExecutePlan}
              disabled={!plan}
              className={`px-3 py-2 text-white rounded font-medium transition-colors text-sm ${
                isRunning
                  ? 'bg-yellow-600 hover:bg-yellow-700'
                  : 'bg-green-600 hover:bg-green-700'
              }`}
            >
              {isRunning ? 'Pause' : 'Run All'}
            </button>
          </div>
        </div>
      </motion.div>

      {/* 액션 리스트 패널 */}
      {plan && (
        <motion.div
          initial={{ x: 400 }}
          animate={{ x: 0 }}
          className="absolute right-4 top-4 w-96 max-h-96 overflow-y-auto bg-black/80 backdrop-blur-sm rounded-lg border border-gray-700 pointer-events-auto"
        >
          <div className="p-4">
            <h3 className="text-white font-bold mb-3">Visual Agent Plan</h3>

            <div className="space-y-2">
              {plan.actions.map((action, index) => {
                const result = executionResults[index];
                const isCurrent = index === currentStep;
                const isExecuted = result?.status === 'executed';

                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`p-3 rounded border cursor-pointer transition-all ${
                      isCurrent
                        ? 'bg-blue-900/50 border-blue-400 ring-2 ring-blue-400'
                        : selectedAction === index
                        ? 'bg-blue-900/30 border-blue-400'
                        : `bg-gray-800/50 ${getSafetyColor(action.safety)}`
                    } ${isExecuted ? 'opacity-75' : ''}`}
                    onClick={() => setSelectedAction(index)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-white font-medium">
                        {index + 1}. {action.type.toUpperCase()}
                      </span>
                      <div className="flex items-center space-x-2">
                        {result && (
                          <span className={`text-sm ${getStatusColor(result.status)}`}>
                            {result.status === 'executed' ? '✅' :
                             result.status === 'blocked' ? '🚫' :
                             result.status === 'error' ? '❌' : '⚠️'}
                          </span>
                        )}
                        <span className="text-sm">
                          {getSafetyIcon(action.safety)}
                        </span>
                      </div>
                    </div>

                    <div className="text-sm text-gray-300 mb-1">
                      {action.why}
                    </div>

                    <div className="text-xs text-gray-400">
                      Confidence: {Math.round(action.confidence * 100)}%
                      {action.bbox && (
                        <> | Bbox: {action.bbox.x.toFixed(2)},{action.bbox.y.toFixed(2)} {action.bbox.w.toFixed(2)}x{action.bbox.h.toFixed(2)}</>
                      )}
                    </div>

                    {action.text && (
                      <div className="text-xs text-blue-300 mt-1">
                        Text: "{action.text}"
                      </div>
                    )}

                    {result?.reason && (
                      <div className="text-xs text-red-300 mt-1">
                        Reason: {result.reason}
                      </div>
                    )}
                  </motion.div>
                );
              })}
            </div>
          </div>
        </motion.div>
      )}

      {/* 진행 상태 표시 */}
      <AnimatePresence>
        {isRunning && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium"
          >
            Executing Step {currentStep + 1}...
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};