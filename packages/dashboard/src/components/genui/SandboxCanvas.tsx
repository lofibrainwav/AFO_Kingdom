import React, { useState, useEffect } from 'react';
import { Sparkles, Terminal, AlertTriangle, Play, Save } from 'lucide-react';
import * as GenUIRegistry from './index';

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

export const SandboxCanvas: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [componentName, setComponentName] = useState('MyNewComponent');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<GenUIResponse | null>(null);
  const [RenderedComponent, setRenderedComponent] = useState<React.ComponentType | null>(null);

  const generateComponent = async () => {
    if (!prompt) return;
    setLoading(true);
    setResponse(null);
    setRenderedComponent(null);

    try {
      const res = await fetch('/api/gen-ui/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          component_name: componentName,
          trinity_threshold: 0.8
        } as GenUIRequest)
      });

      const data: GenUIResponse = await res.json();
      setResponse(data);

      if (data.status === 'approved') {
        // Dynamic load from registry
        // Note: In dev, HMR might take a second.
        // We use a small timeout or just try to load.
        setTimeout(() => {
            // @ts-ignore - Index signature
            const Comp = (GenUIRegistry as any)[data.component_name];
            if (Comp) {
                setRenderedComponent(() => Comp);
            }
        }, 1000);
      }
    } catch (e) {
      console.error(e);
      setResponse({
          component_id: 'error',
          component_name: componentName,
          code: '',
          description: 'Network Error',
          trinity_score: { total_score: 0, truth: 0, goodness: 0, beauty: 0 },
          status: 'rejected',
          error: String(e)
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full h-full flex flex-col bg-gray-900 text-white rounded-xl overflow-hidden border border-gray-700 shadow-2xl">
      {/* Header */}
      <div className="p-4 bg-gray-800 border-b border-gray-700 flex items-center justify-between">
        <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-400" />
            <span className="font-bold text-lg bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                GenUI Sandbox
            </span>
        </div>
        <div className="text-xs text-gray-400">Phase 9-1: Self-Expansion</div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel: Controls */}
        <div className="w-1/3 p-4 border-r border-gray-700 flex flex-col gap-4 overflow-y-auto">
            <div>
                <label className="block text-xs font-medium text-gray-400 mb-1">Component Name (PascalCase)</label>
                <input 
                    type="text" 
                    value={componentName}
                    onChange={(e) => setComponentName(e.target.value)}
                    className="w-full bg-gray-950 border border-gray-700 rounded p-2 text-sm focus:border-purple-500 outline-none transition-colors"
                />
            </div>
            
            <div className="flex-1 flex flex-col">
                <label className="block text-xs font-medium text-gray-400 mb-1">Commander's Intent (Prompt)</label>
                <textarea 
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Describe the UI element you want Samahwi to build..."
                    className="w-full flex-1 bg-gray-950 border border-gray-700 rounded p-2 text-sm focus:border-purple-500 outline-none transition-colors resize-none"
                />
            </div>

            <button 
                onClick={generateComponent}
                disabled={loading || !prompt}
                className={`w-full py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-all
                    ${loading ? 'bg-gray-700 cursor-not-allowed' : 'bg-purple-600 hover:bg-purple-500 shadow-lg hover:shadow-purple-500/20 active:scale-95'}
                `}
            >
                {loading ? (
                    <>
                        <Sparkles className="w-4 h-4 animate-spin" />
                        Samahwi is thinking...
                    </>
                ) : (
                    <>
                        <Play className="w-4 h-4" />
                        Generate Component
                    </>
                )}
            </button>

            {/* Trinity Score Card */}
            {response && (
                <div className={`mt-4 p-3 rounded border ${response.status === 'approved' ? 'bg-green-900/20 border-green-500/30' : 'bg-red-900/20 border-red-500/30'}`}>
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs font-bold uppercase">{response.status}</span>
                        <span className="text-xl font-bold">{response.trinity_score.total_score}</span>
                    </div>
                    {response.error && (
                        <div className="text-xs text-red-400 mt-1 flex gap-1 items-start">
                            <AlertTriangle className="w-3 h-3 shrink-0 mt-0.5" />
                            {response.error}
                        </div>
                    )}
                </div>
            )}
        </div>

        {/* Right Panel: Preview */}
        <div className="flex-1 bg-black/50 p-8 flex items-center justify-center relative overflow-hidden">
             {/* Grid Background */}
             <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

             {RenderedComponent ? (
                 <div className="relative z-10 animate-in fade-in zoom-in duration-500">
                     <div className="absolute -top-6 left-0 text-xs text-gray-500">Preview: {componentName}</div>
                     <RenderedComponent />
                 </div>
             ) : (
                 <div className="text-gray-600 flex flex-col items-center gap-2">
                     <Terminal className="w-12 h-12 opacity-20" />
                     <span className="text-sm">Waiting for code generation...</span>
                 </div>
             )}
        </div>
      </div>
    </div>
  );
};
