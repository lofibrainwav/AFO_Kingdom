"use client";

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface VisualAgentAction {
  action_id: string;
  type: 'click' | 'type' | 'scroll' | 'wait' | 'goto';
  bbox: { x: number; y: number; w: number; h: number };
  text?: string;
  confidence: number;
  why: string;
  safety: 'safe' | 'confirm' | 'block';
}

interface VisualAgentOverlayProps {
  actions: VisualAgentAction[];
  onExecuteAction: (actionId: string) => void;
  onStep: () => void;
  onRun: () => void;
  onPause: () => void;
  isRunning: boolean;
  currentStep: number;
  screenshot?: string;
}

export const VisualAgentOverlay: React.FC<VisualAgentOverlayProps> = ({
  actions,
  onExecuteAction,
  onStep,
  onRun,
  onPause,
  isRunning,
  currentStep,
  screenshot
}) => {
  const [selectedAction, setSelectedAction] = useState<string | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // 캔버스에 bbox 오버레이 그리기
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // 캔버스 초기화
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 각 액션에 대한 bbox 그리기
    actions.forEach((action, index) => {
      const { bbox, confidence, safety } = action;
      const alpha = safety === 'block' ? 0.3 : safety === 'confirm' ? 0.7 : 1.0;

      // bbox 색상 (안전도에 따라)
      let color = '#10b981'; // green for safe
      if (safety === 'confirm') color = '#f59e0b'; // yellow for confirm
      if (safety === 'block') color = '#ef4444'; // red for block

      // bbox 사각형 그리기
      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.globalAlpha = alpha;
      ctx.strokeRect(bbox.x, bbox.y, bbox.w, bbox.h);

      // 신뢰도 텍스트
      ctx.fillStyle = color;
      ctx.font = '12px Arial';
      ctx.fillText(
        `${Math.round(confidence * 100)}%`,
        bbox.x + 5,
        bbox.y - 5
      );

      // 액션 타입 표시
      ctx.fillStyle = color;
      ctx.fillText(
        action.type.toUpperCase(),
        bbox.x + bbox.w - 30,
        bbox.y + 15
      );
    });

    ctx.globalAlpha = 1.0;
  }, [actions]);

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

      {/* 액션 리스트 패널 */}
      <motion.div
        initial={{ x: 400 }}
        animate={{ x: 0 }}
        className="absolute right-4 top-4 w-96 max-h-96 overflow-y-auto bg-black/80 backdrop-blur-sm rounded-lg border border-gray-700 pointer-events-auto"
      >
        <div className="p-4">
          <h3 className="text-white font-bold mb-3">Visual Agent Actions</h3>

          <div className="space-y-2">
            {actions.map((action, index) => (
              <motion.div
                key={action.action_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`p-3 rounded border cursor-pointer transition-all ${
                  selectedAction === action.action_id
                    ? 'bg-blue-900/50 border-blue-400'
                    : `bg-gray-800/50 ${getSafetyColor(action.safety)}`
                }`}
                onClick={() => setSelectedAction(action.action_id)}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-white font-medium">
                    {index + 1}. {action.type.toUpperCase()}
                  </span>
                  <span className="text-sm">
                    {getSafetyIcon(action.safety)}
                  </span>
                </div>

                <div className="text-sm text-gray-300 mb-1">
                  {action.why}
                </div>

                <div className="text-xs text-gray-400">
                  Confidence: {Math.round(action.confidence * 100)}% |
                  Bbox: {action.bbox.x},{action.bbox.y} {action.bbox.w}x{action.bbox.h}
                </div>

                {action.text && (
                  <div className="text-xs text-blue-300 mt-1">
                    Text: "{action.text}"
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* 컨트롤 패널 */}
      <motion.div
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        className="absolute bottom-4 left-1/2 transform -translate-x-1/2 pointer-events-auto"
      >
        <div className="flex space-x-2 bg-black/80 backdrop-blur-sm rounded-lg p-2 border border-gray-700">
          <button
            onClick={onStep}
            disabled={isRunning}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded font-medium transition-colors"
          >
            Step ({currentStep}/{actions.length})
          </button>

          <button
            onClick={isRunning ? onPause : onRun}
            className={`px-4 py-2 text-white rounded font-medium transition-colors ${
              isRunning
                ? 'bg-yellow-600 hover:bg-yellow-700'
                : 'bg-green-600 hover:bg-green-700'
            }`}
          >
            {isRunning ? 'Pause' : 'Run'}
          </button>
        </div>
      </motion.div>

      {/* 진행 상태 표시 */}
      <AnimatePresence>
        {isRunning && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium"
          >
            Executing Step {currentStep}...
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};