
import { RcateData } from '../types';

// --- Types for Trinity Integration ---
export interface MemberScore {
    name: string;
    truth: number;
    goodness: number;
    beauty: number;
    serenity: number;
    forever: number;
    message: string;
}

export interface FamilyHubStatus {
    timestamp: string;
    family: {
        name: string;
        harmony_score: number;
    };
    members: Record<string, any>; // Simplified for now
    daily_message: {
        message: string;
        emoji: string;
        type: string;
    };
}

const TRINITY_API_BASE = 'http://localhost:8010/api/5pillars';

// --- Trinity Service ---
export const TrinityService = {
    /**
     * Updates Julie's status in the Family Hub.
     * Call this when significant actions occur (e.g., completing an audit).
     */
    async updateJulieStatus(action: 'IDLE' | 'WORKING' | 'AUDITING' | 'RESTING', detail: string): Promise<boolean> {
        // Default Baseline Scores for Julie (High Goodness/Truth)
        const baseScore: MemberScore = {
            name: 'Julie',
            truth: 0.95,
            goodness: 0.98,
            beauty: 0.92,
            serenity: 0.97,
            forever: 0.99,
            message: "Ready for work 💼"
        };

        // Adjust scores based on context
        if (action === 'AUDITING') {
            baseScore.truth = 0.99; // Peak Truth focus
            baseScore.serenity = 0.90; // High stress
            baseScore.message = `Auditing: ${detail} 👁️`;
        } else if (action === 'WORKING') {
            baseScore.goodness = 0.99; // Serving clients
            baseScore.message = `Working: ${detail} 📝`;
        } else if (action === 'RESTING') {
            baseScore.serenity = 0.99;
            baseScore.message = "Recharging 🍵";
        }

        try {
            const response = await fetch(`${TRINITY_API_BASE}/family/hub/member/update`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(baseScore)
            });
            
            if (!response.ok) throw new Error('Failed to update Trinity');
            console.log(`[Trinity] Julie Status Updated: ${action}`);
            return true;
        } catch (e) {
            console.warn("[Trinity] Connection Failed (Dev Mode?):", e);
            return false;
        }
    },

    /**
     * Fetches the current Family Hub state to display team status.
     */
    async getFamilyStatus(): Promise<FamilyHubStatus | null> {
        try {
            const response = await fetch(`${TRINITY_API_BASE}/family/hub`);
            if (!response.ok) throw new Error('Failed to fetch Family Hub');
            return await response.json();
        } catch (e) {
            console.warn("[Trinity] Fetch Failed:", e);
            return null;
        }
    }
};
