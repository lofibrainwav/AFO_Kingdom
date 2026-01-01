import React from 'react';
import { readFileSync } from 'fs';
import { join } from 'path';

interface MLXBenchResult {
  ts: string;
  model: string;
  prompt_chars: number;
  gen_tokens: number;
  seconds: number;
  tokens_per_sec: number;
  metal_available: boolean;
  active_memory_bytes: number;
  peak_memory_bytes: number;
}

export function MLXPerformanceCard() {
  // Read latest benchmark result from JSONL file
  // Note: In production, this would be an API call, but for demo we read directly
  let latestBench: MLXBenchResult | null = null;
  try {
    const benchFile = join(process.cwd(), '../../../tools/mlx_optimization/artifacts/mlx_bench_20251231.jsonl');
    const content = readFileSync(benchFile, 'utf-8');
    const lines = content.trim().split('\n');
    if (lines.length > 0) {
      latestBench = JSON.parse(lines[lines.length - 1]);
    }
  } catch (error) {
    console.warn('Could not read MLX benchmark file:', error);
  }

  if (!latestBench) {
    return (
      <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">MLX Apple Silicon Performance</h3>
        <p className="text-gray-400">Benchmark data not available</p>
      </div>
    );
  }

  const formatBytes = (bytes: number) => {
    const gb = bytes / (1024 ** 3);
    return `${gb.toFixed(1)} GB`;
  };

  return (
    <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-white mb-4">MLX Apple Silicon Performance</h3>

      <div className="grid grid-cols-2 gap-4">
        {/* Primary Metrics */}
        <div className="space-y-3">
          <div>
            <div className="text-2xl font-bold text-green-400">
              {latestBench.tokens_per_sec.toFixed(0)}
            </div>
            <div className="text-sm text-gray-400">tokens/sec</div>
          </div>

          <div>
            <div className="text-lg font-semibold text-blue-400">
              {formatBytes(latestBench.peak_memory_bytes)}
            </div>
            <div className="text-sm text-gray-400">Peak Memory</div>
          </div>
        </div>

        {/* Secondary Metrics */}
        <div className="space-y-3">
          <div>
            <div className="text-lg font-semibold text-purple-400">
              {latestBench.metal_available ? '✅ Active' : '❌ N/A'}
            </div>
            <div className="text-sm text-gray-400">Metal GPU</div>
          </div>

          <div>
            <div className="text-sm text-gray-400">
              {latestBench.model}
            </div>
            <div className="text-xs text-gray-500">
              {new Date(latestBench.ts).toLocaleString()}
            </div>
          </div>
        </div>
      </div>

      {/* Performance Summary */}
      <div className="mt-4 pt-4 border-t border-white/10">
        <div className="text-sm text-gray-400">
          Generated {latestBench.gen_tokens} tokens in {latestBench.seconds.toFixed(3)}s
          from {latestBench.prompt_chars} chars prompt
        </div>
      </div>
    </div>
  );
}
