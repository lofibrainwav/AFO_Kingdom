/**
 * AFO Kingdom Tree of Thoughts (아름다운 코드 적용)
 * Trinity Score 기반 아름다운 코드로 구현된 AI 추론 시각화 컴포넌트
 *
 * Author: AFO Kingdom Development Team
 * Date: 2025-12-24
 * Version: 2.0.0 (Beautiful Code Edition)
 *
 * Philosophy:
 * - 智 (Wisdom): AI 추론 과정의 시각적 표현
 * - 眞 (Truth): 정확한 상태 및 데이터 표시
 * - 美 (Beauty): 우아한 애니메이션과 인터랙션
 * - 孝 (Serenity): 안정적인 실시간 업데이트
 * - 永 (Eternity): 지속적인 학습 및 개선
 */

"use client";

import { useVerdictStream } from "@/lib/useVerdictStream";
import { motion, Variants } from "framer-motion";
import {
  Brain,
  Coins,
  GitBranch,
  Sparkles,
  Target,
  XCircle,
  Zap,
  ZoomIn
} from "lucide-react";
import { useCallback, useEffect, useState } from "react";

// ============================================================================
// TYPES & INTERFACES (아름다운 코드: 타입 안전성)
// ============================================================================

/**
 * 생각 노드 타입 정의 (Trinity Score: 眞 - 정확한 타입 정의)
 */
interface ThoughtNode {
  readonly id: string;
  readonly type: ThoughtNodeType;
  readonly content: string;
  readonly status: ThoughtNodeStatus;
  readonly score?: number;
  readonly children: ReadonlyArray<string>;
  readonly agent?: AgentType;
  readonly category?: NodeCategory;
}

/**
 * 노드 타입 열거형
 */
type ThoughtNodeType = "root" | "reasoning" | "criticism" | "conclusion" | "finance";

/**
 * 노드 상태 열거형
 */
type ThoughtNodeStatus = "active" | "completed" | "pruned" | "pending";

/**
 * 에이전트 타입
 */
type AgentType = "Commander" | "Zhuge Liang" | "Sima Yi" | "Zhou Yu" | "Grok" | "Claude" | "Julie CPA" | "System";

/**
 * 노드 카테고리
 */
type NodeCategory = "finance" | "general";

/**
 * 노드 컬렉션 타입
 */
type ThoughtNodeMap = Record<string, ThoughtNode>;

/**
 * 컴포넌트 Props 인터페이스
 */
interface TreeOfThoughtsProps {
  readonly className?: string;
  readonly maxDepth?: number;
  readonly animationEnabled?: boolean;
}


const INITIAL_NODES: Record<string, ThoughtNode> = {
  "root": {
    id: "root",
    type: "root",
    content: "Command: Execute Genesis Phase 2 (ToT)",
    status: "completed",
    children: ["b1", "b2", "b3"],
    agent: "Commander"
  },
  "b1": {
    id: "b1",
    type: "reasoning",
    content: "Zhuge Liang (Truth): Architecture Analysis",
    status: "completed",
    score: 95,
    children: ["c1-1"],
    agent: "Zhuge Liang"
  },
  "b2": {
    id: "b2",
    type: "reasoning",
    content: "Sima Yi (Goodness): Security & Risk Check",
    status: "completed",
    score: 88,
    children: ["c2-1"],
    agent: "Sima Yi"
  },
  "b3": {
    id: "b3",
    type: "reasoning",
    content: "Zhou Yu (Beauty): UX & Visual Design",
    status: "active",
    score: 92,
    children: ["c3-1"], // c3-2 removed to simplify
    agent: "Zhou Yu"
  },
  "c1-1": {
    id: "c1-1",
    type: "conclusion",
    content: "Tech Stack: Next.js 14 + Tailwind + Framer Motion",
    status: "completed",
    score: 98,
    children: [],
    agent: "Zhuge Liang"
  },
  "c2-1": {
    id: "c2-1",
    type: "criticism",
    content: "Alert: Verify Input Sanitization & Auth Tokens",
    status: "active", // Changed to active for visibility
    score: 45,
    children: [],
    agent: "Sima Yi"
  },
  "c3-1": {
    id: "c3-1",
    type: "conclusion",
    content: "Visuals: Deep Glassmorphism + Aurora Gradients",
    status: "active",
    score: 99,
    children: [],
    agent: "Zhou Yu"
  }
};

