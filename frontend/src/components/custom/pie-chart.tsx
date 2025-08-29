"use client";

import { TrendingUp } from "lucide-react";
import { Pie, PieChart, Cell } from "recharts";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { PieChartData } from "@/helpers/transformToChart";

interface PieChartProps {
  title: string;
  description: string;
  header?: string;
  subheader?: string;
  chartData: PieChartData["data"];
  dataKey: PieChartData["dataKey"];
  nameKey: PieChartData["nameKey"];
  chartConfig: PieChartData["chartConfig"];
}

export function ChartPieLabel({
  title,
  description,
  header,
  subheader,
  dataKey,
  nameKey,
  chartData,
  chartConfig,
}: PieChartProps) {
  return (
    <Card className="flex flex-col">
      <CardHeader className="items-center pb-0">
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer
          config={chartConfig}
          className="[&_.recharts-pie-label-text]:fill-foreground mx-auto aspect-square max-h-[250px] pb-0"
        >
          <PieChart>
            <ChartTooltip content={<ChartTooltipContent hideLabel />} />
            <Pie data={chartData} dataKey={dataKey} label nameKey={nameKey}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm">
        <div className="flex items-center gap-2 leading-none font-medium">
          {header} <TrendingUp className="h-4 w-4" />
        </div>
        <div className="text-muted-foreground leading-none">{subheader}</div>
      </CardFooter>
    </Card>
  );
}
