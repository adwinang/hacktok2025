import { getAuditReportsBySource } from "@/services/auditReportService";
import SourceAuditReportsClientView from "./client-view";

export default async function SourceAuditReportsPage({
    params,
}: {
    params: Promise<{ sourceId: string }>;
}) {
    const { sourceId } = await params;
    const auditReports = await getAuditReportsBySource(sourceId);
    const sortedReports = [...auditReports].sort(
        (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    );

    // Build a map of feature_id -> feature.name for display
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    const featureIds = Array.from(new Set(sortedReports.map((r) => r.feature_id)));
    const featureNames: Record<string, string> = {};

    await Promise.all(
        featureIds.map(async (id) => {
            try {
                const res = await fetch(`${apiUrl}/features/${id}`, { cache: "no-store" });
                if (!res.ok) return;
                const data = await res.json();
                const feature = data.feature || data;
                if (feature && typeof feature.name === "string") {
                    featureNames[id] = feature.name;
                }
            } catch {
                // ignore per-feature fetch failures
            }
        })
    );

    return (
        <div className="space-y-4">
            <h2 className="text-xl font-semibold">Audit Reports for Source</h2>
            <SourceAuditReportsClientView auditReports={sortedReports} featureNames={featureNames} />
        </div>
    );
}


