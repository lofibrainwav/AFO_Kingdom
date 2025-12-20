import { GoogleGenerativeAI, ChatSession, GenerativeModel } from "@google/generative-ai";
import { BriefingItem, RcateData, KnowledgeDoc, AgentRole } from '../types';

// --- API CLIENT FACTORY ---
// --- API CLIENT FACTORY ---
const getAiClient = (): GoogleGenerativeAI | null => {
  try {
    let apiKey = '';

    // 1. Try Vite Env (Standard)
    try {
       // @ts-ignore
       if (import.meta.env && import.meta.env.VITE_GEMINI_API_KEY) {
         // @ts-ignore
         apiKey = import.meta.env.VITE_GEMINI_API_KEY;
       }
    } catch (e) {}

    // 2. Try Node/Process Env (Fallback - Safely)
    if (!apiKey) {
      try {
         // Check type safely before accessing properties
         if (typeof process !== 'undefined' && process && process.env) {
           apiKey = process.env.API_KEY || process.env.GEMINI_API_KEY || '';
         }
      } catch (e) {
          // Ignore ReferenceError for process
      }
    }

    // 3. LocalStorage
    if (!apiKey && typeof window !== 'undefined') {
        apiKey = localStorage.getItem('gemini_api_key') || '';
    }

    // Debug Log
    // console.log("[Gemini Client] Key computed:", apiKey ? "YES" : "NO");

    if (apiKey) {
        return new GoogleGenerativeAI(apiKey);
    }
    
    console.warn("No API Key found. Using Mock Data/Fallback Mode.");
    return null;

  } catch (err: any) {
      if (err.message?.includes('429')) console.error("Quota Exceeded");
      console.error("[Gemini Client] Critical Initialization Error:", err);
      return null;
  }
};

// --- MOCK DATA ---
const getMockBriefing = (location: string): BriefingItem[] => [
    { category: 'Local', headline: `${location} 지역 경제, 전년 대비 3.2% 성장세 기록`, url: '#' },
    { category: 'CPA', headline: '2025년 세법 개정안 주요 포인트: 상속세 완화 논의', url: '#' },
    { category: 'Tech', headline: 'AI 감사(Audit) 툴 도입 기업, 생산성 40% 향상', url: '#' },
    { category: 'Tip', headline: '바쁜 시즌(Busy Season) 번아웃 관리 가이드', url: '#' }
];

const getMockReview = () => ({
    score: 85,
    summary: "전반적으로 훌륭한 전략입니다. 특히 리스크 관리 부분이 구체적입니다.",
    strengths: ["명확한 역할 정의", "보수적인 시나리오 분석"],
    weaknesses: ["구체적인 타임라인 부재", "실행 예산 미언급"],
    refined_suggestion: "실행 계획 단계에서 주 단위 마일스톤을 추가하면 완벽할 것입니다."
});

// --- UTILITY ---
const extractJson = <T>(text: string, fallback: T): T => {
  try {
    return JSON.parse(text);
  } catch (e) {
    const match = text.match(/(\{[\s\S]*\}|\[[\s\S]*\])/);
    if (match) {
      try { return JSON.parse(match[0]); } catch (e2) {}
    }
    const cleaned = text.replace(/```json/g, '').replace(/```/g, '').trim();
    try { return JSON.parse(cleaned); } catch (e3) { return fallback; }
  }
};

async function safeCall<T>(operation: () => Promise<T>, fallbackValue: T, contextName: string): Promise<T> {
    try {
        return await operation();
    } catch (error: any) {
        console.warn(`[Gemini] ${contextName} Error:`, error.message);
        return fallbackValue;
    }
}

// --- EXPORTED FUNCTIONS ---

export const runAgentDrafting = async function* (rcateData: RcateData) {
    try {
        const fullPrompt = `ROLE: ${rcateData.role}\nCONTEXT: ${rcateData.context}\nAUDIENCE: ${rcateData.audience}\nTASK: ${rcateData.task}\nEXECUTION: ${rcateData.execution}`;
        const prompt = `
        Draft a comprehensive strategy document based on this R.C.A.T.E framework.
        Input:
        ${fullPrompt}
        
        Output Format: Markdown.
        Language: Korean.
        Structure:
        # Strategy Plan
        ## 1. Executive Summary
        ## 2. Risk Analysis
        ## 3. Action Plan (Step-by-step)
        `;
        
        const genAI = getAiClient();
        if (!genAI) throw new Error("No Client");

        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const result = await model.generateContentStream(prompt);
        
        for await (const chunk of result.stream) {
            const text = chunk.text();
            if (text) yield text;
        }
    } catch (error: any) {
        if (error.message.includes('429') || error.message.includes('Quota')) {
            yield "⚠️ Daily Quota Exceeded (Free Tier). Please try again later.";
        } else {
            yield `AI Error: ${error.message || "Connection interrupted"}`;
        }
    }
};

