"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Brain, Share2, Sparkles, Network } from "lucide-react";

interface GraphContext {
  source: string;
  relationship: string;
  target: string;
  description: string;
}

interface RAGResponse {
  answer: string;
  sources: any[];
  graph_context: GraphContext[];
  processing_log: string[];
}

export const GraphRAGQuery: React.FC = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RAGResponse | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);
    setLogs([]);

    try {
      // Simulate/Real Log Streaming
      setLogs(["🧠 Connecting to Brain Organ..."]);

      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, use_hyde: true, use_graph: true }),
      });

      if (!res.ok) throw new Error("Failed to query kingdom");

      const data = await res.json();
      setResult(data);
      if (data.processing_log) setLogs(data.processing_log);
    } catch (err) {
      console.error(err);
      setLogs((prev) => [...prev, "❌ Error connecting to neural network"]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 text-white font-sans">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="backdrop-blur-xl bg-black/40 border border-white/10 rounded-3xl p-8 shadow-2xl relative overflow-hidden"
      >
        {/* Glow Effect */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-purple-500/20 rounded-full blur-[100px] -z-10" />

        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="p-3 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl shadow-lg shadow-purple-500/20">
            <Brain className="w-8 h-8 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">
              Ask the Kingdom
            </h2>
            <p className="text-sm text-white/50">GraphRAG v4.0 • Qdrant + Neo4j Optimized</p>
          </div>
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="relative mb-8 group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything (e.g., Who is the Chancellor?)"
            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-14 pr-4 text-lg text-white placeholder-white/30 focus:outline-none focus:border-purple-500/50 focus:bg-white/10 transition-all shadow-inner"
          />
          <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-white/40 group-focus-within:text-purple-400 transition-colors w-6 h-6" />
          <motion.div
            className="absolute inset-0 rounded-2xl ring-1 ring-inset ring-transparent group-focus-within:ring-purple-500/30 pointer-events-none"
            layoutId="search-glow"
          />
        </form>

        {/* Loading / Logs */}
        <AnimatePresence>
          {(loading || logs.length > 0) && !result && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="mb-8 space-y-2 overflow-hidden"
            >
              {logs.map((log, i) => (
                <motion.div
                  key={i}
                  initial={{ x: -10, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: i * 0.1 }}
                  style={{ caretColor: "transparent" }}
                  className="flex items-center gap-2 text-sm text-green-400/80 font-mono"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-green-500/50" />
                  {log}
                </motion.div>
              ))}
              {loading && (
                <div className="flex items-center gap-2 text-purple-300/50 text-xs animate-pulse mt-2">
                  <Sparkles className="w-3 h-3" /> Processing Neural Pathways...
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* Main Answer */}
              <div className="p-6 bg-white/5 rounded-2xl border border-white/10">
                <div className="flex items-center gap-2 mb-4 text-purple-300 text-sm font-medium uppercase tracking-wider">
                  <Sparkles className="w-4 h-4" /> Comprehensive Answer
                </div>
                <div className="prose prose-invert max-w-none text-white/90 leading-relaxed whitespace-pre-wrap">
                  {result.answer}
                </div>
              </div>

              {/* Graph Context Cards */}
              {result.graph_context && result.graph_context.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-4 text-blue-300 text-sm font-medium uppercase tracking-wider">
                    <Share2 className="w-4 h-4" /> Graph Connections (Neo4j)
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {result.graph_context.map((ctx, idx) => (
                      <motion.div
                        key={idx}
                        whileHover={{ scale: 1.02, backgroundColor: "rgba(255,255,255,0.08)" }}
                        className="p-4 bg-white/5 rounded-xl border border-white/5 flex flex-col gap-2 transition-colors cursor-default"
                      >
                        <div className="flex items-center justify-between text-xs text-white/40">
                          <span>Connection #{idx + 1}</span>
                          <Network className="w-3 h-3" />
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <span className="font-bold text-blue-200">{ctx.source}</span>
                          <span className="px-2 py-0.5 rounded-full bg-white/10 text-xs text-white/60">
                            {ctx.relationship}
                          </span>
                          <span className="font-bold text-purple-200">{ctx.target}</span>
                        </div>
                        {ctx.description && (
                          <p className="text-xs text-white/50 italic mt-1">"{ctx.description}"</p>
                        )}
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {/* Zero State for Graph */}
              {(!result.graph_context || result.graph_context.length === 0) && (
                <div className="p-4 rounded-xl border border-dashed border-white/10 text-center text-white/30 text-sm">
                  No direct graph connections found for this query context.
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
};
