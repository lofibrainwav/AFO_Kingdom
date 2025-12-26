"use client";

import { useState } from "react";

interface GenUIProps {
  className?: string;
}

export default function GenUICreator({ className = "" }: GenUIProps) {
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setIsGenerating(true);
    setResult(null);

    try {
      // Placeholder for now - will implement in PR#2
      // This is template-only system, no code execution
      setTimeout(() => {
        setResult(`Template Preview: ${prompt}`);
        setIsGenerating(false);
      }, 1000);
    } catch (error) {
      console.error("Generation failed:", error);
      setResult("Error: Generation failed");
      setIsGenerating(false);
    }
  };

  return (
    <div className={`bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 p-6 ${className}`}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <h3 className="text-xl font-bold text-slate-600">🎨 GenUI Creator</h3>
          <div className="h-[1px] flex-1 bg-slate-300" />
        </div>

        {/* Description */}
        <div className="text-sm text-slate-500">
          Generate UI components from natural language descriptions. Template-based system with no code execution.
        </div>

        {/* Input Section */}
        <div className="space-y-4">
          <label htmlFor="genui-prompt" className="block text-sm font-medium text-slate-600">
            Describe your UI component:
          </label>
          <textarea
            id="genui-prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., Create a card component with title, description, and action button"
            className="w-full h-32 px-4 py-3 bg-white/50 border border-slate-300 rounded-xl text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
            disabled={isGenerating}
          />
          <button
            onClick={handleGenerate}
            disabled={!prompt.trim() || isGenerating}
            className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            {isGenerating ? "Generating..." : "Generate UI"}
          </button>
        </div>

        {/* Result Section */}
        {result && (
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-slate-600">Generated Result:</h4>
            <div className="bg-white/30 border border-slate-200 rounded-xl p-4">
              <pre className="text-sm text-slate-700 whitespace-pre-wrap font-mono">
                {result}
              </pre>
            </div>
          </div>
        )}

        {/* Safety Notice */}
        <div className="text-xs text-slate-400 bg-yellow-50/50 border border-yellow-200 rounded-lg p-3">
          <strong>🔒 Safety:</strong> This system only generates templates from a predefined whitelist.
          No arbitrary code execution or external API calls are performed.
        </div>
      </div>
    </div>
  );
}