import React, { createContext, useContext, useState, ReactNode, useCallback, useEffect } from 'react';
import { AppState, AuthUser, Tab, KnowledgeFolder, RcateData, BriefingItem, BrowserState, KnowledgeDoc, CalendarEvent, TaskItem, Template } from '../types';

const INITIAL_RCATE: RcateData = {
  role: 'CPA Expert',
  context: '',
  audience: 'Client / Board',
  task: '',
  execution: 'Step-by-step Analysis'
};

const INITIAL_BROWSER: BrowserState = {
  isOpen: false,
  activeStepIndex: 0,
  steps: [],
  logs: [],
  memory: {}
};

interface Notification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
}

interface AppStateExtended extends AppState {
  notification: Notification | null;
  showNotification: (message: string, type?: 'success' | 'error' | 'info' | 'warning') => void;
  closeNotification: () => void;
  resetApp: () => void;
  
  // Private setters for internal logic (exposed via start/close methods)
  setBrowserState: React.Dispatch<React.SetStateAction<BrowserState>>;
}

const AppContext = createContext<AppStateExtended | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // --- 1. Load Initial State ---
  // Updated keys to 'aicpa_core_*' to invalidate old 'AICPA Nexus' cache
  const loadState = <T,>(key: string, fallback: T): T => {
    try {
      const stored = localStorage.getItem(key);
      return stored ? JSON.parse(stored) : fallback;
    } catch (e) {
      return fallback;
    }
  };

  const [user, setUser] = useState<AuthUser | null>(() => loadState('aicpa_core_user', null));
  const [currentTab, setCurrentTab] = useState<Tab>(() => loadState('aicpa_core_tab', Tab.HOME));
  const [knowledgeFolders, setKnowledgeFolders] = useState<KnowledgeFolder[]>(() => loadState('aicpa_core_folders', []));
  const [rcateData, setRcateData] = useState<RcateData>(() => loadState('aicpa_core_rcate', INITIAL_RCATE));
  const [userTemplates, setUserTemplates] = useState<Template[]>(() => loadState('aicpa_core_user_templates', []));
  const [isGoogleConnected, setIsGoogleConnected] = useState<boolean>(() => loadState('aicpa_core_gcal_connected', false));
  
  // Chat history with corrected initial greeting
  const [chatHistory, setChatHistory] = useState<{ role: 'user' | 'model'; text: string }[]>(() => loadState('aicpa_core_chat', [
    { role: 'model', text: '안녕하세요! AICPA Core 통합 어시스턴트입니다.\n무엇을 도와드릴까요?' }
  ]));
  
  // Transient States
  const [briefingItems, setBriefingItems] = useState<BriefingItem[]>([]);
  const [notification, setNotification] = useState<Notification | null>(null);
  const [calculatorTotal, setCalculatorTotal] = useState<number>(0);
  const [isCalculatorOpen, setIsCalculatorOpen] = useState<boolean>(false);
  const [browserState, setBrowserState] = useState<BrowserState>(INITIAL_BROWSER);
  
  // Schedule & Tasks (Persisted)
  const [calendarEvents, setCalendarEvents] = useState<CalendarEvent[]>([]); 
  const [todoList, setTodoList] = useState<TaskItem[]>(() => loadState('aicpa_core_todos', []));

  // --- 2. Persist State Changes (New Keys) ---
  useEffect(() => { localStorage.setItem('aicpa_core_user', JSON.stringify(user)); }, [user]);
  useEffect(() => { localStorage.setItem('aicpa_core_tab', JSON.stringify(currentTab)); }, [currentTab]);
  useEffect(() => { localStorage.setItem('aicpa_core_folders', JSON.stringify(knowledgeFolders)); }, [knowledgeFolders]);
  useEffect(() => { localStorage.setItem('aicpa_core_rcate', JSON.stringify(rcateData)); }, [rcateData]);
  useEffect(() => { localStorage.setItem('aicpa_core_user_templates', JSON.stringify(userTemplates)); }, [userTemplates]);
  useEffect(() => { localStorage.setItem('aicpa_core_chat', JSON.stringify(chatHistory)); }, [chatHistory]);
  useEffect(() => { localStorage.setItem('aicpa_core_gcal_connected', JSON.stringify(isGoogleConnected)); }, [isGoogleConnected]);
  useEffect(() => { localStorage.setItem('aicpa_core_todos', JSON.stringify(todoList)); }, [todoList]);

  const toggleCalculator = () => setIsCalculatorOpen(prev => !prev);

  const addTodo = (text: string) => {
      const newItem: TaskItem = {
          id: Date.now().toString(),
          text,
          completed: false,
          priority: 'medium'
      };
      setTodoList(prev => [newItem, ...prev]);
  };

  const toggleTodo = (id: string) => {
      setTodoList(prev => prev.map(t => t.id === id ? { ...t, completed: !t.completed } : t));
  };

  const deleteTodo = (id: string) => {
      setTodoList(prev => prev.filter(t => t.id !== id));
  };
  
  const connectGoogle = () => setIsGoogleConnected(true);
  const disconnectGoogle = () => setIsGoogleConnected(false);

  const saveUserTemplate = (template: Template) => {
      setUserTemplates(prev => [...prev, template]);
  };

  const deleteUserTemplate = (id: string) => {
      setUserTemplates(prev => prev.filter(t => t.id !== id));
  };

  const addToChat = (text: string, role: 'user' | 'model') => {
    setChatHistory(prev => [...prev, { role, text }]);
  };

  const showNotification = useCallback((message: string, type: 'success' | 'error' | 'info' | 'warning' = 'info') => {
    const id = Date.now().toString();
    setNotification({ id, message, type });
    setTimeout(() => {
        setNotification(prev => prev?.id === id ? null : prev);
    }, 4000);
  }, []);

  const closeNotification = () => setNotification(null);

  const startBrowserAgent = (doc: KnowledgeDoc) => {
      setBrowserState({
          isOpen: true,
          activeStepIndex: 0,
          targetDocId: doc.id,
          logs: [`Agent initiated for document: ${doc.name}`],
          memory: {},
          steps: [
              { action: 'NAVIGATE', status: 'pending', description: 'Opening Office 365 Environment...', url: 'https://www.office.com/launch/excel' },
              { action: 'READ_EXCEL', status: 'pending', description: `Scanning ${doc.name} for key figures...`, url: `https://excel.office.com/d/${doc.id}` },
              { action: 'ANALYZE', status: 'pending', description: 'Cross-referencing with Accounting Standards...', url: 'aicpa://analysis/engine' },
              { action: 'WRITE_WORD', status: 'pending', description: 'Drafting Audit Memo in Word...', url: 'https://word.office.com/new' },
              { action: 'SAVE', status: 'pending', description: 'Saving to Knowledge Base...', url: 'aicpa://local/save' }
          ]
      });
  };

  const closeBrowserAgent = () => {
      setBrowserState(prev => ({ ...prev, isOpen: false }));
  };

  const resetApp = () => {
      localStorage.clear();
      localStorage.removeItem('gemini_api_key');
      setUser(null);
      setKnowledgeFolders([]);
      setRcateData(INITIAL_RCATE);
      setChatHistory([]);
      setUserTemplates([]);
      setIsGoogleConnected(false);
      setTodoList([]);
      window.location.reload();
  };

  const value: AppStateExtended = {
    user, setUser,
    currentTab, setCurrentTab,
    knowledgeFolders, setKnowledgeFolders,
    rcateData, setRcateData,
    briefingItems, setBriefingItems,
    chatHistory, setChatHistory,
    userTemplates, saveUserTemplate, deleteUserTemplate,
    calculatorTotal, setCalculatorTotal,
    isCalculatorOpen, toggleCalculator,
    browserState, setBrowserState, startBrowserAgent, closeBrowserAgent,
    calendarEvents, todoList, addTodo, toggleTodo, deleteTodo,
    isGoogleConnected, connectGoogle, disconnectGoogle,
    addToChat,
    notification, showNotification, closeNotification,
    resetApp
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within an AppProvider');
  return context;
};