'use client';
import { GenericWidget } from './GenericWidget';

export const SyncWidget = () => {
  // Using health status as proxy for sync 'Green Light' for now
  return (
    <GenericWidget 
      title="동기화 상태 (Sync)" 
      endpoint="/api/health" 
      valueKey="status" 
      subText="Remote/Local Twin Truth"
      className="border-green-500/50"
    />
  );
};
