"use client";
import { ColumnDef } from "@tanstack/react-table";
import { Feature } from "@/types/feature";
import { DataTableColumnHeader } from "./data-table-column-header";
import { formatDate } from "date-fns";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, Ban, Check, Clock } from "lucide-react";

export const columns: ColumnDef<Feature>[] = [
  {
    id: "id",
    accessorKey: "id",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="ID" />
    ),
    cell: ({ row }) => (
      <div className="text-sm font-mono text-muted-foreground truncate">
        {row.getValue("id")}
      </div>
    ),
    enableSorting: false,
    size: 80,
    minSize: 80,
    maxSize: 80,
  },
  {
    accessorKey: "name",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Name" />
    ),
    cell: ({ row }) => (
      <div className="break-words whitespace-normal">
        <span className="font-medium">{row.getValue("name")}</span>
      </div>
    ),
    enableSorting: false,
    enableHiding: false,
    size: 280,
    minSize: 280,
    maxSize: 280,
  },
  {
    id: "description",
    accessorKey: "description",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Description" />
    ),
    cell: ({ row }) => (
      <div className="break-words whitespace-normal text-sm text-muted-foreground leading-relaxed">
        {row.getValue("description")}
      </div>
    ),
    enableSorting: false,
    size: undefined,
    minSize: undefined,
    maxSize: undefined,
  },
  {
    accessorKey: "tags",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Tags" />
    ),
    cell: ({ row }) => {
      const tags = row.getValue("tags") as string[] | undefined;
      return (
        <div className="flex flex-wrap gap-1.5">
          {tags && tags.length > 0 ? (
            tags.map((tag) => (
              <Badge key={`${row.id}-${tag}`} variant="secondary">
                {tag}
              </Badge>
            ))
          ) : (
            <span className="text-xs text-muted-foreground">—</span>
          )}
        </div>
      );
    },
    enableSorting: false,
    size: 200,
    minSize: 160,
    maxSize: 280,
    filterFn: (row, id, value) => {
      const selected = (value as string[]) ?? [];
      if (selected.length === 0) return true;
      const rowTags = (row.getValue(id) as string[] | undefined) ?? [];
      return selected.some((tag) => rowTags.includes(tag));
    },
  },
  {
    accessorKey: "created_at",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Created" />
    ),
    cell: ({ row }) => (
      <div className="text-sm whitespace-nowrap">
        {formatDate(row.getValue("created_at"), "MM/dd/yyyy")}
      </div>
    ),
    enableSorting: false,
    size: 100,
    minSize: 100,
    maxSize: 100,
  },
  {
    accessorKey: "updated_at",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Updated" />
    ),
    cell: ({ row }) => (
      <div className="text-sm whitespace-nowrap">
        {formatDate(row.getValue("updated_at"), "MM/dd/yyyy")}
      </div>
    ),
    enableSorting: false,
    size: 100,
    minSize: 100,
    maxSize: 100,
  },
  {
    accessorKey: "status",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Status" />
    ),
    cell: ({ row }) => {
      const status = row.getValue("status") as string;

      const getStatusConfig = (status: string) => {
        switch (status) {
          case "pending":
            return {
              icon: <Clock className="h-3 w-3" />,
              variant: "secondary" as const,
              className: "text-yellow-700 bg-yellow-50 border-yellow-200",
            };
          case "pass":
            return {
              icon: <Check className="h-3 w-3" />,
              variant: "secondary" as const,
              className: "text-green-700 bg-green-50 border-green-200",
            };
          case "warning":
            return {
              icon: <AlertTriangle className="h-3 w-3" />,
              variant: "secondary" as const,
              className: "text-orange-700 bg-orange-50 border-orange-200",
            };
          default:
            return {
              icon: <Ban className="h-3 w-3" />,
              variant: "secondary" as const,
              className: "text-red-700 bg-red-50 border-red-200",
            };
        }
      };

      const config = getStatusConfig(status);

      return (
        <Badge
          variant={config.variant}
          className={`flex items-center gap-1 text-xs font-medium ${config.className}`}
        >
          {config.icon}
          <span className="capitalize">{status}</span>
        </Badge>
      );
    },
    enableSorting: false,
    size: 120,
    minSize: 120,
    maxSize: 120,
    filterFn: (row, id, value) => {
      if (!value || value.length === 0) return true;
      return value.includes(row.getValue(id));
    },
  },
];
