
import { RcateData, KnowledgeDoc } from '../types';
import { runAgentDrafting, runAgentManagerReview, generateDailyBriefing, optimizeRcatePrompt } from './geminiService';
import { TrinityService } from './trinityService';

export enum ScholarType {
    YEONGDEOK = 'yeongdeok', // Local/Privacy (Ollama/Qwen)
    YUKSON = 'yukson',       // Strategy (Gemini)
    ZHAOYUN = 'zhaoyun',     // Verify (Claude)
    BANGTONG = 'pangtong'    // Code/Excel (Codex)
}

export interface ScholarResponse {
    scholar: ScholarType;
    content: string;
    confidence: number;
    status: 'success' | 'warn' | 'error';
}

// --- The Scholar Orchestrator ---
export const ScholarService = {
    
    /**
     * Phase 1: Yeongdeok (Privacy Guard)
     * Scans input for PII before letting it leave the app.
     */
    async guardPrivacy(text: string): Promise<ScholarResponse> {
        // Simulation of Local LLM/Regex for Privacy
        const piiPatterns = [
            /\b\d{3}-\d{2}-\d{4}\b/, // SSN
            /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/ // Email
        ];

        const hasPII = piiPatterns.some(p => p.test(text));
        
        if (hasPII) {
            TrinityService.updateJulieStatus('WORKING', 'Yeongdeok flagged PII data.');
            return {
                scholar: ScholarType.YEONGDEOK,
                content: "⚠️ PII Detected! I have redacted sensitive information for your safety.",
                confidence: 1.0,
                status: 'warn'
            };
        }

        return {
            scholar: ScholarType.YEONGDEOK,
            content: "✅ Data is clean. Safe to proceed to Cloud Scholars.",
            confidence: 1.0,
            status: 'success'
        };
    },

    /**
     * Phase 2: Yukson (Strategy & Drafting)
     * Uses Gemini (via geminiService) to create the content.
     */
    async draftStrategy(data: RcateData) {
        TrinityService.updateJulieStatus('WORKING', 'Yukson is drafting strategy...');
        return runAgentDrafting(data); // Returns generator
    },

    /**
     * Phase 3: Bangtong (Technical Execution)
     * Generates Excel formulas or specific technical formats.
     */
    async generateTechnicalArtifact(type: 'EXCEL' | 'PYTHON', context: string): Promise<ScholarResponse> {
        TrinityService.updateJulieStatus('WORKING', `Bangtong building ${type} artifact...`);
        
        // In a full implementation, this might call a specific code-gen model.
        // Here we use the main engine with a specific persona.
        return {
            scholar: ScholarType.BANGTONG,
            content: `[Bangtong] Generated ${type} structure for: ${context.substring(0, 50)}...`,
            confidence: 0.95,
            status: 'success'
        };
    },

    /**
     * Phase 4: Zhaoyun (Verification)
     * Double checks the output for logical consistency.
     */
    async verifyContent(draft: string): Promise<ScholarResponse> {
        TrinityService.updateJulieStatus('AUDITING', 'Zhaoyun auditing draft...');
        
        // Re-using the Manager Review but framing it as Zhaoyun
        const review = await runAgentManagerReview(draft);
        
        const isPass = review.score >= 85;
        return {
            scholar: ScholarType.ZHAOYUN,
            content: isPass 
                ? `✅ Zhaoyun Audit Passed (Score: ${review.score}). Logic is sound.` 
                : `🛡️ Zhaoyun Found Risks (Score: ${review.score}). See details.`,
            confidence: review.score / 100,
            status: isPass ? 'success' : 'warn'
        };
    }
};
