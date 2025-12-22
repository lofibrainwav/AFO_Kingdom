import React from "react";
import { ArrowUpRight, ArrowDownLeft, Clock, CheckCircle, XCircle, FileText } from "lucide-react";

interface Transaction {
  id: string;
  description: string;
  amount: number;
  type: "income" | "expense";
  status: "CLEARED" | "PENDING" | "REJECTED";
  date: string;
  category: string;
}

export default function TransactionLedger({ transactions }: { transactions: Transaction[] }) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case "CLEARED":
        return <CheckCircle className="w-4 h-4 text-emerald-500" />;
      case "REJECTED":
        return <XCircle className="w-4 h-4 text-red-500" />;
      default:
        return <Clock className="w-4 h-4 text-amber-500" />;
    }
  };

  return (
    <div className="bg-[#0A0F1C] border border-gray-800 rounded-2xl overflow-hidden flex flex-col h-full">
      <div className="p-6 border-b border-gray-800 flex justify-between items-center">
        <h3 className="text-gray-300 font-medium flex items-center gap-2">
          <FileText className="w-4 h-4 text-blue-400" />
          Royal Ledger
        </h3>
        <span className="text-xs text-gray-500 bg-gray-900 px-2 py-1 rounded border border-gray-800">
          Live Stream
        </span>
      </div>

      <div className="overflow-y-auto flex-1 p-2 space-y-1">
        {transactions.map((tx) => (
          <div
            key={tx.id}
            className="flex items-center justify-between p-3 hover:bg-white/5 rounded-lg transition-colors group"
          >
            <div className="flex items-center gap-4">
              <div
                className={`p-2 rounded-lg ${tx.type === "income" ? "bg-emerald-500/10 text-emerald-500" : "bg-red-500/10 text-red-500"}`}
              >
                {tx.type === "income" ? (
                  <ArrowDownLeft className="w-4 h-4" />
                ) : (
                  <ArrowUpRight className="w-4 h-4" />
                )}
              </div>
              <div>
                <div className="text-sm font-medium text-gray-200 group-hover:text-white transition-colors">
                  {tx.description}
                </div>
                <div className="text-xs text-gray-500 flex items-center gap-2">
                  <span>{tx.date}</span>
                  <span className="w-1 h-1 bg-gray-700 rounded-full"></span>
                  <span>{tx.category}</span>
                </div>
              </div>
            </div>

            <div className="text-right">
              <div
                className={`font-mono font-medium ${tx.type === "income" ? "text-emerald-400" : "text-gray-300"}`}
              >
                {tx.type === "income" ? "+" : "-"}
                {tx.amount.toLocaleString()} ₩
              </div>
              <div className="flex items-center justify-end gap-1 mt-1">
                {getStatusIcon(tx.status)}
                <span className="text-[10px] text-gray-500 font-medium tracking-wide">
                  {tx.status}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
