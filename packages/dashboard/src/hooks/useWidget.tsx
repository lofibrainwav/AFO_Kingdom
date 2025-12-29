'use client';
import useSSE from '@/hooks/useSSE';

interface WidgetProps {
  title: string;
  endpoint: string;
  valueKey: string;
  subText?: string;
}

export const useWidget = ({ endpoint, valueKey }: { endpoint: string; valueKey: string }) => {
  const { data } = useSSE(endpoint);
  // Support nested keys like 'organs' or just direct value
  // Simple accessor for Minimal PR
  if (!data) return 0;
  return data[valueKey] ?? 0;
};
