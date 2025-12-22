"use client";

/**
 * AICPA Control Panel
 *
 * 에이전트 군단 지휘소
 * 클라이언트 입력 → 전체 미션 실행 → 결과물 다운로드
 *
 * 眞 (Truth): 정확한 세금 계산
 * 善 (Goodness): 최적의 절세 전략
 * 美 (Beauty): 아름다운 Glassmorphism UI
 * 孝 (Serenity): Zero Friction - 버튼 하나로 완료
 */

import React, { useState, useCallback } from "react";
import {
  Users,
  Zap,
  FileText,
  Mail,
  Calculator,
  Download,
  RefreshCw,
  CheckCircle,
  AlertTriangle,
  Crown,
} from "lucide-react";
import { logError } from "@/lib/logger";

interface MissionResult {
  client: {
    name: string;
    filing_status: string;
    gross_income: number;
    traditional_ira_balance: number;
    goal: string;
  };
  tax_analysis: {
    total_tax: number;
    effective_federal_rate: number;
    roth_conversion_recommendation: number;
    advice: string;
  };
  roth_strategy: {
    strategy: string;
    estimated_savings: number;
    summary: string;
  } | null;
  generated_files: {
    word_report: string;
    turbotax_csv: string;
    quickbooks_csv: string;
    email_draft: string;
  };
  summary: string;
}

import { API_BASE_URL } from "@/lib/constants";
const API_BASE = API_BASE_URL;

