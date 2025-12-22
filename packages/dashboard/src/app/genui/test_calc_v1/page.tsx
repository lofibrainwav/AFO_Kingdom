"use client";
import React from "react";

export default function GenUIPage() {
  return (
    <div className="min-h-screen bg-black text-white p-8">
      <h1 className="text-xl text-gray-500 mb-8 border-b border-gray-800 pb-2">
        GenUI Sandbox: test_calc_v1
      </h1>

      <div className="p-4 bg-gray-800 rounded-xl border border-gray-700 max-w-sm mx-auto mt-10">
        <h2 className="text-white text-center mb-4 font-bold">GenUI Calculator</h2>
        <div className="bg-black text-green-400 p-4 rounded mb-4 text-right text-2xl font-mono">
          0
        </div>
        <div className="grid grid-cols-4 gap-2">
          {["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "=", "+"].map(
            (btn) => (
              <button
                key={btn}
                className="p-4 bg-gray-700 hover:bg-gray-600 rounded text-white font-bold transition-colors"
              >
                {btn}
              </button>
            )
          )}
        </div>
      </div>
    </div>
  );
}
