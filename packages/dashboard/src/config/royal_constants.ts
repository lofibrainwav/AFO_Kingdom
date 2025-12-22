import {
  Diamond,
  Shield,
  Palette,
  Heart,
  Infinity,
  Layout,
  Brain,
  Scale,
  Server,
} from "lucide-react";

export const ROYAL_CONSTANTS = {
  PROJECT_NAME: "PROJECT GENESIS",
  SUBTITLE: "Digital Royal Palace v1.0 • AFO Kingdom",
  TRINITY_SCORE_LABEL: "TRINITY SCORE",
  SECTIONS: {
    ORGANS: "11-ORGANS VITALITY",
    CHANCELLOR: "CHANCELLOR TOT",
    SKILLS: "ROYAL SKILL DECK",
    BRAIN: "BRAIN ORGAN - GRAPHRAG QUERY",
  },
  MESSAGES: {
    SKILL_HINT: "SWIPE TO EXPLORE • TAP TO SIMULATE",
  },
  LINKS: {
    API_DEFAULT: "http://localhost:8010",
  },
};

// 1. Philosophy Pillars (5 Elements)
export const ROYAL_PILLARS = [
  {
    id: "truth",
    label: "眞",
    name: "Truth",
    weight: "35%",
    role: "제갈량 (Zhuge Liang)",
    desc: "기술적 확실성",
    icon: Diamond,
    color: "text-blue-400",
    border: "border-blue-400/30",
  },
  {
    id: "goodness",
    label: "善",
    name: "Goodness",
    weight: "35%",
    role: "사마의 (Sima Yi)",
    desc: "윤리·안정성",
    icon: Shield,
    color: "text-green-400",
    border: "border-green-400/30",
  },
  {
    id: "beauty",
    label: "美",
    name: "Beauty",
    weight: "20%",
    role: "주유 (Zhou Yu)",
    desc: "단순함·우아함",
    icon: Palette,
    color: "text-purple-400",
    border: "border-purple-400/30",
  },
  {
    id: "serenity",
    label: "孝",
    name: "Serenity",
    weight: "8%",
    role: "승상 (Chancellor)",
    desc: "평온 수호",
    icon: Heart,
    color: "text-pink-400",
    border: "border-pink-400/30",
  },
  {
    id: "eternity",
    label: "永",
    name: "Eternity",
    weight: "2%",
    role: "승상 (Chancellor)",
    desc: "영속성·레거시",
    icon: Infinity,
    color: "text-amber-400",
    border: "border-amber-400/30",
  },
];

export const TRINITY_FORMULA = "Trinity Score = 0.35×眞 + 0.35×善 + 0.20×美 + 0.08×孝 + 0.02×永";
export const AUTORUN_RULE = "Trinity Score ≥ 90 AND Risk Score ≤ 10";

// 2. SSOT Personas
export const ROYAL_PERSONAS = [
  { name: "승상", code: "Chancellor", role: "Web Orchestrator (3-Strategist Coordinator)" },
  { name: "제갈량", code: "Zhuge Liang", role: "眞 35% - Architecture & Strategy" },
  { name: "사마의", code: "Sima Yi", role: "善 35% - Ethics & Risk Gate" },
  { name: "주유", code: "Zhou Yu", role: "美 20% - UX & Narrative" },
  { name: "방통", code: "Bangtong", role: "Codex - Implementation & Prototyping" },
  { name: "자룡", code: "Jaryong", role: "Claude - Logic & Refactoring" },
  { name: "육손", code: "Yukson", role: "Gemini - High-Level Strategy" },
  { name: "영덕", code: "Yeongdeok", role: "Ollama - Local Security & Archiving" },
];

// 3. Port Map
export const SERVICE_PORTS = [
  {
    service: "Soul Engine",
    port: "8010",
    desc: "FastAPI Backend Core",
    status: "LOCKED",
    color: "bg-green-100 text-green-700",
  },
  {
    service: "Dashboard",
    port: "3000",
    desc: "Next.js Frontend Palace",
    status: "LOCKED",
    color: "bg-green-100 text-green-700",
  },
  {
    service: "AICPA Julie",
    port: "3005",
    desc: "Financial Operation App",
    status: "LOCKED",
    color: "bg-green-100 text-green-700",
  },
  {
    service: "Ollama",
    port: "11435",
    desc: "Local AI (Yeongdeok)",
    status: "ACTIVE",
    color: "bg-blue-100 text-blue-700",
  },
  {
    service: "Redis",
    port: "6379",
    desc: "Memory & Caching",
    status: "SYSTEM",
    color: "bg-slate-100 text-slate-700",
  },
  {
    service: "PostgreSQL",
    port: "15432",
    desc: "Long-term Memory (Vector)",
    status: "SYSTEM",
    color: "bg-slate-100 text-slate-700",
  },
];

// 4. LOCK Principles
export const ROYAL_LOCKS = [
  {
    title: "眞 (Truth) LOCK",
    items: [
      "Strict Type Hints + MyPy",
      "Pydantic Runtime Validation",
      "Structured Logging",
      "Pytest Coverage",
    ],
    color: "border-blue-200 bg-blue-50/50",
    iconColor: "text-blue-500",
  },
  {
    title: "善 (Goodness) LOCK",
    items: [
      "DRY_RUN (Pre-check)",
      "Auth/Permission Gates",
      "Cost Optimization Fallback",
      "Graceful Degradation",
    ],
    color: "border-green-200 bg-green-50/50",
    iconColor: "text-green-500",
  },
  {
    title: "美 (Beauty) LOCK",
    items: [
      "Modular Structure",
      "Consistent Naming",
      "Elegant/Concise Code",
      "Layered Architecture",
    ],
    color: "border-purple-200 bg-purple-50/50",
    iconColor: "text-purple-500",
  },
];

// 5. Architecture Layers
export const ARCH_LAYERS = [
  {
    icon: Layout,
    title: "Presentation",
    desc: "FastAPI, Routers, Pydantic (Truth)",
    color: "bg-blue-500",
  },
  {
    icon: Brain,
    title: "Application",
    desc: "Chancellor Graph, RAG, LLM Router",
    color: "bg-indigo-500",
  },
  { icon: Scale, title: "Domain", desc: "Trinity Score, Rules, Policies", color: "bg-purple-500" },
  {
    icon: Server,
    title: "Infrastructure",
    desc: "PostgreSQL, Redis, Qdrant",
    color: "bg-slate-500",
  },
];

export const CHANCELLOR_FLOW = [
  { title: "1. Query Input", desc: "User command received via Dashboard/CLI" },
  { title: "2. Parallel Strategy", desc: "Zhuge (Arch) + Sima (Risk) + Zhou (UX) Analyze" },
  { title: "3. Tree of Thoughts", desc: "Simulate multiple execution paths" },
  { title: "4. Trinity Gate", desc: "Score ≥ 90 & Risk ≤ 10 → AUTO_RUN", highlight: true },
  { title: "5. Execution & History", desc: "Tools invoked, logs saved to PostgreSQL" },
];
