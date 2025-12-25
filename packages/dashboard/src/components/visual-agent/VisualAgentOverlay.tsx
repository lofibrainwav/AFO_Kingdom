"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Play, SkipForward } from "lucide-react";
import { useState } from "react";

// Janus Protocol Types (Frontend Mirror)
interface BBox {
  x: number;
  y: number;
  w: number;
  h: number;
}

interface VisualAction {
  type: string;
  bbox?: BBox;
  text?: string;
  confidence: number;
  why: string;
  safety: "safe" | "confirm" | "block";
}

interface VisualPlan {
  goal: string;
  actions: VisualAction[];
  stop: boolean;
  summary: string;
}

export function VisualAgentOverlay() {
  const [goal, setGoal] = useState("");
  const [currentPlan, setCurrentPlan] = useState<VisualPlan | null>(null);
  const [activeStep, setActiveStep] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Mock Analysis (Simulating Backend Response)
  const handleAnalyze = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      setCurrentPlan({
        goal: goal || "No goal set",
        summary: "Identified navigation elements. Proceeding to click 'Login'.",
        stop: false,
        actions: [
          {
            type: "click",
            bbox: { x: 0.8, y: 0.05, w: 0.1, h: 0.05 },
            confidence: 0.95,
            why: "Detected 'Login' button in top right",
            safety: "safe",
          },
          {
            type: "type",
            text: "user@example.com",
            confidence: 0.88,
            why: "Input for username field",
            safety: "safe",
          }
        ],
      });
      setIsAnalyzing(false);
      setActiveStep(0);
    }, 1500);
  };

  const currentAction = currentPlan?.actions[activeStep];

  const getSafetyColor = (safety: string) => {
    switch (safety) {
      case "safe": return "bg-green-500/20 border-green-500 text-green-400";
      case "confirm": return "bg-yellow-500/20 border-yellow-500 text-yellow-400";
      case "block": return "bg-red-500/20 border-red-500 text-red-400";
      default: return "bg-gray-500/20 border-gray-500 text-gray-400";
    }
  };

  if (!currentPlan && !isAnalyzing) {
    return (
      <Card className="fixed bottom-4 right-4 w-96 p-4 bg-black/90 border-purple-500/50 backdrop-blur-md z-[9999]">
        <h3 className="text-purple-400 font-bold mb-2 flex items-center gap-2">
          <span className="text-xl">👁️</span> Janus Agent
        </h3>
        <div className="flex gap-2">
          <input
            className="flex-1 bg-slate-900 border border-slate-700 rounded px-3 py-1 text-sm text-white"
            placeholder="What should I do?"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
          />
          <Button size="sm" onClick={handleAnalyze} className="bg-purple-600 hover:bg-purple-700">
            Analyze
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <div className="fixed inset-0 pointer-events-none z-[9999]">
      {/* 1. BBox Overlay */}
      {currentAction?.bbox && (
        <div
          className={`absolute border-4 transition-all duration-300 ${getSafetyColor(currentAction.safety)}`}
          style={{
            left: `${currentAction.bbox.x * 100}%`,
            top: `${currentAction.bbox.y * 100}%`,
            width: `${currentAction.bbox.w * 100}%`,
            height: `${currentAction.bbox.h * 100}%`,
          }}
        >
          <div className="absolute -top-8 left-0 text-xs font-bold bg-black/80 px-2 py-1 rounded text-white whitespace-nowrap">
            {currentAction.type.toUpperCase()} ({(currentAction.confidence * 100).toFixed(0)}%)
          </div>
        </div>
      )}

      {/* 2. Control Panel */}
      <Card className="fixed bottom-4 right-4 w-96 p-4 bg-black/90 border-purple-500/50 backdrop-blur-md pointer-events-auto">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-purple-400 font-bold flex items-center gap-2">
              <span className="text-xl">👁️</span> Janus Agent
            </h3>
            <p className="text-xs text-gray-400 line-clamp-1">{currentPlan?.summary}</p>
          </div>
          <Badge variant="outline" className={getSafetyColor(currentAction?.safety || "safe")}>
            {currentAction?.safety.toUpperCase()}
          </Badge>
        </div>

        {/* Action List */}
        <div className="space-y-2 mb-4 max-h-40 overflow-y-auto">
          {currentPlan?.actions.map((action, i) => (
            <div
              key={i}
              className={`p-2 rounded border text-xs ${
                i === activeStep
                  ? "bg-purple-900/40 border-purple-500"
                  : "bg-black/40 border-white/10 opacity-50"
              }`}
            >
              <div className="flex justify-between font-bold mb-1">
                <span>{i + 1}. {action.type}</span>
                <span>{(action.confidence * 100).toFixed(0)}%</span>
              </div>
              <p className="text-gray-400">{action.why}</p>
            </div>
          ))}
        </div>

        {/* Progress & Controls */}
        <Progress value={((activeStep + 1) / (currentPlan?.actions.length || 1)) * 100} className="h-1 mb-4" />
        
        <div className="flex justify-between gap-2">
          <Button
            variant="outline" size="sm"
            className="flex-1 border-white/20 hover:bg-white/10"
            onClick={() => setCurrentPlan(null)}
          >
           Clear
          </Button>
          <Button size="sm" className="bg-emerald-600 hover:bg-emerald-700 flex-1 gap-1">
            <Play className="w-3 h-3" /> Step
          </Button>
          <Button size="sm" className="bg-purple-600 hover:bg-purple-700 flex-1 gap-1">
            <SkipForward className="w-3 h-3" /> Run
          </Button>
        </div>
      </Card>
      
      {/* Loading Overlay */}
      {isAnalyzing && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center pointer-events-auto">
            <div className="text-center animate-pulse">
                <span className="text-6xl">👁️</span>
                <p className="text-purple-400 mt-4 font-mono">Janus Thinking...</p>
            </div>
        </div>
      )}
    </div>
  );
}