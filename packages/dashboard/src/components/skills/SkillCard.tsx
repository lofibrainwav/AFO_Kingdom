'use client';

import React from 'react';
import { SkillCardProps, calculatePhilosophyAverage, getPhilosophyGrade, getTrinityScore } from './types';

export const SkillCard: React.FC<SkillCardProps> = ({
  skill,
  onExecute,
  isExecuting = false,
  executionResult
}) => {
  const philosophyAvg = calculatePhilosophyAverage(skill.philosophy_scores);
  const philosophyGrade = getPhilosophyGrade(philosophyAvg);
  const trinityScore = getTrinityScore(skill.philosophy_scores);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400';
      case 'experimental': return 'text-yellow-400';
      case 'maintenance': return 'text-orange-400';
      case 'deprecated': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getExecutionModeIcon = (mode: string) => {
    switch (mode) {
      case 'sync': return '⚡';
      case 'async': return '🔄';
      case 'streaming': return '🌊';
      case 'background': return '🎭';
      default: return '❓';
    }
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      strategic_command: 'border-blue-500/30 bg-blue-500/10',
      rag_systems: 'border-purple-500/30 bg-purple-500/10',
      workflow_automation: 'border-green-500/30 bg-green-500/10',
      health_monitoring: 'border-red-500/30 bg-red-500/10',
      memory_management: 'border-yellow-500/30 bg-yellow-500/10',
      browser_automation: 'border-cyan-500/30 bg-cyan-500/10',
      analysis_evaluation: 'border-pink-500/30 bg-pink-500/10',
      integration: 'border-indigo-500/30 bg-indigo-500/10',
      metacognition: 'border-emerald-500/30 bg-emerald-500/10'
    };
    return colors[category] || 'border-gray-500/30 bg-gray-500/10';
  };

  return (
    <div className={`
      relative overflow-hidden rounded-xl border backdrop-blur-md
      ${getCategoryColor(skill.category)}
      transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl
      group cursor-pointer
    `}>

      {/* Glassmorphism Background Effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      {/* Header */}
      <div className="relative p-4 border-b border-white/10">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-white mb-1 group-hover:text-blue-300 transition-colors">
              {skill.name}
            </h3>
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(skill.status)} bg-current/10`}>
                {skill.status.toUpperCase()}
              </span>
              <span className="text-gray-500">•</span>
              <span>v{skill.version}</span>
              <span className="text-gray-500">•</span>
              <span>{getExecutionModeIcon(skill.execution_mode)}</span>
            </div>
          </div>

          {/* Trinity Score Badge */}
          <div className="flex flex-col items-end gap-1">
            <div className="text-right">
              <div className="text-xs text-gray-400 mb-1">Trinity Score</div>
              <div className={`text-lg font-bold ${
                trinityScore >= 90 ? 'text-yellow-400' :
                trinityScore >= 80 ? 'text-green-400' :
                trinityScore >= 70 ? 'text-blue-400' : 'text-gray-400'
              }`}>
                {trinityScore.toFixed(1)}
              </div>
            </div>
          </div>
        </div>

        <p className="text-sm text-gray-300 leading-relaxed">
          {skill.description}
        </p>
      </div>

      {/* Philosophy Scores */}
      <div className="relative p-4 border-b border-white/10">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-medium text-gray-300">Philosophy Scores</h4>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-400">Grade:</span>
            <span className={`px-2 py-1 rounded text-xs font-bold ${
              philosophyGrade === 'S' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
              philosophyGrade === 'A' ? 'bg-green-500/20 text-green-400 border border-green-500/30' :
              philosophyGrade === 'B' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' :
              'bg-gray-500/20 text-gray-400 border border-gray-500/30'
            }`}>
              {philosophyGrade}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-blue-400">眞 Truth</span>
              <span className="text-white font-medium">{skill.philosophy_scores.truth}%</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-green-400">善 Goodness</span>
              <span className="text-white font-medium">{skill.philosophy_scores.goodness}%</span>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-purple-400">美 Beauty</span>
              <span className="text-white font-medium">{skill.philosophy_scores.beauty}%</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-orange-400">孝 Serenity</span>
              <span className="text-white font-medium">{skill.philosophy_scores.serenity}%</span>
            </div>
          </div>
        </div>

        <div className="mt-3 pt-3 border-t border-white/10">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Average Score</span>
            <span className="text-white font-medium">{philosophyAvg.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      {/* Capabilities */}
      <div className="relative p-4 border-b border-white/10">
        <h4 className="text-sm font-medium text-gray-300 mb-2">Capabilities</h4>
        <div className="flex flex-wrap gap-1">
          {skill.capabilities.slice(0, 4).map((capability, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-white/5 border border-white/10 rounded-md text-xs text-gray-300 hover:bg-white/10 transition-colors"
            >
              {capability.replace(/_/g, ' ')}
            </span>
          ))}
          {skill.capabilities.length > 4 && (
            <span className="px-2 py-1 bg-gray-500/20 border border-gray-500/30 rounded-md text-xs text-gray-400">
              +{skill.capabilities.length - 4} more
            </span>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="relative p-4">
        <div className="flex gap-2">
          <button
            onClick={() => onExecute(skill.skill_id, true)}
            disabled={isExecuting}
            className="flex-1 px-4 py-2 bg-blue-500/20 border border-blue-500/30 rounded-lg text-blue-400 hover:bg-blue-500/30 hover:border-blue-500/50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {isExecuting ? '🔄 Executing...' : '🎭 DRY RUN'}
          </button>
          <button
            onClick={() => onExecute(skill.skill_id, false)}
            disabled={isExecuting}
            className="flex-1 px-4 py-2 bg-green-500/20 border border-green-500/30 rounded-lg text-green-400 hover:bg-green-500/30 hover:border-green-500/50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {isExecuting ? '🔄 Executing...' : '🚀 EXECUTE'}
          </button>
        </div>

        {/* Execution Result */}
        {executionResult && (
          <div className={`mt-3 p-3 rounded-lg border ${
            executionResult.status === 'dry_run_success' ? 'bg-blue-500/10 border-blue-500/30' :
            executionResult.status === 'completed' ? 'bg-green-500/10 border-green-500/30' :
            executionResult.status === 'failed' ? 'bg-red-500/10 border-red-500/30' :
            'bg-yellow-500/10 border-yellow-500/30'
          }`}>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-sm font-medium">
                {executionResult.status === 'dry_run_success' ? '✅ DRY RUN Success' :
                 executionResult.status === 'completed' ? '✅ Execution Success' :
                 executionResult.status === 'failed' ? '❌ Execution Failed' :
                 '🔄 Executing...'}
              </span>
            </div>
            {executionResult.error && (
              <p className="text-xs text-red-400 mt-1">{executionResult.error}</p>
            )}
            {executionResult.result && (
              <p className="text-xs text-gray-300 mt-1 truncate">
                Result: {JSON.stringify(executionResult.result).slice(0, 100)}...
              </p>
            )}
          </div>
        )}
      </div>

      {/* Hover Effect Overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 via-purple-500/5 to-green-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
    </div>
  );
};