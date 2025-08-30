"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import AuditReportDialog from "@/components/custom/audit-report-dialog";
import { AuditReport, AuditReports, AuditReportStatus } from "@/types/audit_report";
import { AlertTriangle, CheckCircle, Clock, XCircle } from "lucide-react";
import { format } from "date-fns";

function getAuditStatusConfig(status: AuditReportStatus) {
    switch (status) {
        case "pending":
            return {
                icon: <Clock className="h-4 w-4" />,
                variant: "secondary" as const,
                className: "text-yellow-700 bg-yellow-50 border-yellow-200",
            };
        case "verified":
            return {
                icon: <CheckCircle className="h-4 w-4" />,
                variant: "secondary" as const,
                className: "text-green-700 bg-green-50 border-green-200",
            };
        case "dismissed":
            return {
                icon: <XCircle className="h-4 w-4" />,
                variant: "secondary" as const,
                className: "text-gray-700 bg-gray-50 border-gray-200",
            };
        default:
            return {
                icon: <AlertTriangle className="h-4 w-4" />,
                variant: "secondary" as const,
                className: "text-red-700 bg-red-50 border-red-200",
            };
    }
}

function getFeatureStatusClasses(status: string) {
    if (status === "pending") return "text-yellow-700 bg-yellow-50 border border-yellow-200 px-1.5 py-0.5 rounded";
    if (status === "pass") return "text-green-700 bg-green-50 border border-green-200 px-1.5 py-0.5 rounded";
    if (status === "warning") return "text-orange-700 bg-orange-50 border border-orange-200 px-1.5 py-0.5 rounded";
    if (status === "critical") return "text-red-700 bg-red-50 border border-red-200 px-1.5 py-0.5 rounded";
    return "text-muted-foreground";
}

export default function SourceAuditReportsClientView({
    auditReports,
    featureNames,
}: {
    auditReports: AuditReports;
    featureNames?: Record<string, string>;
}) {
    const [selectedReport, setSelectedReport] = useState<AuditReport | null>(null);
    const [dialogOpen, setDialogOpen] = useState(false);

    const openDialog = (report: AuditReport) => {
        setSelectedReport(report);
        setDialogOpen(true);
    };

    return (
        <>
            {auditReports.length === 0 ? (
                <div className="text-sm text-muted-foreground">No audit reports found.</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                    {auditReports.map((report) => (
                        <button
                            key={report.id}
                            onClick={() => openDialog(report)}
                            className="text-left"
                        >
                            <Card className="p-4 space-y-2 hover:bg-accent/50 transition-colors">
                                <div className="flex items-center justify-between">
                                    {(() => {
                                        const config = getAuditStatusConfig(report.status);
                                        return (
                                            <Badge variant={config.variant} className={`flex items-center gap-1 capitalize ${config.className}`}>
                                                {config.icon}
                                                <span className="capitalize">{report.status}</span>
                                            </Badge>
                                        );
                                    })()}
                                    <span className="text-xs text-muted-foreground">
                                        {Math.round(report.confidence * 100)}% confidence
                                    </span>
                                </div>
                                <div className="text-sm">
                                    <div>
                                        <span className="text-muted-foreground">Feature:</span> {featureNames?.[report.feature_id] ?? report.feature_id}
                                    </div>
                                    <div className="mt-1">
                                        <span className="text-muted-foreground mr-1">Change:</span>
                                        <span className={getFeatureStatusClasses(report.original_status)}>{report.original_status}</span>
                                        <span className="mx-1">→</span>
                                        <span className={getFeatureStatusClasses(report.status_change_to)}>{report.status_change_to}</span>
                                    </div>
                                    <div className="mt-1 text-xs text-muted-foreground">
                                        Created: {format(new Date(report.created_at), "MM/dd/yyyy HH:mm")}
                                    </div>
                                </div>
                                <p className="text-sm text-muted-foreground line-clamp-3">{report.reason}</p>
                            </Card>
                        </button>
                    ))}
                </div>
            )}

            <AuditReportDialog
                report={selectedReport}
                open={dialogOpen}
                onOpenChange={(open) => {
                    setDialogOpen(open);
                    if (!open) setSelectedReport(null);
                }}
            />
        </>
    );
}


