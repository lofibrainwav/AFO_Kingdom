"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { SectionCard, MarkdownViewer } from "@/components/docs";
import { FileText, Download } from "lucide-react";

export default function AgentsMDPage() {
  const [content, setContent] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const response = await fetch("/api/docs/AGENTS.md");
        if (response.ok) {
          const data = await response.json();
          setContent(data.content || "");
        } else {
          // Fallback: 파일이 없으면 기본 메시지
          setContent("# AGENTS.md\n\n문서를 불러오는 중...");
        }
      } catch (error) {
        console.error("Failed to load AGENTS.md:", error);
        setContent("# AGENTS.md\n\n문서를 불러올 수 없습니다.");
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, []);

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
              <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400 mb-4 flex items-center gap-4">
                <FileText className="w-10 h-10" />
                AGENTS.md
              </h1>
              <p className="text-slate-500 text-lg">
                AFO 왕국 중앙 관제탑 - 모든 AI 코딩 에이전트 공용 지침서
              </p>
            </div>
            <a
              href="/AGENTS.md"
              download
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              다운로드
            </a>
          </div>
        </motion.header>

        {/* Content */}
        <SectionCard title="문서 내용" badge="정본">
          <MarkdownViewer content={content} loading={loading} />
        </SectionCard>
      </div>
    </div>
  );
}