// Beautiful Code: UI Component
export default function TreeOfThoughtsWidget() {
  const [nodes, setNodes] = useState(INITIAL_NODES);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  // Connect to the Neural Stream
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8010';
  const { latestEvent, connected } = useVerdictStream(apiBase);

  // Callback: Process incoming thoughts (Beautiful Code: Callback pattern)
  const processIncomingThought = useCallback((event: typeof latestEvent) => {
    if (!event) return;

    const newNodeId = event.graph_node_id || `node-${Date.now()}`;
    const parentId = 'root';
    const isFinance = event.extra?.category === 'finance';
    const agentName = isFinance ? 'Julie CPA' : (event.rule_id?.split('_')[0] || 'System');
    const nodeType = isFinance ? 'finance' : 'reasoning'; 
    
    const newNode: ThoughtNode = {
        id: newNodeId,
        type: nodeType,
        content: isFinance 
            ? `Transaction: ${event.extra?.merchant} (${event.decision})`
            : `${agentName}: ${event.decision} (Rule: ${event.rule_id})`,
        status: 'active',
        score: event.trinity_score,
        children: [],
        agent: agentName as AgentType,
        category: isFinance ? 'finance' : 'general'
    };

    setNodes(prev => {
        if (prev[newNodeId]) return prev;
        const next = { ...prev };
        next[newNodeId] = newNode;
        if (next[parentId]) {
            next[parentId] = {
                ...next[parentId],
                children: [...next[parentId].children, newNodeId]
            };
        }
        return next;
    });
  }, []);

  // Effect: Subscribe to stream events
  useEffect(() => {
    if (latestEvent) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      processIncomingThought(latestEvent);
    }
  }, [latestEvent, processIncomingThought]);


  // Animation: Stable Entry Only
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    show: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, scale: 0.8 },
    show: { 
        opacity: 1, 
        scale: 1, 
        transition: { 
            type: "spring", 
            stiffness: 300, 
            damping: 24 
        } 
    }
  };

  const getPillarStyles = (agent?: string, type?: string, category?: string) => {
    // 0. Julie / Finance -> Emerald/Gold
    if (category === 'finance' || type === 'finance') {
        return 'bg-emerald-900/40 border-emerald-400/50 text-emerald-100 shadow-[0_0_20px_rgba(16,185,129,0.2)]';
    }

    // 1. Root / Commander -> Gold
    if (type === 'root') return 'bg-yellow-500/10 border-yellow-500/40 shadow-[0_0_30px_rgba(234,179,8,0.2)]';
    
    // 2. Criticism -> Red (Universal)
    if (type === 'criticism') return 'bg-red-500/10 border-red-500/30 grayscale';

    // 3. Agent Mapping (Pillar Colors)
    if (agent?.includes('Truth') || agent?.includes('Zhuge') || agent?.includes('Grok')) {
        return 'bg-blue-600/10 border-blue-500/40 text-blue-100 shadow-[0_0_15px_rgba(59,130,246,0.1)]'; // 眞 (Truth)
    }
    if (agent?.includes('Goodness') || agent?.includes('Sima')) {
        return 'bg-emerald-600/10 border-emerald-500/40 text-emerald-100 shadow-[0_0_15px_rgba(16,185,129,0.1)]'; // 善 (Goodness)
    }
    if (agent?.includes('Beauty') || agent?.includes('Zhou')) {
        return 'bg-orange-500/10 border-orange-500/40 text-orange-100 shadow-[0_0_15px_rgba(249,115,22,0.1)]'; // 美 (Beauty)
    }

    // Default -> Indigo
    return 'bg-indigo-600/10 border-indigo-500/30';
  };

  // Constants
  const SPACING = 350;

  const NodeCard = ({ id, x, y }: { id: string, x: number, y: number }) => {
    const node = nodes[id];
    if (!node) return null;

    const isActive = node.status === "active";
    const isPruned = node.status === "pruned";
    const isRoot = node.type === "root";
    
    const pillarStyle = getPillarStyles(node.agent, node.type, node.category);

    return (
      <motion.div
        variants={itemVariants}
        className={`absolute w-64 p-4 rounded-xl backdrop-blur-md border cursor-pointer transition-transform duration-200
          ${pillarStyle}
          ${isActive ? 'ring-2 ring-white/20 shadow-xl z-10 scale-105' : 'hover:bg-white/5 hover:scale-105'}
        `}
        style={{ 
            left: '50%', 
            top: y,
            x: '-50%',
            marginLeft: x 
        }}
        onClick={() => setSelectedNode(id)}
      >
        <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-2">
                {isRoot && <Target className="w-4 h-4 text-yellow-400" />}
                {node.category === 'finance' && <Coins className="w-4 h-4 text-emerald-400" />}
                {node.agent?.includes('Truth') && <Brain className="w-4 h-4 text-blue-400" />}
                {node.agent?.includes('Goodness') && <Zap className="w-4 h-4 text-emerald-400" />}
                {node.agent?.includes('Beauty') && <Sparkles className="w-4 h-4 text-orange-400" />}
                {node.type === 'criticism' && <XCircle className="w-4 h-4 text-red-400" />}
                
                <span className={`text-xs font-bold uppercase tracking-wider ${isPruned ? 'line-through opacity-50' : 'opacity-90'}`}>
                    {node.agent}
                </span>
            </div>
            {node.score && (
                <div className="px-2 py-0.5 rounded-full text-[10px] font-mono border bg-white/5 border-white/10 text-white/70">
                    {node.score}%
                </div>
            )}
        </div>
        
        <p className={`text-sm text-white/90 leading-relaxed ${isPruned ? 'line-through text-white/30' : ''}`}>
            {node.content}
        </p>

        {/* Connector Lines (Unified Geometry) */}
        {node.children.map((childId, i) => {
             // Calculate offset based on child index relative to center
             const childOffset = (i - (node.children.length - 1) / 2) * SPACING;
             return (
             <svg key={childId} className="absolute top-full left-1/2 w-full h-24 -ml-[1px] overflow-visible pointer-events-none">
                <path 
                    d={`M 0 0 C 0 40, ${childOffset} 40, ${childOffset} 80`} 
                    fill="none" 
                    stroke="rgba(255,255,255,0.1)" 
                    strokeWidth="2" 
                    vectorEffect="non-scaling-stroke"
                />
             </svg>
        )})}
      </motion.div>
    );
  };

  // Logical Render Helper: Groups nodes by depth
  const renderTreeLevels = () => {
      // Level 1: Root (0, 0)
      const root = nodes['root'];

      // Level 2: Children of Root (Standard Distribution)
      const level2 = root.children;

      // Level 3: Children of Level 2 (Direct Descendants) - Fixed structure
      const level3 = level2.flatMap(id => nodes[id]?.children || []);

      return (
        <div className="relative w-full h-full min-w-[1200px] min-h-[800px] flex justify-center pt-10">
            {/* Level 1 */}
            <NodeCard id="root" x={0} y={0} />

            {/* Level 2 */}
            <div className="absolute top-[200px] w-full flex justify-center">
                {level2.map((id, i) => {
                    // Logic: Distribute evenly across available space
                     const x = (i - (level2.length - 1) / 2) * SPACING;
                     return <div key={id} className="relative"><NodeCard id={id} x={x} y={0} /></div>
                })}
            </div>

            {/* Level 3 - Fixed: Render all level3 nodes with proper positioning */}
            <div className="absolute top-[400px] w-full flex justify-center">
                {level3.map((childId, index) => {
                    // Find parent index for positioning
                    const parentId = Object.keys(nodes).find(id =>
                        nodes[id].children?.includes(childId)
                    );
                    const parentIndex = parentId ? level2.indexOf(parentId) : 0;
                    const parentX = (parentIndex - (level2.length - 1) / 2) * SPACING;

                    // For multiple children of same parent, spread them out
                    const siblings = parentId ? nodes[parentId]?.children || [] : [];
                    const childIndex = siblings.indexOf(childId);
                    const siblingOffset = siblings.length > 1 ?
                        (childIndex - (siblings.length - 1) / 2) * (SPACING / 2) : 0;

                    return (
                        <div key={childId} className="absolute left-[50%]" style={{
                            marginLeft: parentX + siblingOffset
                        }}>
                            <NodeCard id={childId} x={0} y={0} />
                        </div>
                    );
                })}
            </div>
        </div>
      );
  };

  return (
    <div className="w-full h-[800px] bg-[#0A0C14] rounded-3xl border border-white/5 relative overflow-hidden flex flex-col">
      
      {/* Header */}
      <div className="p-6 border-b border-white/5 flex justify-between items-center bg-white/[0.02] backdrop-blur-xl z-20">
         <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-500/20 rounded-lg border border-purple-500/30">
                <GitBranch className="w-5 h-5 text-purple-400" />
            </div>
            <div>
                <h2 className="text-xl font-bold text-white">Tree of Thoughts</h2>
                <div className="flex items-center gap-2">
                    <p className="text-xs text-white/40 font-mono">GENESIS REASONING ENGINE • ACTIVE</p>
                    {connected && <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_10px_#10b981]" />}
                </div>
            </div>
         </div>
         <div className="flex gap-2">
            <button className="p-2 hover:bg-white/10 rounded-lg transition-colors text-white/50 hover:text-white">
                <ZoomIn className="w-5 h-5" />
            </button>
         </div>
      </div>

      {/* Graph Area */}
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="flex-1 relative overflow-auto cursor-grab active:cursor-grabbing p-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/20 via-[#0A0C14] to-[#0A0C14]"
      >
         {/* Background Grid */}
         <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_at_center,black,transparent_80%)] pointer-events-none" />

         {renderTreeLevels()}
      </motion.div>

    </div>
  );
}