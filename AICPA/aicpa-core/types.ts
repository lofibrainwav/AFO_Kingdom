import React from 'react';

// --- GLOBAL WINDOW TYPE EXTENSION ---
declare global {
  interface AIStudio {
    hasSelectedApiKey: () => Promise<boolean>;
    openSelectKey: () => Promise<void>;
  }

  interface Window {
    aistudio?: AIStudio;
  }
}

export interface RcateData {
  role: string;
  context: string;
  audience: string;
  task: string;
  execution: string;
}

export interface TemplateVariable {
  key: string;
  label: string;
  value: string;
  type: 'currency' | 'percent' | 'date' | 'text';
}

export interface Template {
  id: string;
  category: string; // Changed from enum to string to support user custom categories
  name: string;
  badge?: string; // e.g., "Big 4 Style", "LA Local"
  data: RcateData;
  variables: TemplateVariable[]; // Smart variables for easy editing
  description?: string;
  isUserCreated?: boolean; // Flag to identify user templates
}

export enum Tab {
  HOME = 'HOME',
  FRAMEWORK = 'FRAMEWORK',
  GENERATOR = 'GENERATOR',
  KNOWLEDGE = 'KNOWLEDGE',
  WIZARD = 'WIZARD',
  COMMUNITY = 'COMMUNITY', 
}

export interface Collaborator {
  id: string;
  name: string;
  color: string;
}

export type CollabMessage = 
  | { type: 'JOIN'; user: Collaborator }
  | { type: 'PRESENCE'; user: Collaborator }
  | { type: 'UPDATE_DATA'; data: RcateData; senderId: string }
  | { type: 'UPDATE_RESPONSE'; response: string; senderId: string };

export type AgentRole = 'DRAFTER' | 'MANAGER' | 'AUDITOR';

export interface WorkflowStep {
  id: number;
  role: AgentRole;
  agentName: string;
  status: 'pending' | 'working' | 'completed' | 'error';
  content: string;
  timestamp?: Date;
}

export interface AuthUser {
  id: string;
  name: string;
  email: string;
  avatarUrl?: string;
  isAuthenticated: boolean;
}

export interface KnowledgeDoc {
  id: string;
  name: string;
  type: 'PDF' | 'EXCEL' | 'WORD' | 'TEXT' | 'VIDEO';
  size: string;
  uploadDate: Date;
  content: string; 
  mimeType: string;
  summary?: string;
}

export interface KnowledgeFolder {
  id: string;
  name: string;
  docs: KnowledgeDoc[];
}

export interface BriefingItem {
  category: 'Local' | 'Economy' | 'CPA' | 'Tech' | 'Tip';
  headline: string;
  url: string;
}

export interface ChatMessage {
  id: string;
  sender: string;
  text: string;
  timestamp: Date;
  isMe: boolean;
  type: 'text' | 'file';
  fileName?: string;
  role?: 'DRAFTER' | 'MANAGER' | 'AUDITOR' | 'USER'; 
}

export interface ChatRoom {
  id: string;
  name: string;
  type: 'team' | 'kakao_import' | 'ai_council';
  lastMessage: string;
  updatedAt: Date;
  messages: ChatMessage[];
  participants: number;
}

// --- SCHEDULE & TASKS ---
export interface CalendarEvent {
  id: string;
  time: string;
  title: string;
  subtitle: string;
  status: 'upcoming' | 'active' | 'done';
  timestamp: Date; // For sorting/logic
  link?: string; // Deep link to Google Calendar
}

export interface TaskItem {
  id: string;
  text: string;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
}

// --- AUTOMATION / BROWSER AGENT TYPES ---
export interface BrowserStep {
  action: 'NAVIGATE' | 'READ_EXCEL' | 'ANALYZE' | 'WRITE_WORD' | 'SAVE';
  status: 'pending' | 'running' | 'done';
  description: string;
  url?: string;
  contentPreview?: string; // HTML/Text showing what agent sees
}

export interface BrowserState {
  isOpen: boolean;
  activeStepIndex: number;
  steps: BrowserStep[];
  logs: string[];
  targetDocId?: string;
  memory: Record<string, string>; // To pass data between steps (e.g. extracted numbers)
}

// --- GLOBAL STATE INTERFACE ---
export interface AppState {
  user: AuthUser | null;
  currentTab: Tab;
  knowledgeFolders: KnowledgeFolder[];
  rcateData: RcateData;
  briefingItems: BriefingItem[];
  chatHistory: { role: 'user' | 'model'; text: string }[];
  
  // Templates
  userTemplates: Template[];
  saveUserTemplate: (template: Template) => void;
  deleteUserTemplate: (id: string) => void;

  // Calculator State
  calculatorTotal: number;
  isCalculatorOpen: boolean;
  
  // Browser Agent State
  browserState: BrowserState;

  // Schedule & Tasks
  isGoogleConnected: boolean;
  connectGoogle: () => void;
  disconnectGoogle: () => void;
  calendarEvents: CalendarEvent[];
  todoList: TaskItem[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;

  // Actions
  setUser: (user: AuthUser | null) => void;
  setCurrentTab: (tab: Tab) => void;
  setKnowledgeFolders: React.Dispatch<React.SetStateAction<KnowledgeFolder[]>>;
  setRcateData: React.Dispatch<React.SetStateAction<RcateData>>;
  setBriefingItems: (items: BriefingItem[]) => void;
  setChatHistory: React.Dispatch<React.SetStateAction<{ role: 'user' | 'model'; text: string }[]>>;
  
  // Calculator Actions
  setCalculatorTotal: (val: number) => void;
  toggleCalculator: () => void;
  
  // Browser Actions
  startBrowserAgent: (doc: KnowledgeDoc) => void;
  closeBrowserAgent: () => void;
  
  // Helpers
  addToChat: (text: string, role: 'user' | 'model') => void;
}