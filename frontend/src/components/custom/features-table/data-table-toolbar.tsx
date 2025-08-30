"use client";

import { Table } from "@tanstack/react-table";

import { DataTableFacetedFilter } from "./data-table-faceted-filter";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { DataTableViewOptions } from "./data-table-view-options";
import { X } from "lucide-react";
import { statuses } from "./data/statuses";

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
}

export function DataTableToolbar<TData>({
  table,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;
  const allColumns = table.getAllColumns();
  const nameColumn = allColumns.find((c) => c.id === "name");
  const urlColumn = allColumns.find((c) => c.id === "source_url");
  const statusColumn = allColumns.find((c) => c.id === "status");
  const tagsColumn = allColumns.find((c) => c.id === "tags");
  const filterableColumn = nameColumn ?? urlColumn;
  const placeholder = nameColumn
    ? "Filter by name"
    : urlColumn
      ? "Filter by URL"
      : "Search";

  // Build tag options dynamically from the table data
  const tagOptions = Array.from(
    new Set(
      table
        .getPreFilteredRowModel()
        .flatRows.flatMap((row) =>
          ((row.getValue("tags") as string[] | undefined) ?? []).filter(Boolean)
        )
    )
  ).map((tag) => ({ label: tag, value: tag }));

  return (
    <div className="flex items-center justify-between w-full overflow-x-scroll pb-4">
      <div className="flex flex-1 items-center space-x-2 p-1">
        <Input
          placeholder={placeholder}
          value={(filterableColumn?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            filterableColumn?.setFilterValue(event.target.value)
          }
          className="h-8 w-[150px] lg:w-[250px]"
        />
        {statusColumn && (
          <DataTableFacetedFilter
            column={statusColumn}
            title="Status"
            options={statuses}
          />
        )}
        {tagsColumn && tagOptions.length > 0 && (
          <DataTableFacetedFilter
            column={tagsColumn}
            title="Tags"
            options={tagOptions}
          />
        )}
        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => table.resetColumnFilters()}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <X />
          </Button>
        )}
      </div>
      <div className="flex space-x-2">
        <DataTableViewOptions table={table} />
      </div>
    </div>
  );
}