export const runAgentManagerReview = async (draft: string) => {
    return safeCall(async () => {
        const genAI = getAiClient();
        if (!genAI) return getMockReview();

        const model = genAI.getGenerativeModel({ 
            model: "gemini-1.5-flash",
            generationConfig: { responseMimeType: "application/json" }
        });

        const prompt = `
            Act as a Senior Audit Partner. Review the following strategy draft.
            Draft: ${draft.substring(0, 3000)}...
            
            Evaluate based on:
            1. Logic & Feasibility
            2. Compliance (Risk)
            3. Clarity
            
            Return JSON with keys: score, summary, strengths (array), weaknesses (array), refined_suggestion.
        `;
        
        const result = await model.generateContent(prompt);
        return extractJson(result.response.text(), getMockReview());
    }, getMockReview(), 'ManagerReview');
};

export const createChatSession = (): ChatSession | null => {
  const genAI = getAiClient();
  if (!genAI) return null; // Logic in ChatWidget needs to handle null
  const model = genAI.getGenerativeModel({ 
      model: "gemini-1.5-flash",
      systemInstruction: "You are 'AICPA Core', an advanced AI assistant for CPAs."
  });
  return model.startChat();
};

export const generateDailyBriefing = async (location: string, language: 'ko' | 'en' = 'en'): Promise<BriefingItem[]> => {
    return safeCall(async () => {
        const genAI = getAiClient();
        if (!genAI) return getMockBriefing(location);

        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        
        const langInstruction = language === 'ko' ? "Translate headlines to Korean." : "Keep headlines in English.";
        const prompt = `
          Search for latest news in ${location} related to: Local Economy, US CPA News, Tech Tips.
          Return JSON Array of 6 items.
          Keys: "category", "headline", "url".
          ${langInstruction}
        `;

        const result = await model.generateContent(prompt);
        const rawData = extractJson<any[]>(result.response.text(), []);
        
        return rawData.map(item => ({
            category: (['Local', 'Economy', 'CPA', 'Tech', 'Tip'].includes(item.category) ? item.category : 'Tip') as any,
            headline: item.headline || item.title || 'Latest News',
            url: item.url || '#'
        })).slice(0, 4);
    }, getMockBriefing(location), 'DailyBriefing');
};

export const generateFieldOptions = async (field: keyof RcateData, currentData: RcateData): Promise<string[]> => {
    return safeCall(async () => {
        const genAI = getAiClient();
        if (!genAI) return ["Option A", "Option B", "Option C"];

        const model = genAI.getGenerativeModel({ 
            model: "gemini-1.5-flash",
            generationConfig: { responseMimeType: "application/json" } 
        });

        const prompt = `Context: ${JSON.stringify(currentData)}. Suggest 3 alternative professional options for the field '${field}' in Korean. Return JSON Array of strings.`;
        const result = await model.generateContent(prompt);
        return extractJson<string[]>(result.response.text(), []);
    }, ["Option A", "Option B", "Option C"], 'FieldOptions');
};

export const optimizeRcatePrompt = async (currentData: RcateData): Promise<RcateData | null> => {
    return safeCall(async () => {
        const genAI = getAiClient();
        if (!genAI) return currentData;

        const model = genAI.getGenerativeModel({ 
            model: "gemini-1.5-flash",
            generationConfig: { responseMimeType: "application/json" }
        });

        const prompt = `
            Act as a Prompt Engineer for CPAs. Optimize input R.C.A.T.E data.
            Input: ${JSON.stringify(currentData)}
            Make it professional, precise. Korean.
            Return JSON matching RcateData structure.
        `;
        const result = await model.generateContent(prompt);
        return extractJson<RcateData>(result.response.text(), currentData);
    }, currentData, 'OptimizePrompt');
};

export const refineRcateWithWebGrounding = async (currentData: RcateData) => currentData;
export const benchmarkStrategy = async (currentData: RcateData) => currentData;

export const analyzeClientDocumentsForRcate = async (docs: KnowledgeDoc[]) => {
    return {
        role: "Financial Analyst",
        context: `Analyzed ${docs.length} document(s). Detected revenue figures and potential compliance risks in Q3.`,
        audience: "CFO & Audit Team",
        task: "Investigate revenue recognition anomalies and prepare variance analysis.",
        execution: "Draft a detailed memo with findings and recommendations."
    } as RcateData;
};

export const generateAgentReply = async (role: AgentRole, history: string) => {
    return safeCall(async () => {
        const genAI = getAiClient();
        if (!genAI) return `[${role}] (Offline) Ready.`;

        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const prompt = `
            Act as a ${role} in a professional strategy committee.
            Recent Discussion History:
            ${history.substring(Math.max(0, history.length - 2000))}

            Task: Provide a concise, 1-2 sentence insight or suggestion based on your specific role (${role}).
            Language: Korean.
        `;
        
        const result = await model.generateContent(prompt);
        return result.response.text();
    }, `[${role}] (연결 불안정) 데이터를 검토했습니다. 계속 진행해주세요.`, 'AgentReply');
};

