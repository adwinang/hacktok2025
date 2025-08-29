"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface NumberCardProps {
  title: string;
  description: string;
  value: number;
  footerText: string;
  subFooterText?: string;
}

export function NumberCard({
  title,
  description,
  value,
  footerText,
  subFooterText,
}: NumberCardProps) {
  // Format large numbers (e.g., 1,234 or 1.2K)
  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1).replace(/\.0$/, "") + "M";
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1).replace(/\.0$/, "") + "K";
    }
    return num.toLocaleString();
  };

  return (
    <Card className="flex flex-col">
      <CardHeader className="items-center pb-0">
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <div className="flex items-center justify-center h-full min-h-[200px]">
          <span className="text-6xl font-bold text-muted-foreground/80 tracking-tight">
            {formatNumber(value)}
          </span>
        </div>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm">
        <div className="flex items-center gap-2 leading-none font-medium">
          {footerText}
        </div>
        {subFooterText && (
          <div className="text-muted-foreground leading-none">
            {subFooterText}
          </div>
        )}
      </CardFooter>
    </Card>
  );
}
