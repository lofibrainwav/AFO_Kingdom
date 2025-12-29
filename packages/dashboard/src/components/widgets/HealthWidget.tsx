'use client';
import { GenericWidget } from './GenericWidget';

export const HealthWidget = () => {
  return (
    <GenericWidget 
      title="오장육부 건강도" 
      endpoint="/api/health/comprehensive" 
      valueKey="organs_v2" 
      subText="11 Critical Organs Active" // Static for now or derive
      className="border-emerald-500/30"
    />
  );
};
