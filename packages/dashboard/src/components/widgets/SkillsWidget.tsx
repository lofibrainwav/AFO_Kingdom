'use client';
import { GenericWidget } from './GenericWidget';

export const SkillsWidget = () => {
  return (
    <GenericWidget 
      title="능력 목록 (Skills)" 
      endpoint="/api/skills" 
      valueKey="total" 
      subText="Active MCP Skills"
      className="border-blue-500/30"
    />
  );
};
