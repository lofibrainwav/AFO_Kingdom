/**
 * SandboxCanvas.tsx
 * 
 * GenUI Sandbox - Self-Expansion Phase 9-1
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useState, useMemo, useCallback } from "react";
import { Sparkles, Terminal, AlertTriangle, Play } from "lucide-react";
import * as GenUIRegistry from "./index";
import { logError } from "@/lib/logger";
import ErrorBoundary from "@/components/common/ErrorBoundary";

// Types for API
interface GenUIRequest {
  prompt: string;
  component_name: string;
  trinity_threshold: number;
}

interface GenUIResponse {
  component_id: string;
  component_name: string;
  code: string;
  description: string;
  trinity_score: {
    total_score: number;
    truth: number;
    goodness: number;
    beauty: number;
  };
  status: string;
  error?: string;
}

function SandboxCanvasContent() {
  const [prompt, setPrompt] = useState("");
  const [componentName, setComponentName] = useState("MyNewComponent");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<GenUIResponse | null>(null);
  const [RenderedComponent, setRenderedComponent] = useState<React.ComponentType | null>(null);

  // Memoize generateComponent function
  const generateComponent = useCallback(async () => {
    if (!prompt) return;
    setLoading(true);
    setResponse(null);
    setRenderedComponent(null);

    try {
      const res = await fetch("/api/gen-ui/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt,
          component_name: componentName,
          trinity_threshold: 0.8,
        } as GenUIRequest),
      });

      const data: GenUIResponse = await res.json();
      setResponse(data);

      if (data.status === "approved") {
        // Dynamic load from registry
        setTimeout(() => {
          const Comp = (GenUIRegistry as any)[data.component_name];
          if (Comp) {
            setRenderedComponent(() => Comp);
          }
        }, 1000);
      }
    } catch (err) {
      logError("GenUI component generation failed", {
        error: err instanceof Error ? err.message : "Unknown error",
      });
      setResponse({
        component_id: "error",
        component_name: componentName,
        code: "",
        description: "Network Error",
        trinity_score: { total_score: 0, truth: 0, goodness: 0, beauty: 0 },
        status: "rejected",
        error: "Component generation failed",
      });
    } finally {
      setLoading(false);
    }
  }, [prompt, componentName]);

  // Memoize input handlers
  const handlePromptChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setPrompt(e.target.value);
  }, []);

  const handleComponentNameChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setComponentName(e.target.value);
  }, []);

  // Memoize button disabled state
  const isButtonDisabled = useMemo(() => {
    return loading || !prompt.trim();
  }, [loading, prompt]);

  // Memoize button styles
  const buttonStyles = useMemo(() => {
    return isButtonDisabled
      ? "bg-gray-700 cursor-not-allowed"
      : "bg-purple-600 hover:bg-purple-500 shadow-lg hover:shadow-purple-500/20 active:scale-95";
  }, [isButtonDisabled]);

  // Memoize response card styles
  const responseCardStyles = useMemo(() => {
    if (!response) return null;
    return response.status === "approved"
      ? "bg-green-900/20 border-green-500/30"
      : "bg-red-900/20 border-red-500/30";
  }, [response]);

  return (
    <div
      className="w-full h-full flex flex-col bg-gray-900 text-white rounded-xl overflow-hidden border border-gray-700 shadow-2xl"
      role="region"
      aria-labelledby="sandbox-title"
    >
      {/* Header */}
      <header className="p-4 bg-gray-800 border-b border-gray-700 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-purple-400" aria-hidden="true" />
          <h1
            id="sandbox-title"
            className="font-bold text-lg bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent"
          >
            GenUI Sandbox
          </h1>
        </div>
        <div className="text-xs text-gray-400" aria-label="Phase information">
          Phase 9-1: Self-Expansion
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel: Controls */}
        <aside
          className="w-1/3 p-4 border-r border-gray-700 flex flex-col gap-4 overflow-y-auto"
          aria-label="Control panel"
        >
          <div>
            <label htmlFor="componentName" className="block text-xs font-medium text-gray-400 mb-1">
              Component Name (PascalCase)
            </label>
            <input
              type="text"
              id="componentName"
              value={componentName}
              onChange={handleComponentNameChange}
              aria-label="Component Name"
              className="w-full bg-gray-950 border border-gray-700 rounded p-2 text-sm focus:border-purple-500 outline-none transition-colors"
            />
          </div>

          <div className="flex-1 flex flex-col">
            <label htmlFor="prompt" className="block text-xs font-medium text-gray-400 mb-1">
              Commander's Intent (Prompt)
            </label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={handlePromptChange}
              placeholder="Describe the UI element you want Samahwi to build..."
              aria-label="Commander's Intent"
              aria-required="false"
              className="w-full flex-1 bg-gray-950 border border-gray-700 rounded p-2 text-sm focus:border-purple-500 outline-none transition-colors resize-none"
            />
          </div>

          <button
            onClick={generateComponent}
            disabled={isButtonDisabled}
            className={`w-full py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-all ${buttonStyles}`}
            aria-label={loading ? "Generating component" : "Generate component"}
            aria-disabled={isButtonDisabled}
          >
            {loading ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin" aria-hidden="true" />
                Samahwi is thinking...
              </>
            ) : (
              <>
                <Play className="w-4 h-4" aria-hidden="true" />
                Generate Component
              </>
            )}
          </button>

          {/* Trinity Score Card */}
          {response && (
            <div
              className={`mt-4 p-3 rounded border ${responseCardStyles}`}
              role="status"
              aria-live="polite"
              aria-label={`Component generation ${response.status}, Trinity score: ${response.trinity_score.total_score}`}
            >
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-bold uppercase">{response.status}</span>
                <span className="text-xl font-bold">{response.trinity_score.total_score}</span>
              </div>
              {response.error && (
                <div
                  className="text-xs text-red-400 mt-1 flex gap-1 items-start"
                  role="alert"
                  aria-live="assertive"
                >
                  <AlertTriangle className="w-3 h-3 shrink-0 mt-0.5" aria-hidden="true" />
                  {response.error}
                </div>
              )}
            </div>
          )}
        </aside>

        {/* Right Panel: Preview */}
        <main
          className="flex-1 bg-black/50 p-8 flex items-center justify-center relative overflow-hidden"
          aria-label="Component preview"
        >
          {/* Grid Background */}
          <div
            className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"
            aria-hidden="true"
          />

          {RenderedComponent ? (
            <div
              className="relative z-10 animate-in fade-in zoom-in duration-500"
              role="region"
              aria-label={`Preview of ${componentName}`}
            >
              <div className="absolute -top-6 left-0 text-xs text-gray-500" aria-hidden="true">
                Preview: {componentName}
              </div>
              <RenderedComponent />
            </div>
          ) : (
            <div
              className="text-gray-600 flex flex-col items-center gap-2"
              role="status"
              aria-live="polite"
              aria-label="Waiting for code generation"
            >
              <Terminal className="w-12 h-12 opacity-20" aria-hidden="true" />
              <span className="text-sm">Waiting for code generation...</span>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export const SandboxCanvas: React.FC = () => {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("SandboxCanvas error:", error, errorInfo);
      }}
      fallback={
        <div
          className="w-full h-full flex flex-col bg-gray-900 text-white rounded-xl overflow-hidden border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center p-8">GenUI Sandbox를 불러올 수 없습니다.</p>
        </div>
      }
    >
      <SandboxCanvasContent />
    </ErrorBoundary>
  );
};

export default SandboxCanvas;
