"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { SectionCard, CodeBlock } from "@/components/docs";
import { CheckCircle, XCircle, Loader2 } from "lucide-react";

interface MCPTool {
  name: string;
  description: string;
  status: "connected" | "disconnected" | "checking";
  category: "core" | "advanced";
}

const coreTools: MCPTool[] = [
  {
    name: "shell_execute",
    description: "Shell 명령어 실행 (zsh)",
    status: "checking",
    category: "core",
  },
  {
    name: "read_file",
    description: "파일 읽기",
    status: "checking",
    category: "core",
  },
  {
    name: "write_file",
    description: "파일 쓰기",
    status: "checking",
    category: "core",
  },
  {
    name: "kingdom_health",
    description: "왕국 건강 체크",
    status: "checking",
    category: "core",
  },
];

const advancedTools: MCPTool[] = [
  {
    name: "calculate_trinity_score",
    description: "眞善美孝永 5기둥 점수 계산",
    status: "checking",
    category: "advanced",
  },
  {
    name: "verify_fact",
    description: "사실 검증 (Hallucination Defense)",
    status: "checking",
    category: "advanced",
  },
  {
    name: "sequential_thinking",
    description: "단계별 논리적 추론",
    status: "checking",
    category: "advanced",
  },
  {
    name: "context7_search",
    description: "Context7 지식 베이스 검색",
    status: "checking",
    category: "advanced",
  },
];

export default function MCPToolsPage() {
  const [tools, setTools] = useState<MCPTool[]>([...coreTools, ...advancedTools]);
  const [checking, setChecking] = useState(false);

  const checkAllTools = async () => {
    setChecking(true);
    const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";

    try {
      const response = await fetch(`${API_BASE}/api/mcp/tools/status`);
      if (response.ok) {
        const data = await response.json();
        // 상태 업데이트 로직
        setTools((prev) =>
          prev.map((tool) => {
            const toolStatus = data.tools?.find((t: any) => t.name === tool.name);
            return {
              ...tool,
              status: toolStatus?.connected ? "connected" : "disconnected",
            };
          })
        );
      }
    } catch (error) {
      console.error("MCP tools check failed:", error);
    } finally {
      setChecking(false);
    }
  };

  useEffect(() => {
    checkAllTools();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "connected":
        return <CheckCircle className="w-5 h-5 text-emerald-500" />;
      case "disconnected":
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Loader2 className="w-5 h-5 text-slate-400 animate-spin" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "connected":
        return "연결됨";
      case "disconnected":
        return "연결 안 됨";
      default:
        return "확인 중...";
    }
  };

  return (
    <div className="min-h-screen bg-[#e0e5ec] p-6 md:p-10 lg:p-12">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400 mb-4">
                MCP 도구 상세 관리
              </h1>
              <p className="text-slate-500 text-lg">
                Model Context Protocol 도구 상태 및 관리
              </p>
            </div>
            <button
              onClick={checkAllTools}
              disabled={checking}
              className="px-6 py-3 bg-indigo-600 text-white rounded-lg font-bold hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {checking ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  확인 중...
                </>
              ) : (
                <>
                  <CheckCircle className="w-5 h-5" />
                  전체 연결 상태 확인
                </>
              )}
            </button>
          </div>
        </motion.header>

        {/* Core Tools */}
        <SectionCard title="Core Tools (4개)" badge="핵심">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {coreTools.map((tool, index) => (
              <motion.div
                key={tool.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 bg-white/50 backdrop-blur-sm rounded-xl border border-white/60 flex items-center justify-between hover:shadow-md transition-all"
              >
                <div className="flex-1">
                  <div className="font-mono font-bold text-slate-700 mb-1">{tool.name}</div>
                  <div className="text-sm text-slate-600">{tool.description}</div>
                </div>
                <div className="flex items-center gap-2">
                  {getStatusIcon(tool.status)}
                  <span className="text-xs text-slate-500">{getStatusText(tool.status)}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </SectionCard>

        {/* Advanced Tools */}
        <SectionCard title="Advanced Tools (10개 이상)" badge="고급">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {advancedTools.map((tool, index) => (
              <motion.div
                key={tool.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: (coreTools.length + index) * 0.1 }}
                className="p-4 bg-white/50 backdrop-blur-sm rounded-xl border border-white/60 flex items-center justify-between hover:shadow-md transition-all"
              >
                <div className="flex-1">
                  <div className="font-mono font-bold text-slate-700 mb-1">{tool.name}</div>
                  <div className="text-sm text-slate-600">{tool.description}</div>
                </div>
                <div className="flex items-center gap-2">
                  {getStatusIcon(tool.status)}
                  <span className="text-xs text-slate-500">{getStatusText(tool.status)}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </SectionCard>

        {/* Unified Server Info */}
        <SectionCard title="Unified Server: afo_ultimate_mcp_server.py" badge="정보">
          <div className="space-y-4">
            <p className="text-slate-600">
              AFO 왕국의 모든 MCP 도구를 통합한 단일 진입점 (Universal Connector & Commander)
            </p>
            <CodeBlock
              code={`위치: packages/trinity-os/trinity_os/servers/afo_ultimate_mcp_server.py

통합 모듈:
- TrinityScoreEngineHybrid
- AfoSkillsMCP
- Context7MCP
- PlaywrightBridgeMCP
- SequentialThinkingMCP
- Core Shell Tools`}
              language="text"
              filename="afo_ultimate_mcp_server.py"
            />
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

