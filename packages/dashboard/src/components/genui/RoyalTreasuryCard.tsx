"use client";

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Coins, Zap, ArrowUpRight, TrendingUp } from "lucide-react";

export const RoyalTreasuryCard = () => {
    return (
        <Card className="bg-gradient-to-br from-amber-50 to-orange-50 border-orange-200/50 shadow-lg hover:shadow-orange-200/50 transition-all duration-300">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-bold text-amber-800 flex items-center gap-2">
                    <Coins className="w-5 h-5 text-amber-500" />
                    ROYAL TREASURY
                </CardTitle>
                <Badge className="bg-amber-100 text-amber-800 hover:bg-amber-200 border-amber-200">
                    Active
                </Badge>
            </CardHeader>
            <CardContent>
                <div className="space-y-6">
                    {/* Gold Balance */}
                    <div>
                        <div className="flex items-center justify-between mb-1">
                            <span className="text-xs font-semibold text-amber-600/70 uppercase">Total Assets</span>
                            <span className="text-xs font-bold text-green-600 flex items-center gap-1">
                                <TrendingUp className="w-3 h-3" /> +12.5%
                            </span>
                        </div>
                        <div className="text-3xl font-black text-slate-800">
                            $ 4,520,000
                        </div>
                        <p className="text-xs text-amber-600/60 font-medium mt-1">
                            ≈ 452,000 AFO Tokens
                        </p>
                    </div>

                    {/* Mana Reserves */}
                    <div className="space-y-2">
                        <div className="flex items-center justify-between text-xs text-slate-600">
                             <span className="flex items-center gap-1"><Zap className="w-3 h-3 text-purple-500"/> Mana Reserves</span>
                             <span className="font-bold">92%</span>
                        </div>
                        <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                             <div className="h-full bg-gradient-to-r from-purple-500 to-blue-500 w-[92%] rounded-full" />
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="grid grid-cols-2 gap-3 pt-2">
                        <Button className="w-full bg-amber-500 hover:bg-amber-600 text-white shadow-amber-200 font-bold">
                            Deposit
                        </Button>
                         <Button variant="outline" className="w-full border-amber-200 text-amber-700 hover:bg-amber-50 font-bold">
                            <ArrowUpRight className="w-4 h-4 mr-1"/> Transfer
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};
