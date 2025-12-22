'use client';

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { motion } from "framer-motion";
import { Crown } from "lucide-react";

// Mock Data
const data = [
  { day: 'Day 1', Truth: 80, Goodness: 75, Beauty: 60 },
  { day: 'Day 2', Truth: 82, Goodness: 78, Beauty: 65 },
  { day: 'Day 3', Truth: 85, Goodness: 80, Beauty: 70 },
  { day: 'Day 4', Truth: 88, Goodness: 85, Beauty: 75 },
  { day: 'Day 5', Truth: 87, Goodness: 90, Beauty: 80 },
  { day: 'Day 6', Truth: 89, Goodness: 88, Beauty: 85 },
  { day: 'Day 7', Truth: 92, Goodness: 91, Beauty: 95 },
];

export default function RoyalAnalyticsWidget() {
    return (
        <motion.div 
            initial={{ opacity: 0, y: 20 }} 
            animate={{ opacity: 1, y: 0 }} 
            transition={{ duration: 0.8 }}
            className="w-full"
        >
            <Card className="w-full h-96 bg-white/10 backdrop-blur-md border border-white/20 shadow-xl overflow-hidden">
                <CardContent className="p-6 h-full flex flex-col">
                    <div className="flex items-center gap-2 mb-4">
                        <Crown className="w-6 h-6 text-amber-400" />
                        <h2 className="text-xl font-bold text-white tracking-widest uppercase">Royal Trinity Analysis</h2>
                    </div>
                    <div className="flex-1 min-h-0">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis dataKey="day" stroke="rgba(255,255,255,0.5)" tick={{fill: 'white', fontSize: 12}} />
                                <YAxis stroke="rgba(255,255,255,0.5)" tick={{fill: 'white', fontSize: 12}} />
                                <Tooltip 
                                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                                <Line type="monotone" dataKey="Truth" stroke="#06b6d4" strokeWidth={3} dot={{r: 4}} activeDot={{r: 8}} />
                                <Line type="monotone" dataKey="Goodness" stroke="#10b981" strokeWidth={3} dot={{r: 4}} activeDot={{r: 8}} />
                                <Line type="monotone" dataKey="Beauty" stroke="#a855f7" strokeWidth={3} dot={{r: 4}} activeDot={{r: 8}} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </CardContent>
            </Card>
        </motion.div>
    );
}
