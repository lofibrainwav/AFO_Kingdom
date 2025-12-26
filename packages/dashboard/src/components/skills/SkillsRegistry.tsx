'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { SkillCard } from './SkillCard';
import {
  SkillsRegistryProps,
  SkillFilterOptions,
  AFOSkill,
  SkillsApiResponse,
  SkillExecutionResult,
  SkillExecutionState,
  SkillCategory
} from './types';

export const SkillsRegistry: React.FC<SkillsRegistryProps> = ({
  filters: initialFilters = {},
  autoRefresh = true,
  refreshInterval = 30000, // 30초
  onSkillExecute
}) => {
  const [skills, setSkills] = useState<AFOSkill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [executionStates, setExecutionStates] = useState<SkillExecutionState>({});

  // 필터 상태
  const [filters, setFilters] = useState<SkillFilterOptions>(initialFilters);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<SkillCategory | ''>('');
  const [minPhilosophyAvg, setMinPhilosophyAvg] = useState<number>(0);

  // 스킬 데이터 가져오기
  const fetchSkills = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const params = new URLSearchParams();
      if (selectedCategory) params.append('category', selectedCategory);
      if (searchTerm) params.append('search', searchTerm);
      if (minPhilosophyAvg > 0) params.append('minPhilosophyAvg', minPhilosophyAvg.toString());

      const response = await fetch(`/api/skills?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch skills: ${response.status}`);
      }

      const data: SkillsApiResponse = await response.json();
      setSkills(data.skills);
      setCategories(data.categories);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch skills');
      console.error('Skills fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, searchTerm, minPhilosophyAvg]);

  // 스킬 실행 핸들러
  const handleSkillExecute = async (skillId: string, dryRun: boolean = false) => {
    const skill = skills.find(s => s.skill_id === skillId);
    if (!skill) return;

    // 실행 상태 업데이트
    setExecutionStates(prev => ({
      ...prev,
      [skillId]: {
        isExecuting: true,
        lastExecuted: new Date()
      }
    }));

    try {
      const response = await fetch('/api/skills', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          skill_id: skillId,
          parameters: {}, // 향후 확장 가능
          dryRun
        }),
      });

      if (!response.ok) {
        throw new Error(`Execution failed: ${response.status}`);
      }

      const result: SkillExecutionResult = await response.json();

      // 실행 결과 업데이트
      setExecutionStates(prev => ({
        ...prev,
        [skillId]: {
          isExecuting: false,
          result,
          lastExecuted: new Date()
        }
      }));

      // 부모 컴포넌트에 알림
      onSkillExecute?.(result);

    } catch (err) {
      const errorResult: SkillExecutionResult = {
        skill_id: skillId,
        status: 'failed',
        error: err instanceof Error ? err.message : 'Unknown error',
        dry_run: dryRun
      };

      setExecutionStates(prev => ({
        ...prev,
        [skillId]: {
          isExecuting: false,
          result: errorResult,
          lastExecuted: new Date()
        }
      }));

      onSkillExecute?.(errorResult);
    }
  };

  // 필터 초기화
  const clearFilters = () => {
    setSearchTerm('');
    setSelectedCategory('');
    setMinPhilosophyAvg(0);
  };

  // 컴포넌트 마운트 시 데이터 로드
  useEffect(() => {
    fetchSkills();
  }, [fetchSkills]);

  // 자동 새로고침
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      fetchSkills();
    }, refreshInterval);

    return () => clearInterval(interval);
  }, [autoRefresh, refreshInterval, fetchSkills]);

  if (error) {
    return (
      <div className="p-6 bg-red-500/10 border border-red-500/30 rounded-lg backdrop-blur-md">
        <div className="flex items-center gap-3">
          <span className="text-red-400 text-xl">❌</span>
          <div>
            <h3 className="text-red-400 font-medium">Failed to load skills</h3>
            <p className="text-red-300 text-sm mt-1">{error}</p>
          </div>
        </div>
        <button
          onClick={fetchSkills}
          className="mt-3 px-4 py-2 bg-red-500/20 border border-red-500/30 rounded-lg text-red-400 hover:bg-red-500/30 transition-colors text-sm"
        >
          🔄 Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <span className="text-2xl">⚔️</span>
            Skills Registry
          </h2>
          <p className="text-gray-400 mt-1">
            AFO Kingdom의 19개 스킬을 탐색하고 실행하세요
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-sm text-gray-400">
            Total: {skills.length} skills
          </div>
          {autoRefresh && (
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              Auto-refresh: {refreshInterval / 1000}s
            </div>
          )}
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              🔍 Search Skills
            </label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="스킬 이름이나 설명으로 검색..."
              className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:border-blue-500/50 focus:outline-none transition-colors"
            />
          </div>

          {/* Category Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              📂 Category
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value as SkillCategory | '')}
              className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:border-blue-500/50 focus:outline-none transition-colors"
            >
              <option value="">All Categories</option>
              {categories.map(category => (
                <option key={category} value={category}>
                  {category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
          </div>

          {/* Philosophy Score Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              🎯 Min Philosophy Avg
            </label>
            <select
              value={minPhilosophyAvg}
              onChange={(e) => setMinPhilosophyAvg(Number(e.target.value))}
              className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:border-blue-500/50 focus:outline-none transition-colors"
            >
              <option value={0}>All Scores</option>
              <option value={80}>80%+</option>
              <option value={85}>85%+</option>
              <option value={90}>90%+</option>
              <option value={95}>95%+</option>
            </select>
          </div>
        </div>

        {/* Filter Actions */}
        <div className="flex justify-between items-center mt-4 pt-4 border-t border-white/10">
          <div className="text-sm text-gray-400">
            Active filters: {
              [searchTerm && 'search', selectedCategory && 'category', minPhilosophyAvg > 0 && 'score']
                .filter(Boolean).length || 'none'
            }
          </div>
          <button
            onClick={clearFilters}
            className="px-4 py-2 bg-gray-500/20 border border-gray-500/30 rounded-lg text-gray-400 hover:bg-gray-500/30 hover:border-gray-500/50 transition-colors text-sm"
          >
            🧹 Clear Filters
          </button>
        </div>
      </div>

      {/* Skills Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="flex items-center gap-3 text-gray-400">
            <div className="w-6 h-6 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
            <span>Loading skills...</span>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {skills.map(skill => (
            <SkillCard
              key={skill.skill_id}
              skill={skill}
              onExecute={handleSkillExecute}
              isExecuting={executionStates[skill.skill_id]?.isExecuting || false}
              executionResult={executionStates[skill.skill_id]?.result}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && skills.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🎭</div>
          <h3 className="text-xl font-medium text-gray-300 mb-2">No skills found</h3>
          <p className="text-gray-500 mb-4">
            {searchTerm || selectedCategory || minPhilosophyAvg > 0
              ? 'Try adjusting your filters'
              : 'Skills registry is empty'}
          </p>
          <button
            onClick={clearFilters}
            className="px-6 py-3 bg-blue-500/20 border border-blue-500/30 rounded-lg text-blue-400 hover:bg-blue-500/30 hover:border-blue-500/50 transition-colors"
          >
            🔄 Reset Filters
          </button>
        </div>
      )}

      {/* Footer Stats */}
      <div className="text-center text-sm text-gray-500 pt-6 border-t border-white/10">
        <div className="flex justify-center gap-6">
          <span>眞善美孝 - AFO Kingdom Skills Registry</span>
          <span>•</span>
          <span>Trinity Score 기반 정렬</span>
          <span>•</span>
          <span>DRY_RUN 지원</span>
        </div>
      </div>
    </div>
  );
};