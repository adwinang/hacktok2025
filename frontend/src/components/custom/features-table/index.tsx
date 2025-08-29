import { Features } from "@/types/feature";
import { columns } from "./column";
import { DataTable } from "./data-table";

interface FeaturesTableProps {
  data: Features;
}

export default function FeaturesTable({ data }: FeaturesTableProps) {
  // IMPORTANT TODO: This is a temporary solution to show the table with more data
  // This should be removed once the backend is implemented
  return <DataTable data={data} columns={columns} />;
  // return <p>TODO</p>;
}
