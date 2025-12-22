"use client";
import React from "react";

export default function GenUIPage() {
  return (
    <div className="min-h-screen bg-black text-white p-8">
      <h1 className="text-xl text-gray-500 mb-8 border-b border-gray-800 pb-2">
        GenUI Sandbox: test_vision_block
      </h1>

      <div className="p-10 text-center">
        <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
          dashboard
        </h2>
        <p className="text-gray-400 mt-4">Created by GenUI Orchestrator</p>
        <div className="mt-8 animate-pulse">
          <span className="px-4 py-2 bg-blue-500/20 text-blue-300 rounded-full border border-blue-500/30">
            Autonomously Generated
          </span>
        </div>
      </div>
    </div>
  );
}
