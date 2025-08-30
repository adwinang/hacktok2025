"use client";
import { ColumnDef } from "@tanstack/react-table";
import { Source } from "@/types/source";
import { DataTableColumnHeader } from "../features-table/data-table-column-header";
import { Badge } from "@/components/ui/badge";
import { format } from "date-fns";
import Link from "next/link";

export const columns: ColumnDef<Source>[] = [
    {
        accessorKey: "source_url",
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Source URL" />
        ),
        cell: ({ row }) => (
            <div className="break-words whitespace-normal">
                <span className="font-medium break-all">
                    {row.getValue("source_url")}
                </span>
            </div>
        ),
        enableSorting: false,
        size: 420,
        minSize: 420,
        maxSize: 420,
    },
    {
        accessorKey: "tags",
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Tags" />
        ),
        cell: ({ row }) => {
            const tags: string[] | null = row.getValue("tags");
            return (
                <div className="flex flex-wrap gap-1.5">
                    {tags && tags.length > 0 ? (
                        tags.map((tag) => (
                            <Badge key={`${row.id}-${tag}`} variant="secondary">
                                {tag}
                            </Badge>
                        ))
                    ) : (
                        <span className="text-sm text-muted-foreground">-</span>
                    )}
                </div>
            );
        },
        enableSorting: false,
        size: 220,
        minSize: 220,
        maxSize: 220,
    },
    {
        accessorKey: "created_at",
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Created" />
        ),
        cell: ({ row }) => {
            const value: Date | string = row.getValue("created_at");
            const date = value instanceof Date ? value : new Date(value);
            return <div className="text-sm whitespace-nowrap">{format(date, "MM/dd/yyyy")}</div>;
        },
        enableSorting: false,
        size: 120,
        minSize: 120,
        maxSize: 120,
    },
    {
        accessorKey: "updated_at",
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Updated" />
        ),
        cell: ({ row }) => {
            const value: Date | string | null = row.getValue("updated_at");
            if (!value) return <div className="text-sm whitespace-nowrap">-</div>;
            const date = value instanceof Date ? value : new Date(value);
            return <div className="text-sm whitespace-nowrap">{format(date, "MM/dd/yyyy")}</div>;
        },
        enableSorting: false,
        size: 120,
        minSize: 120,
        maxSize: 120,
    },
    {
        id: "audit_reports",
        header: ({ column }) => (
            <DataTableColumnHeader column={column} title="Audit Reports" />
        ),
        cell: ({ row }) => {
            const sourceId = row.original.id;
            return (
                <Link
                    href={`/sources/${sourceId}/audit-reports`}
                    className="text-sm text-primary hover:underline"
                >
                    View reports
                </Link>
            );
        },
        enableSorting: false,
        size: 140,
        minSize: 140,
        maxSize: 160,
    },
];


