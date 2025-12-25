"use client";

import RoyalOpsCenter from "@/components/genui/RoyalOpsCenter";
import TreeOfThoughts from "@/components/genui/TreeOfThoughts";
import { motion } from "framer-motion";

export default function RealtimeStatusPage() {
  return (
    <div className="min-h-screen bg-[#0f111a] text-white p-6 md:p-10 lg:p-12 font-sans">
      <div className="max-w-[1600px] mx-auto space-y-8">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          {/* Header content managed inside RoyalOpsCenter or handled here if separate */}
        </motion.header>

        {/* Genesis Component: Royal Ops Center */}
        <motion.div
           initial={{ opacity: 0, scale: 0.95 }}
           animate={{ opacity: 1, scale: 1 }}
           transition={{ duration: 0.5 }}
        >
            <RoyalOpsCenter />
        </motion.div>

        {/* Genesis Component: Tree of Thoughts */}
        <motion.div
           initial={{ opacity: 0, y: 50 }}
           animate={{ opacity: 1, y: 0 }}
           transition={{ duration: 0.5, delay: 0.2 }}
        >
            <TreeOfThoughts />
        </motion.div>
      </div>
    </div>
  );
}

