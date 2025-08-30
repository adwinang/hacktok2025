"use client";
import dynamic from "next/dynamic";

const AddSourceDialog = dynamic(
    () => import("@/components/custom/sources-table/add-source-dialog"),
    { ssr: false }
);

export default function AddSourceButton() {
    return <AddSourceDialog />;
}


