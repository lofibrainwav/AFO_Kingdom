// AICPA/aicpa-core/services/julieService.ts

export interface JulieStatusResponse {
    status: string;
    alerts: string[];
    advice: string;
    dry_run_tx_count: number;
}

// Default mock data in case backend is unreachable (Graceful Degradation - 善)
const MOCK_STATUS: JulieStatusResponse = {
    status: "Offline Mode",
    alerts: ["⚠️ Backend disconnected"],
    advice: "Check connection to Soul Engine (Port 8010).\nEnsure 'python api_server.py' is running.",
    dry_run_tx_count: 0
};

export const JulieService = {
    /**
     * Fetches the real-time status of the Julie CPA Engine.
     * Endpoint: /api/julie/status
     */
    async getStatus(): Promise<JulieStatusResponse> {
        try {
            // AFO Kingdom Integration: Use environment variable for API base
            const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8010';
            const response = await fetch(`${API_BASE}/api/julie/status`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                console.warn("[JulieService] Backend responded with error:", response.status);
                throw new Error("Backend Error");
            }

            return await response.json();
        } catch (e) {
            console.error("[JulieService] Connection Failed:", e);
            return MOCK_STATUS;
        }
    }
};
