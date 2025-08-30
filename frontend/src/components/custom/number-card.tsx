"use client";

import Link from "next/link";
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
  href?: string; // optional: make the number clickable
}

export function NumberCard({
  title,
  description,
  value,
  footerText,
  subFooterText,
  href,
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
          {href ? (
            <Link
              href={href}
              className="text-6xl font-bold text-muted-foreground/80 tracking-tight hover:text-muted-foreground underline-offset-4 hover:underline focus:outline-none focus:ring-2 focus:ring-ring rounded"
            >
              {formatNumber(value)}
            </Link>
          ) : (
            <span className="text-6xl font-bold text-muted-foreground/80 tracking-tight">
              {formatNumber(value)}
            </span>
          )}
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
