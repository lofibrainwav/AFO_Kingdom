import React from "react";
import { AlertCircle, Check, X } from "lucide-react";

interface ApprovalItem {
  id: string;
  title: string;
  amount: number;
  requester: string;
  reason: string;
}

export default function ApprovalQueue({ items }: { items: ApprovalItem[] }) {
  return (
    <div className="bg-[#0A0F1C] border border-gray-800 rounded-2xl overflow-hidden flex flex-col">
      <div className="p-6 border-b border-gray-800 flex justify-between items-center bg-gradient-to-r from-amber-900/10 to-transparent">
        <h3 className="text-amber-200 font-medium flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-500" />
          The Prince's Desk (Approvals)
        </h3>
        <span className="text-xs font-bold text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded-full">
          {items.length} Pending
        </span>
      </div>

      <div className="p-4 space-y-3">
        {items.length === 0 ? (
          <div className="text-center py-8 text-gray-600 text-sm">
            No pending approvals. The desk is clear.
          </div>
        ) : (
          items.map((item) => (
            <div key={item.id} className="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-medium text-gray-200 text-sm">{item.title}</h4>
                <span className="font-mono text-amber-400 font-bold">
                  {item.amount.toLocaleString()} ₩
                </span>
              </div>
              <p className="text-xs text-gray-500 mb-3">
                {item.reason} • <span className="text-gray-400">Req: {item.requester}</span>
              </p>

              <div className="flex gap-2">
                <button className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium py-2 rounded-lg flex justify-center items-center gap-1 transition-colors">
                  <Check className="w-3 h-3" /> Approve
                </button>
                <button className="flex-1 bg-white/5 hover:bg-white/10 text-gray-300 text-xs font-medium py-2 rounded-lg flex justify-center items-center gap-1 transition-colors">
                  <X className="w-3 h-3" /> Reject
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
