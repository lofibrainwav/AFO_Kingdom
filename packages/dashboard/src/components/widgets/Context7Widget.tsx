'use client';
import { GenericWidget } from './GenericWidget';

export const Context7Widget = () => {
  return (
    <GenericWidget 
      title="Context7 지식" 
      endpoint="/api/context7/list" 
      valueKey="items_loaded" 
      subText="SSOT Documents Loaded"
      className="border-purple-500/30"
    />
  );
};
