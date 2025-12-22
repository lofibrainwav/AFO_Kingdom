"use client";

import { useCallback, useEffect, useState } from "react";
import { TrinityGlowCard } from "./TrinityGlowCard";
import { useSpatialAudio } from "../hooks/useSpatialAudio";

interface SerenityProgress {
  status: "idle" | "generating" | "capturing" | "evaluating" | "complete" | "failed";
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
  apiEndpoint = "/api/serenity/create",
  onComplete,
}: SerenityMonitorProps) {
  const [prompt, setPrompt] = useState("");
  const [progress, setProgress] = useState<SerenityProgress>({
    status: "idle",
    iteration: 0,
    maxIterations: 3,
    trinityScore: 0.85,
    riskScore: 0.15,
    feedback: "",
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
      setProgress((p) => ({ ...p, status: "generating", iteration: 1 }));

      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const result = await response.json();

      setProgress({
        status: result.success ? "complete" : "failed",
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
      setProgress((p) => ({
        ...p,
        status: "failed",
        feedback: `Error: ${error}`,
      }));
    } finally {
      setIsCreating(false);
    }
  }, [prompt, apiEndpoint, initAudio, onComplete]);

  const getStatusIcon = () => {
    switch (progress.status) {
      case "idle":
        return "💭";
      case "generating":
        return "🎨";
      case "capturing":
        return "📸";
      case "evaluating":
        return "⚖️";
      case "complete":
        return "✅";
      case "failed":
        return "❌";
    }
  };

  const getStatusText = () => {
    switch (progress.status) {
      case "idle":
        return "Ready to create";
      case "generating":
        return "GenUI creating code...";
      case "capturing":
        return "Capturing screenshot...";
      case "evaluating":
        return "Chancellor evaluating...";
      case "complete":
        return "Creation complete!";
      case "failed":
        return "Creation failed";
    }
  };

  return (
    <div className="max-w-[600px] mx-auto p-8">
      <h1 className="text-2xl font-bold text-white mb-4 text-center">🌟 Project Serenity</h1>

      {/* Input */}
      <div className="mb-6">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe the UI you want to create..."
          disabled={isCreating}
          className="w-full p-4 rounded-lg bg-white/10 border border-white/20 text-white text-base min-h-[80px] resize-y focus:outline-none focus:border-green-500/50"
        />
        <button
          onClick={startCreation}
          disabled={isCreating || !prompt.trim()}
          className={`w-full py-3 mt-2 rounded-lg text-white font-bold border-none transition-colors ${
            isCreating
              ? "bg-gray-600 cursor-wait"
              : "bg-green-500 hover:bg-green-600 cursor-pointer"
          }`}
        >
          {isCreating ? "🔄 Creating..." : "✨ Create UI"}
        </button>
      </div>

      {/* Progress Display */}
      <TrinityGlowCard trinityScore={progress.trinityScore} riskScore={progress.riskScore}>
        <div className="text-center">
          <div className="text-3xl mb-2">{getStatusIcon()}</div>
          <div className="text-white font-semibold">{getStatusText()}</div>
          {progress.iteration > 0 && (
            <div className="text-gray-400 text-sm mt-1">
              Iteration {progress.iteration}/{progress.maxIterations}
            </div>
          )}
        </div>

        {/* Feedback */}
        {progress.feedback && (
          <div className="mt-4 p-3 bg-white/10 rounded-lg text-gray-300 text-sm">
            💬 {progress.feedback}
          </div>
        )}
      </TrinityGlowCard>

      {/* Screenshot Preview */}
      {progress.screenshotUrl && (
        <div className="mt-6">
          <h3 className="text-white mb-2">📸 Preview</h3>
          <img
            src={progress.screenshotUrl}
            alt="Generated UI"
            className="w-full rounded-lg border border-white/20"
          />
        </div>
      )}
    </div>
  );
}

export default SerenityMonitor;
