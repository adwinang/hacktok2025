import { Sources } from "@/types/source";
import { columns } from "./source-columns";
import { DataTable } from "../features-table/data-table";

interface SourcesTableProps {
    data: Sources;
}

export default function SourcesTable({ data }: SourcesTableProps) {
    return <DataTable data={data} columns={columns} />;
}


