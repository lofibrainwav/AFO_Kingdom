"use client";

import React, { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { GitBranch, Play, Save, Plus, Trash2, Settings } from "lucide-react";

// Node Types
interface WorkflowNode {
  id: string;
  type: "start" | "llm" | "tool" | "condition" | "end";
  label: string;
  x: number;
  y: number;
  config?: Record<string, any>;
}

interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
}

interface WorkflowState {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
}

const NODE_TEMPLATES: Omit<WorkflowNode, "id" | "x" | "y">[] = [
  { type: "start", label: "Start" },
  { type: "llm", label: "LLM Call", config: { model: "gpt-4" } },
  { type: "tool", label: "Tool", config: { tool_name: "" } },
  { type: "condition", label: "Condition", config: { condition: "" } },
  { type: "end", label: "End" },
];

const NODE_COLORS: Record<string, string> = {
  start: "from-green-500 to-emerald-600",
  llm: "from-purple-500 to-violet-600",
  tool: "from-blue-500 to-cyan-600",
  condition: "from-yellow-500 to-amber-600",
  end: "from-red-500 to-rose-600",
};

export const WorkflowDesigner: React.FC = () => {
  const [workflow, setWorkflow] = useState<WorkflowState>({
    nodes: [
      { id: "1", type: "start", label: "Start", x: 100, y: 200 },
      { id: "2", type: "llm", label: "Process Query", x: 300, y: 200 },
      { id: "3", type: "end", label: "End", x: 500, y: 200 },
    ],
    edges: [
      { id: "e1-2", source: "1", target: "2" },
      { id: "e2-3", source: "2", target: "3" },
    ],
  });

  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [draggingNode, setDraggingNode] = useState<string | null>(null);

  const addNode = useCallback(
    (template: Omit<WorkflowNode, "id" | "x" | "y">) => {
      const newNode: WorkflowNode = {
        ...template,
        id: `node-${Date.now()}`,
        x: 250 + Math.random() * 100,
        y: 150 + Math.random() * 100,
      };
      setWorkflow((prev) => ({
        ...prev,
        nodes: [...prev.nodes, newNode],
      }));
    },
    []
  );

  const deleteNode = useCallback((nodeId: string) => {
    setWorkflow((prev) => ({
      nodes: prev.nodes.filter((n) => n.id !== nodeId),
      edges: prev.edges.filter(
        (e) => e.source !== nodeId && e.target !== nodeId
      ),
    }));
    setSelectedNode(null);
  }, []);

  const handleNodeDrag = useCallback(
    (nodeId: string, e: React.MouseEvent) => {
      if (!draggingNode) return;
      const canvas = e.currentTarget.getBoundingClientRect();
      const x = e.clientX - canvas.left - 60;
      const y = e.clientY - canvas.top - 20;

      setWorkflow((prev) => ({
        ...prev,
        nodes: prev.nodes.map((n) => (n.id === nodeId ? { ...n, x, y } : n)),
      }));
    },
    [draggingNode]
  );

  const saveWorkflow = async () => {
    try {
      const res = await fetch("/api/proxy/workflow/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ workflow }),
      });
      if (res.ok) {
        console.log("Workflow saved!");
      }
    } catch (err) {
      console.error("Save failed:", err);
    }
  };

  return (
    <div className="w-full h-[600px] bg-black/40 backdrop-blur-xl rounded-3xl border border-white/10 overflow-hidden flex">
      {/* Sidebar - Node Palette */}
      <div className="w-48 bg-black/30 border-r border-white/10 p-4 flex flex-col gap-4">
        <div className="flex items-center gap-2 text-white/80 font-semibold mb-2">
          <GitBranch className="w-5 h-5" />
          Workflow Designer
        </div>

        <div className="text-xs text-white/50 uppercase tracking-wider">
          Add Nodes
        </div>

        {NODE_TEMPLATES.map((template) => (
          <motion.button
            key={template.type}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => addNode(template)}
            className={`p-3 rounded-xl bg-gradient-to-r ${
              NODE_COLORS[template.type]
            } text-white text-sm font-medium flex items-center gap-2 shadow-lg`}
          >
            <Plus className="w-4 h-4" />
            {template.label}
          </motion.button>
        ))}

        <div className="mt-auto flex flex-col gap-2">
          <button
            onClick={saveWorkflow}
            className="p-2 rounded-lg bg-green-500/20 text-green-400 hover:bg-green-500/30 flex items-center justify-center gap-2 text-sm"
          >
            <Save className="w-4 h-4" /> Save
          </button>
          <button className="p-2 rounded-lg bg-purple-500/20 text-purple-400 hover:bg-purple-500/30 flex items-center justify-center gap-2 text-sm">
            <Play className="w-4 h-4" /> Execute
          </button>
        </div>
      </div>

      {/* Canvas */}
      <div
        className="flex-1 relative"
        onMouseMove={(e) => draggingNode && handleNodeDrag(draggingNode, e)}
        onMouseUp={() => setDraggingNode(null)}
        onMouseLeave={() => setDraggingNode(null)}
      >
        {/* Edges (SVG) */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none">
          {workflow.edges.map((edge) => {
            const source = workflow.nodes.find((n) => n.id === edge.source);
            const target = workflow.nodes.find((n) => n.id === edge.target);
            if (!source || !target) return null;

            const x1 = source.x + 60;
            const y1 = source.y + 20;
            const x2 = target.x;
            const y2 = target.y + 20;

            return (
              <g key={edge.id}>
                <path
                  d={`M${x1},${y1} C${x1 + 50},${y1} ${x2 - 50},${y2} ${x2},${y2}`}
                  stroke="rgba(168, 85, 247, 0.5)"
                  strokeWidth="2"
                  fill="none"
                />
                <circle cx={x2} cy={y2} r="4" fill="rgb(168, 85, 247)" />
              </g>
            );
          })}
        </svg>

        {/* Nodes */}
        {workflow.nodes.map((node) => (
          <motion.div
            key={node.id}
            style={{ left: node.x, top: node.y }}
            className={`absolute cursor-move select-none`}
            onMouseDown={() => setDraggingNode(node.id)}
            onClick={() => setSelectedNode(node.id)}
          >
            <div
              className={`px-4 py-2 rounded-xl bg-gradient-to-r ${
                NODE_COLORS[node.type]
              } text-white text-sm font-medium shadow-lg border-2 ${
                selectedNode === node.id
                  ? "border-white"
                  : "border-transparent"
              } flex items-center gap-2 min-w-[120px]`}
            >
              {node.label}
              {selectedNode === node.id && node.type !== "start" && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteNode(node.id);
                  }}
                  className="ml-auto p-1 rounded-full bg-black/30 hover:bg-black/50"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              )}
            </div>
          </motion.div>
        ))}

        {/* Empty State */}
        {workflow.nodes.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center text-white/30 text-sm">
            Drag nodes from the sidebar to build your workflow
          </div>
        )}
      </div>

      {/* Node Config Panel */}
      {selectedNode && (
        <div className="w-64 bg-black/30 border-l border-white/10 p-4">
          <div className="flex items-center gap-2 text-white/80 font-semibold mb-4">
            <Settings className="w-4 h-4" />
            Node Config
          </div>
          <div className="text-sm text-white/60">
            Node: {workflow.nodes.find((n) => n.id === selectedNode)?.label}
          </div>
        </div>
      )}
    </div>
  );
};

export default WorkflowDesigner;
