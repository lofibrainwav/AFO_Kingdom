'use client';
import React from 'react';
import { useWidget } from '@/hooks/useWidget';

interface GenericWidgetProps {
  title: string;
  endpoint: string;
  valueKey: string;
  subText?: string;
  className?: string;
}

export const GenericWidget = ({ title, endpoint, valueKey, subText, className }: GenericWidgetProps) => {
  const value = useWidget({ endpoint, valueKey });
  
  return (
    <div className={`glass-card p-4 sm:p-6 rounded-xl shadow-lg transition-all hover:scale-105 border border-white/10 bg-white/5 backdrop-blur-lg ${className || ''}`}>
      <h2 className="text-lg sm:text-xl text-emerald-400 font-bold mb-2">{title}</h2>
      <p className="text-2xl sm:text-3xl text-white font-mono">{value}</p>
      {subText && <p className="text-sm text-gray-400 mt-2">{subText}</p>}
    </div>
  );
};
