"use client";

import { Code2, Paintbrush, RefreshCw, Sparkles, Zap } from "lucide-react";
import { useState } from "react";

interface SerenityResponse {
  code: string;
  screenshot_path: string | null;
  trinity_score: number;
  success: boolean;
  feedback: string;
}

export default function SerenityCanvas() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SerenityResponse | null>(null);
  const [activeTab, setActiveTab] = useState<"preview" | "code">("preview");

  const handleGenerate = async () => {
    if (!prompt) return;
    setLoading(true);
    setResult(null);

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";
      const res = await fetch(`${apiBase}/api/serenity/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error("GenUI Failed:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full h-full min-h-screen bg-[#0A0C14] text-white p-8 flex flex-col gap-8 relative overflow-hidden">
      {/* Ambient Background */}
      <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_50%_0%,rgba(56,189,248,0.1),transparent_50%)] pointer-events-none" />

      {/* Header */}
      <div className="relative z-10 flex items-center justify-between">
        <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-sky-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent flex items-center gap-3">
                <Paintbrush className="w-8 h-8 text-sky-400" />
                Project Serenity
            </h1>
            <p className="text-white/40 font-mono mt-1 tracking-wider uppercase text-xs">Autonomous GenUI Engine • Phase 9</p>
        </div>
      </div>

      {/* Input Area */}
      <div className="relative z-10 w-full max-w-3xl mx-auto">
        <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-sky-500 to-purple-500 rounded-2xl opacity-20 group-hover:opacity-40 blur transition duration-500" />
            <div className="relative flex gap-2 bg-black/80 backdrop-blur-xl p-2 rounded-2xl border border-white/10">
                <input 
                    type="text" 
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Describe the UI component you want to create (e.g., 'A futuristic treasury widget with gold accents')"
                    className="flex-1 bg-transparent border-none outline-none text-white px-4 placeholder:text-white/20 font-light"
                    onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                />
                <button 
                    onClick={handleGenerate}
                    disabled={loading || !prompt}
                    className="bg-white/10 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2"
                >
                    {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                    {loading ? "Dreaming..." : "Generate"}
                </button>
            </div>
        </div>
      </div>

      {/* Main Canvas */}
      <div className="flex-1 relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-8 min-h-[500px]">
        
        {/* Left: Component Preview (Placeholder for Sandbox) */}
        <div className="bg-black/40 border border-white/10 rounded-3xl overflow-hidden relative group">
            <div className="absolute top-4 left-4 flex gap-2 z-20">
                <div className="px-3 py-1 rounded-full bg-black/50 border border-white/10 text-xs font-mono text-white/50 backdrop-blur-md">
                    Canvas Preview
                </div>
            </div>
            
            <div className="w-full h-full flex items-center justify-center bg-[url('/grid.svg')] bg-center p-8">
                {result ? (
                    <div className="text-center space-y-4">
                         <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-sky-500 flex items-center justify-center mx-auto shadow-[0_0_30px_rgba(16,185,129,0.3)]">
                            <Zap className="w-8 h-8 text-white" />
                         </div>
                         <h3 className="text-xl font-bold text-white">Generation Successful</h3>
                         <p className="text-white/50 max-w-sm mx-auto">
                            Trinity Score: <span className="text-emerald-400 font-mono">{result.trinity_score}%</span>
                         </p>
                         <p className="text-xs text-white/30 font-mono max-w-md mx-auto border border-white/5 p-4 rounded-lg bg-black/50">
                            {result.feedback}
                         </p>
                         {/* Would normally render component here via Sandbox/Iframe */}
                    </div>
                ) : (
                    <div className="text-center text-white/20">
                        <Paintbrush className="w-12 h-12 mx-auto mb-4 opacity-50" />
                        <p>Waiting for inspiration...</p>
                    </div>
                )}
            </div>
        </div>

        {/* Right: Code/Trinity Analysis */}
        <div className="flex flex-col gap-4">
             {/* Tabs */}
             <div className="flex gap-2">
                <button 
                    onClick={() => setActiveTab("code")}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'code' ? 'bg-white/10 text-white' : 'text-white/40 hover:text-white'}`}
                >
                    <Code2 className="w-4 h-4 inline mr-2" />
                    Generated Code
                </button>
                <button 
                    onClick={() => setActiveTab("preview")}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'preview' ? 'bg-white/10 text-white' : 'text-white/40 hover:text-white'}`}
                >
                    <Zap className="w-4 h-4 inline mr-2" />
                    Trinity Analysis
                </button>
             </div>

             <div className="flex-1 bg-[#1e1e1e] rounded-3xl border border-white/10 overflow-hidden relative">
                {result?.code && activeTab === 'code' ? (
                     <pre className="p-6 text-xs font-mono text-gray-300 overflow-auto h-full scrollbar-thin scrollbar-thumb-white/10">
                        {result.code}
                     </pre>
                ) : (
                    <div className="w-full h-full flex items-center justify-center text-white/20 text-sm font-mono">
                        Code will appear here
                    </div>
                )}
             </div>
        </div>

      </div>

    </div>
  );
}