export const AICPAControlPanel: React.FC = () => {
  const [clientName, setClientName] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MissionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Memoize execute mission function
  const executeMission = useCallback(async () => {
    if (!clientName.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/aicpa/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ client_name: clientName }),
      });

      if (!response.ok) throw new Error("Mission Failed");

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("에이전트 연결 실패 - 서버 상태를 확인하세요");
      logError("[AICPA] Error", { error: err instanceof Error ? err.message : "Unknown error" });
    } finally {
      setLoading(false);
    }
  }, [clientName]);

  // Memoize currency formatter
  const formatCurrency = useCallback((value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(value);
  }, []);

  // Memoize input handler
  const handleClientNameChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setClientName(e.target.value);
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-purple-900 to-slate-900 rounded-3xl p-8 text-white relative overflow-hidden">
        {/* Glow Effect */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />

        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-amber-500/20 rounded-2xl border border-amber-500/30">
              <Crown className="w-8 h-8 text-amber-400" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">AICPA Agent Army</h1>
              <p className="text-slate-400">Command Center | AFO Kingdom</p>
            </div>
          </div>

          <p className="text-slate-300 max-w-lg mb-6">
            클라이언트 이름을 입력하고 "Run Agents"를 클릭하면 세금 분석부터 문서 생성까지 자동으로
            처리됩니다.
          </p>

          {/* Input Section */}
          <div className="flex gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={clientName}
                onChange={handleClientNameChange}
                placeholder="Enter client name (e.g., Justin Mason)"
                className="w-full bg-white/10 backdrop-blur border border-white/20 rounded-xl px-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                aria-label="Client name input"
              />
            </div>
            <button
              onClick={executeMission}
              disabled={loading || !clientName.trim()}
              className={`px-8 py-3 rounded-xl font-bold flex items-center gap-2 transition-all ${
                loading || !clientName.trim()
                  ? "bg-slate-600 cursor-not-allowed"
                  : "bg-gradient-to-r from-emerald-600 to-teal-600 hover:shadow-lg hover:shadow-emerald-500/30 hover:scale-105"
              }`}
              aria-label={loading ? "Processing mission" : "Run AICPA agents mission"}
              aria-busy={loading}
            >
              {loading ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  Run Agents
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div
          className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-rose-700 flex items-center gap-3"
          role="alert"
          aria-live="assertive"
        >
          <AlertTriangle className="w-5 h-5" aria-hidden="true" />
          {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6" role="region" aria-label="Mission results">
          {/* Client Info */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-blue-100 rounded-xl">
                <Users className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="font-bold text-slate-800">Client Profile</h3>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-500">Name</span>
                <span className="font-bold">{result.client.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Filing Status</span>
                <span className="font-bold uppercase">{result.client.filing_status}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Gross Income</span>
                <span className="font-bold">{formatCurrency(result.client.gross_income)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Traditional IRA</span>
                <span className="font-bold">
                  {formatCurrency(result.client.traditional_ira_balance)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Goal</span>
                <span className="font-bold text-emerald-600">{result.client.goal}</span>
              </div>
            </div>
          </div>

          {/* Tax Analysis */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-emerald-100 rounded-xl">
                <Calculator className="w-5 h-5 text-emerald-600" />
              </div>
              <h3 className="font-bold text-slate-800">Tax Analysis</h3>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-500">Total Tax</span>
                <span className="font-bold text-lg">
                  {formatCurrency(result.tax_analysis.total_tax)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Effective Rate</span>
                <span className="font-bold">{result.tax_analysis.effective_federal_rate}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Roth Conversion Rec.</span>
                <span className="font-bold text-emerald-600">
                  {formatCurrency(result.tax_analysis.roth_conversion_recommendation)}
                </span>
              </div>
            </div>

            <div className="mt-4 p-3 bg-slate-50 rounded-xl text-sm text-slate-600">
              {result.tax_analysis.advice}
            </div>
          </div>

          {/* Roth Strategy */}
          {result.roth_strategy && (
            <div className="md:col-span-2 bg-gradient-to-r from-purple-50 to-emerald-50 rounded-3xl border border-purple-100 p-6">
              <div className="flex items-center gap-3 mb-4">
                <CheckCircle className="w-6 h-6 text-emerald-600" />
                <h3 className="font-bold text-slate-800">{result.roth_strategy.strategy}</h3>
              </div>
              <p className="text-slate-600 mb-2">{result.roth_strategy.summary}</p>
              <div className="inline-block bg-emerald-100 text-emerald-700 px-4 py-2 rounded-xl font-bold">
                Estimated Savings: {formatCurrency(result.roth_strategy.estimated_savings)}
              </div>
            </div>
          )}

          {/* Generated Files */}
          <div className="md:col-span-2 bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-amber-100 rounded-xl">
                <Download className="w-5 h-5 text-amber-600" />
              </div>
              <h3 className="font-bold text-slate-800">Generated Files</h3>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <FileCard
                icon={<FileText className="w-5 h-5 text-blue-500" />}
                title="Strategy Report"
                format="DOCX"
                path={result.generated_files.word_report}
              />
              <FileCard
                icon={<Calculator className="w-5 h-5 text-red-500" />}
                title="TurboTax Data"
                format="CSV"
                path={result.generated_files.turbotax_csv}
              />
              <FileCard
                icon={<FileText className="w-5 h-5 text-green-500" />}
                title="QuickBooks"
                format="CSV"
                path={result.generated_files.quickbooks_csv}
              />
              <FileCard
                icon={<Mail className="w-5 h-5 text-amber-500" />}
                title="Email Draft"
                format="TXT"
                hasPreview={true}
                content={result.generated_files.email_draft}
              />
            </div>
          </div>

          {/* Mission Summary */}
          <div className="md:col-span-2 bg-slate-900 text-white rounded-3xl p-6">
            <div className="flex items-center gap-2 text-amber-400 mb-3">
              <Crown className="w-5 h-5" />
              <span className="font-bold">Mission Complete</span>
            </div>
            <pre className="text-slate-300 text-sm whitespace-pre-wrap font-mono">
              {result.summary}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

// File Card Component
const FileCard = ({
  icon,
  title,
  format,
  path: _path,
  hasPreview,
  content,
}: {
  icon: React.ReactNode;
  title: string;
  format: string;
  path?: string;
  hasPreview?: boolean;
  content?: string;
}) => {
  const [showPreview, setShowPreview] = useState(false);

  return (
    <>
      <div
        onClick={() => hasPreview && content && setShowPreview(true)}
        className={`p-4 bg-slate-50 rounded-2xl border border-slate-100 hover:bg-slate-100 transition-colors ${
          hasPreview ? "cursor-pointer" : ""
        }`}
      >
        <div className="flex items-center gap-3">
          {icon}
          <div className="flex-1 min-w-0">
            <div className="text-sm font-bold text-slate-800 truncate">{title}</div>
            <div className="text-xs text-slate-500">{format}</div>
          </div>
        </div>
      </div>

      {/* Preview Modal */}
      {showPreview && content && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setShowPreview(false)}
        >
          <div
            className="bg-white rounded-2xl p-6 max-w-2xl w-full max-h-[80vh] overflow-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="font-bold text-lg mb-4">{title} Preview</h3>
            <pre className="text-sm bg-slate-50 p-4 rounded-xl whitespace-pre-wrap font-mono">
              {content}
            </pre>
            <button
              onClick={() => setShowPreview(false)}
              className="mt-4 px-4 py-2 bg-slate-900 text-white rounded-xl text-sm font-bold"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default AICPAControlPanel;
