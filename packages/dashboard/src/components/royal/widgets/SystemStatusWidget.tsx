"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Activity, Server, Cpu, HardDrive } from "lucide-react";

export const SystemStatusWidget = () => {
    // Simulated Data for "Vibe"
    const [metrics, setMetrics] = useState({ cpu: 12, mem: 45, disk: 30 });
    
    useEffect(() => {
        const interval = setInterval(() => {
            setMetrics({
                cpu: Math.floor(Math.random() * 20) + 10,
                mem: Math.floor(Math.random() * 10) + 40,
                disk: 30
            });
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    return (
        <Card className="bg-white/50 backdrop-blur-md border-white/60 shadow-lg hover:shadow-xl transition-all duration-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-bold text-slate-600 flex items-center gap-2">
                    <Server className="w-4 h-4 text-blue-500" />
                    SYSTEM VITALITY
                </CardTitle>
                <Badge variant="outline" className="bg-green-100 text-green-700 border-green-200">
                    NORMAL
                </Badge>
            </CardHeader>
            <CardContent>
                <div className="space-y-4 mt-2">
                    {/* CPU */}
                    <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                        <span className="flex items-center gap-1"><Cpu className="w-3 h-3"/> CPU Load</span>
                        <span>{metrics.cpu}%</span>
                    </div>
                    <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-blue-500 rounded-full transition-all duration-1000 ease-out"                                    style={{ width: `${Math.min(metrics.cpu, 100)}%` }} 
                        />
                    </div>

                    {/* Memory */}
                    <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                        <span className="flex items-center gap-1"><Activity className="w-3 h-3"/> Memory</span>
                        <span>{metrics.mem}%</span>
                    </div>
                    <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-purple-500 rounded-full transition-all duration-1000 ease-out" 
                            style={{ width: `${Math.min(metrics.mem, 100)}%` }} 
                        />
                    </div>

                    {/* Disk */}
                    <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                        <span className="flex items-center gap-1"><HardDrive className="w-3 h-3"/> Storage</span>
                        <span>{metrics.disk}%</span>
                    </div>
                    <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-slate-400 rounded-full transition-all duration-1000 ease-out" 
                            style={{ width: `${Math.min(metrics.disk, 100)}%` }} 
                        />
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};
