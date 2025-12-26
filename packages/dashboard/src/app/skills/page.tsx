'use client';

import React from 'react';
import { SkillsRegistry } from '@/components/skills/SkillsRegistry';
import { SkillExecutionResult } from '@/components/skills/types';

export default function SkillsPage() {
  const handleSkillExecute = (result: SkillExecutionResult) => {
    console.log('Skill execution result:', result);

    // 향후 확장 가능: 실행 결과 로깅, 알림 표시 등
    // - 성공 시 토스트 알림
    // - 실패 시 에러 모달
    // - 실행 히스토리 저장
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%239C92AC" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="4"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-20"></div>

      <div className="relative container mx-auto px-6 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <span className="text-2xl">⚔️</span>
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">Skills Manager</h1>
              <p className="text-gray-400 mt-1">
                AFO Kingdom의 지능적 능력을 탐색하고 활용하세요
              </p>
            </div>
          </div>

          {/* Breadcrumb */}
          <nav className="flex items-center gap-2 text-sm text-gray-500">
            <span>🏰 AFO Kingdom</span>
            <span>›</span>
            <span className="text-gray-300">Skills Manager</span>
          </nav>
        </div>

        {/* Skills Registry Widget */}
        <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-2xl p-8">
          <SkillsRegistry
            autoRefresh={true}
            refreshInterval={30000}
            onSkillExecute={handleSkillExecute}
          />
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center gap-6 px-6 py-3 bg-white/5 backdrop-blur-md border border-white/10 rounded-full">
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <span>眞</span>
              <span className="text-blue-400 font-medium">Technical Certainty</span>
            </div>
            <div className="w-1 h-1 bg-gray-600 rounded-full"></div>
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <span>善</span>
              <span className="text-green-400 font-medium">Ethical Priority</span>
            </div>
            <div className="w-1 h-1 bg-gray-600 rounded-full"></div>
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <span>美</span>
              <span className="text-purple-400 font-medium">Clear Storytelling</span>
            </div>
            <div className="w-1 h-1 bg-gray-600 rounded-full"></div>
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <span>孝</span>
              <span className="text-orange-400 font-medium">Frictionless Operation</span>
            </div>
          </div>

          <p className="text-xs text-gray-600 mt-4">
            AFO Kingdom Skills Registry • Trinity Score 기반 • DRY_RUN 지원 • Auto-refresh 30초
          </p>
        </div>
      </div>
    </div>
  );
}