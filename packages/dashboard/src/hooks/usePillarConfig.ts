import useSWR from "swr";

export type PillarNode = {
  id: string;
  name: string;
  role: string;
  weight: number;
  color: string;
};

export type PillarConfig = {
  pillars: PillarNode[];
  trinity_formula: string;
  auto_run_condition: string;
};

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export function usePillarConfig() {
  const { data, error, isLoading } = useSWR<PillarConfig>("/api/5pillars/config", fetcher);

  return {
    config: data,
    isLoading,
    isError: error,
  };
}
