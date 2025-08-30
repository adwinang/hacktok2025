import { AuditReports, AuditReportsResponseSchema } from "@/types/audit_report";

export async function getAuditReportsBySource(sourceId: string): Promise<AuditReports> {
    try {
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/audit-report/source/${sourceId}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to fetch audit reports for source ${sourceId}: ${response.status}`
            );
        }

        const data = await response.json();
        const parsed = AuditReportsResponseSchema.parse(data);
        return parsed.audit_reports;
    } catch (error: unknown) {
        console.error("Error fetching audit reports by source:", error);
        return [];
    }
}