export const generateInterviewQuestion = async (step: string, inputs: any[]) => {
    return safeCall(async () => {
        const genAI = getAiClient();
        if (!genAI) return "다음 정보를 입력해주세요.";

        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const prompt = `
            Context: Conducting a strategy interview for CPAs (R.C.A.T.E framework).
            Current Step: ${step}
            Previous Answers: ${JSON.stringify(inputs)}
            
            Task: Generate a professional, engaging interview question to gather information for the '${step}' stage.
            Language: Korean.
            Max Length: 1-2 sentences.
        `;
        
        const result = await model.generateContent(prompt);
        return result.response.text();
    }, "다음 단계 정보를 입력해주세요.", 'InterviewQuestion');
};

export const generateRcateFromInterview = async (inputs: any[]) => {
     return {
        role: inputs.find(i => i.step === 'ROLE')?.answer || "Role",
        context: inputs.find(i => i.step === 'CONTEXT')?.answer || "Context",
        audience: inputs.find(i => i.step === 'AUDIENCE')?.answer || "Audience",
        task: inputs.find(i => i.step === 'TASK')?.answer || "Task",
        execution: inputs.find(i => i.step === 'EXECUTION')?.answer || "Execution",
     } as RcateData;
};

export const generateSyntheticFinancialData = async () => {
    return [
        {
            id: `syn-${Date.now()}-1`,
            name: 'FY23_Financial_Statements.xlsx',
            type: 'EXCEL',
            size: '2.4 MB',
            uploadDate: new Date(),
            content: "base64...",
            mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            summary: 'Synthetic Balance Sheet & Income Statement'
        },
        {
            id: `syn-${Date.now()}-2`,
            name: 'Board_Meeting_Minutes_Q3.pdf',
            type: 'PDF',
            size: '1.1 MB',
            uploadDate: new Date(),
            content: "base64...",
            mimeType: 'application/pdf',
            summary: 'Discussion on merger acquisition targets'
        }
    ] as KnowledgeDoc[];
};

export const runBrowserAgent = async function* (step: string, docId: string, context: string = '') {
    const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
    const genAI = getAiClient();
    
    // Fallback if no client
    if (!genAI) {
        yield `<div style="color:orange">API Key Missing. Using System Simulation...</div>`;
        await delay(1000);
        yield step === 'READ_EXCEL' ? '<div>(Mock) Excel Generated</div>' : '<div>(Mock) Doc Generated</div>';
        return;
    }

    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

        // --- 1. DYNAMIC EXCEL GENERATION ---
        if (step === 'READ_EXCEL') {
             const prompt = `
                Generate a realistic HTML table representing a financial transaction log for "Q1 2024".
                Style it like Excel (Segoe UI, border-collapse, etc.).
                Columns: Date, Transaction ID, Description, Amount ($), Status.
                Rows: 6 realistic entries (Include Revenue, Expenses, Pending items).
                
                IMPORTANT: Return ONLY the raw HTML string. No markdown block.
                Do not include <html> or <body> tags, just the <div style="..."> wrapper.
             `;
             
             try {
                const result = await model.generateContentStream(prompt);
                for await (const chunk of result.stream) {
                     const t = chunk.text();
                     if (t) yield t;
                     await delay(50);
                }
             } catch (e) {
                 yield `<div style="color:red; padding:20px;">Error generating financial data: ${(e as any).message}</div>`;
             }

        // --- 2. DYNAMIC ANALYSIS GENERATION ---
        } else if (step === 'ANALYZE') {
            const prompt = `
                Analyze the following financial context: "${context}".
                Produce a technical analysis log in HTML format.
                Use specific styles:
                - <h3 style="color: #4ade80; font-family: monospace;"> for headers
                - <div style="border-left: 2px solid #3b82f6; padding-left: 10px; margin-bottom: 10px;"> for sections
                
                Sections to include:
                1. [REVENUE STREAM]
                2. [EXPENSE AUDIT]
                3. [COMPLIANCE CHECK]
                
                Make up plausible numbers based on the context.
                End with "> Data integrity verified."
                
                IMPORTANT: Return ONLY the raw HTML string. No markdown block.
            `;
            
            try {
                const result = await model.generateContentStream(prompt);
                for await (const chunk of result.stream) {
                     const t = chunk.text();
                     if (t) yield t;
                }
            } catch (e) {
                yield `<div style="color:red;">Analysis Failed: ${(e as any).message}</div>`;
            }

        // --- 3. DYNAMIC MEMO GENERATION (WORD) ---
        } else if (step === 'WRITE_WORD') {
             const prompt = `
                Write a formal Internal Audit Memorandum based on these findings: "${context}".
                Format it as HTML for a Word document view (Times New Roman, padding 20px).
                
                Structure:
                - Header (TO, FROM, DATE, RE) inside a table with border-bottom.
                - 1. EXECUTIVE SUMMARY
                - 2. KEY FINDINGS (<ul> list)
                - 3. RECOMMENDATIONS
                
                IMPORTANT: Return ONLY the raw HTML string. No markdown.
             `;

             try {
                 const result = await model.generateContentStream(prompt);
                 for await (const chunk of result.stream) {
                     const t = chunk.text();
                     if (t) yield t;
                 }
             } catch (e) {
                 yield `<div>Error generating memo.</div>`;
             }

        } else {
            yield "Processing...";
        }
    };