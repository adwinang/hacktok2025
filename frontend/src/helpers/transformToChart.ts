import { ChartConfig } from "@/components/ui/chart";
import { Features } from "@/types/feature";

export interface PieChartData {
  dataKey: string;
  nameKey: string;
  data: {
    name: string;
    value: number;
    fill: string;
  }[];
  chartConfig: ChartConfig;
}

export function transformFeaturesToChart(features: Features): PieChartData {
  const statusCount = {
    pending: 0,
    pass: 0,
    warning: 0,
    critical: 0,
  };

  const dataKey = "value";
  const nameKey = "name";

  features.forEach((feature) => {
    statusCount[feature.status]++;
  });

  // Color mapping for each status
  const colorMap = {
    pending: "oklch(0.646 0.222 41.116)", // Yellow/Orange
    pass: "oklch(0.6 0.118 184.704)", // Blue
    warning: "oklch(0.398 0.07 227.392)", // Dark Blue
    critical: "oklch(0.828 0.189 84.429)", // Light Green
  };

  const data = Object.entries(statusCount).map(([name, value]) => ({
    name,
    value,
    fill: colorMap[name as keyof typeof colorMap] || "oklch(0.5 0.1 180)", // Fallback color
  }));

  const chartConfig = {
    pending: {
      label: "Pending",
      color: colorMap.pending,
    },
    pass: {
      label: "Pass",
      color: colorMap.pass,
    },
    warning: {
      label: "Warning",
      color: colorMap.warning,
    },
    critical: {
      label: "Critical",
      color: colorMap.critical,
    },
  } satisfies ChartConfig;

  return {
    dataKey,
    nameKey,
    data,
    chartConfig,
  };
}
