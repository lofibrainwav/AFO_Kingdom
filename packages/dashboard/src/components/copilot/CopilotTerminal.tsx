import React, { useEffect, useState, useRef } from 'react';
import { Terminal, Cpu, Shield, Activity } from 'lucide-react';

interface LogEntry {
  id: string;
  source: string;
  message: string;
  timestamp: string;
  type: 'info' | 'tool' | 'thought' | 'error';
}

const CopilotTerminal: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Mock Data Stream (Simulating MCP Stream)
  useEffect(() => {
    const mockLogs = [
        { source: "Brain", message: "Analyzing user request: 'Create GenUI'", type: "thought" },
        { source: "MCP", message: "Calling tool: write_to_file", type: "tool" },
        { source: "GenUI", message: "Drafting code for Project Genesis...", type: "info" },
        { source: "Trinity", message: "Truth Score: 98% | Serenity: 100%", type: "thought" },
    ];
    
    let i = 0;
    const interval = setInterval(() => {
        if (i < mockLogs.length) {
            const log = mockLogs[i];
            setLogs(prev => [...prev, {
                id: Date.now().toString(),
                source: log.source,
                message: log.message,
                timestamp: new Date().toLocaleTimeString(),
                type: log.type as any
            }]);
            i++;
        }
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="bg-black/90 border border-green-500/30 rounded-xl overflow-hidden shadow-[0_0_20px_rgba(34,197,94,0.1)] font-mono text-sm h-full flex flex-col">
      {/* Header */}
      <div className="bg-gray-900/50 p-3 border-b border-green-500/20 flex justify-between items-center">
        <div className="flex items-center gap-2 text-green-400">
            <Terminal className="w-4 h-4" />
            <span className="font-bold tracking-wider">AFO.COPILOT_TERMINAL</span>
        </div>
        <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-xs text-blue-400">
                <Cpu className="w-3 h-3" /> 12%
            </div>
             <div className="flex items-center gap-1.5 text-xs text-purple-400">
                <Shield className="w-3 h-3" /> ACTIVE
            </div>
            <div className="flex items-center gap-1.5 text-xs text-green-400">
                <Activity className="w-3 h-3" /> LIVE
            </div>
        </div>
      </div>

      {/* Log Body */}
      <div ref={scrollRef} className="flex-1 p-4 overflow-y-auto space-y-2 custom-scrollbar">
        {logs.length === 0 && (
            <div className="text-gray-600 italic">Initializing Neural Link...</div>
        )}
        {logs.map((log) => (
            <div key={log.id} className="flex gap-3 hover:bg-white/5 p-1 rounded transition-colors group">
                <span className="text-gray-600 text-xs whitespace-nowrap pt-0.5">{log.timestamp}</span>
                <div className="flex-1 break-all">
                    <span className={`font-bold mr-2 ${
                        log.source === 'Brain' ? 'text-blue-400' :
                        log.source === 'MCP' ? 'text-yellow-400' :
                        log.source === 'GenUI' ? 'text-pink-400' :
                        'text-green-400'
                    }`}>[{log.source}]</span>
                    <span className={`
                         ${log.type === 'thought' ? 'text-gray-400 italic' : 
                           log.type === 'tool' ? 'text-yellow-200' : 
                           log.type === 'error' ? 'text-red-400' : 'text-gray-300'}
                    `}>{log.message}</span>
                </div>
            </div>
        ))}
         <div className="animate-pulse text-green-500 font-bold">_</div>
      </div>
    </div>
  );
};

export default CopilotTerminal;
