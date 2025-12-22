"use client";

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { GitBranch, GitCommit } from "lucide-react";

export const GitWidget = () => {
    return (
        <Card className="bg-white/50 backdrop-blur-md border-white/60 shadow-lg hover:shadow-xl transition-all duration-500">
             <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-bold text-slate-600 flex items-center gap-2">
                    <GitBranch className="w-4 h-4 text-orange-500" />
                    GIT REPOSITORY
                </CardTitle>
                <Badge variant="outline" className="bg-blue-100 text-blue-700 border-blue-200">
                    main
                </Badge>
            </CardHeader>
            <CardContent>
                 <div className="space-y-3 mt-2">
                    <div className="flex items-center gap-3 p-2 bg-white/60 rounded-lg border border-slate-100">
                        <GitCommit className="w-4 h-4 text-slate-400" />
                        <div className="flex-1">
                            <div className="text-xs font-mono text-slate-400">SHA: a8f9c2</div>
                            <div className="text-xs font-medium text-slate-700">feat: Project Genesis Init</div>
                        </div>
                    </div>
                    
                    <div className="flex items-center justify-between text-xs">
                        <span className="text-slate-500">Status</span>
                        <span className="text-green-600 font-bold flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"/> Clean
                        </span>
                    </div>
                 </div>
            </CardContent>
        </Card>
    );
};
