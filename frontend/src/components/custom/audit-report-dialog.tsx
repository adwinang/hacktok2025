"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import {
  AlertTriangle,
  CheckCircle,
  Clock,
  XCircle,
  ExternalLink,
  Loader2,
} from "lucide-react";
import { AuditReport, AuditReportStatus } from "@/types/audit_report";
import {
  Source,
  SourcesResponseSchema,
  SourceIdsRequest,
} from "@/types/source";
import { Feature } from "@/types/feature";

interface AuditReportDialogProps {
  report: AuditReport | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function AuditReportDialog({
  report,
  open,
  onOpenChange,
}: AuditReportDialogProps) {
  const [feature, setFeature] = useState<Feature | null>(null);
  const [loadingFeature, setLoadingFeature] = useState(false);
  const [featureError, setFeatureError] = useState<string | null>(null);
  const [sources, setSources] = useState<Source[]>([]);
  const [loadingSources, setLoadingSources] = useState(false);
  const [sourcesError, setSourcesError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<
    "verify" | "dismiss" | null
  >(null);

  // Fetch sources when dialog opens and report changes
  useEffect(() => {
    if (open && report && report.source_ids.length > 0) {
      fetchSources(report.source_ids);
      fetchFeature(report.feature_id);
    }
  }, [open, report]);

  const fetchFeature = async (featureId: string) => {
    setLoadingFeature(true);
    setFeatureError(null);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/features/${featureId}`,
        {
          headers: {
            "Access-Control-Allow-Origin": "*",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch feature: ${response.statusText}`);
      }

      const data = await response.json();
      // Extract the feature from the nested response structure
      const featureData = data.feature || data;
      setFeature(featureData);
      console.log("Feature fetched successfully", data);
    } catch (error) {
      setFeatureError(
        error instanceof Error ? error.message : "Failed to load feature"
      );
      setFeature(null);
    } finally {
      setLoadingFeature(false);
    }
  };

  const fetchSources = async (sourceIds: string[]) => {
    setLoadingSources(true);
    setSourcesError(null);

    try {
      const requestBody: SourceIdsRequest = { source_ids: sourceIds };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/sources/ids`,
        {
          method: "POST",
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch sources: ${response.statusText}`);
      }

      const data = await response.json();
      const validatedData = SourcesResponseSchema.parse(data);
      setSources(validatedData.sources);
    } catch (error) {
      setSourcesError(
        error instanceof Error ? error.message : "Failed to load sources"
      );
      setSources([]);
    } finally {
      setLoadingSources(false);
    }
  };

  const handleVerify = async () => {
    if (!report) return;

    setActionLoading("verify");
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/audit-report/${report.id}/verify`,
        {
          method: "POST",
          headers: {
            "Access-Control-Allow-Origin": "*",
          },
        }
      );

      if (!response.ok) {
        throw new Error(
          `Failed to verify audit report: ${response.statusText}`
        );
      }

      toast.success(
        `Audit report has been verified successfully. ${
          report.status_change_to !== "pass" &&
          "Feature creation request and audit report will be sent to the team."
        }`
      );

      onOpenChange(false);
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : "Failed to verify audit report"
      );
    } finally {
      setActionLoading(null);
    }
  };

  const handleDismiss = async () => {
    if (!report) return;

    setActionLoading("dismiss");
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/audit-report/${report.id}/dismiss`,
        {
          method: "POST",
          headers: {
            "Access-Control-Allow-Origin": "*",
          },
        }
      );

      if (!response.ok) {
        throw new Error(
          `Failed to dismiss audit report: ${response.statusText}`
        );
      }

      toast.success("Audit report has been dismissed successfully.");

      onOpenChange(false);
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Failed to dismiss audit report"
      );
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusConfig = (status: AuditReportStatus) => {
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
  };

  if (!report) return null;

  const statusConfig = getStatusConfig(report.status);
  const confidencePercentage = Math.round(report.confidence);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="min-w-[50vw] max-h-[80vh] overflow-hidden">
        <DialogHeader>
          <DialogTitle className="flex items-center justify-between">
            <span>Audit Report Details</span>
            <Badge
              variant={statusConfig.variant}
              className={`flex items-center gap-1 ${statusConfig.className} mr-4`}
            >
              {statusConfig.icon}
              <span className="capitalize">{report.status}</span>
            </Badge>
          </DialogTitle>
        </DialogHeader>

        <div className="grid grid-cols-12 gap-6 max-h-[70vh] overflow-hidden h-full">
          {/* Sources Sidebar */}
          <div className="col-span-4 border-r pr-4">
            <h3 className="font-semibold mb-3 text-sm uppercase tracking-wide text-muted-foreground">
              Sources ({report.source_ids.length})
            </h3>

            <div className="space-y-2 max-h-[50vh] overflow-y-auto">
              {loadingSources && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Loading sources...
                </div>
              )}

              {sourcesError && (
                <div className="p-2 bg-red-50 border border-red-200 rounded text-red-600 text-xs">
                  {sourcesError}
                </div>
              )}

              {sources.map((source) => (
                <div
                  key={source.id}
                  className="p-2 border rounded-lg bg-card hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-mono text-muted-foreground break-all">
                        {source.source_url}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        Added:{" "}
                        {new Date(source.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <a
                      href={source.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-shrink-0 p-1 hover:bg-accent rounded"
                    >
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  </div>
                </div>
              ))}

              {!loadingSources && !sourcesError && sources.length === 0 && (
                <div className="text-xs text-muted-foreground text-center py-4">
                  No sources found
                </div>
              )}
            </div>
          </div>

          {/* Main Content */}
          <div className="col-span-8">
            <div className="space-y-4 max-h-[50vh] overflow-y-auto">
              {/* Feature Details */}
              <div className="space-y-2">
                <h3 className="font-semibold text-sm uppercase tracking-wide text-muted-foreground">
                  Feature Details
                </h3>

                {loadingFeature && (
                  <div className="flex items-center gap-2 p-3 bg-accent/50 rounded-lg">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span className="text-sm text-muted-foreground">
                      Loading feature details...
                    </span>
                  </div>
                )}

                {featureError && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex items-center gap-2">
                      <XCircle className="h-4 w-4 text-red-600" />
                      <span className="text-sm text-red-600">
                        {featureError}
                      </span>
                    </div>
                  </div>
                )}

                {!loadingFeature && !featureError && feature && (
                  <div className="space-y-3">
                    <div className="p-3 bg-accent/50 rounded-lg">
                      <h4 className="font-semibold text-xs uppercase tracking-wide text-muted-foreground mb-2">
                        Name
                      </h4>
                      <p className="text-sm font-medium">{feature.name}</p>
                    </div>

                    <div className="p-3 bg-accent/50 rounded-lg">
                      <h4 className="font-semibold text-xs uppercase tracking-wide text-muted-foreground mb-2">
                        Description
                      </h4>
                      <div className="max-h-32 overflow-y-auto">
                        <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                          {feature.description}
                        </p>
                      </div>
                    </div>

                    {feature.tags && feature.tags.length > 0 && (
                      <div className="p-3 bg-accent/50 rounded-lg">
                        <h4 className="font-semibold text-xs uppercase tracking-wide text-muted-foreground mb-2">
                          Tags
                        </h4>
                        <div className="flex flex-wrap gap-1">
                          {feature.tags.map((tag, index) => (
                            <Badge
                              key={index}
                              variant="secondary"
                              className="text-xs"
                            >
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {!loadingFeature && !featureError && !feature && (
                  <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                    <span className="text-sm text-gray-600">
                      No feature details available
                    </span>
                  </div>
                )}
              </div>

              {/* Status Change */}
              <div className="space-y-2">
                <h3 className="font-semibold text-sm uppercase tracking-wide text-muted-foreground">
                  Status Change
                </h3>
                <div className="flex items-center gap-2 p-3 bg-accent/50 rounded-lg">
                  <Badge variant="outline" className="text-xs">
                    {report.original_status}
                  </Badge>
                  <span className="text-muted-foreground">→</span>
                  <Badge variant="outline" className="text-xs">
                    {report.status_change_to}
                  </Badge>
                  <div className="ml-auto text-xs text-muted-foreground">
                    {confidencePercentage}% confidence
                  </div>
                </div>
              </div>

              {/* Reason */}
              <div className="space-y-2">
                <h3 className="font-semibold text-sm uppercase tracking-wide text-muted-foreground">
                  Reason
                </h3>
                <div className="p-3 bg-card border rounded-lg">
                  <p className="text-sm leading-relaxed">{report.reason}</p>
                </div>
              </div>

              {/* Metadata */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <h3 className="font-semibold text-xs uppercase tracking-wide text-muted-foreground">
                    Feature ID
                  </h3>
                  <p
                    className="font-mono text-xs bg-accent/20 p-2 rounded truncate"
                    title={report.feature_id}
                  >
                    {report.feature_id}
                  </p>
                </div>

                <div className="space-y-2">
                  <h3 className="font-semibold text-xs uppercase tracking-wide text-muted-foreground">
                    Created
                  </h3>
                  <p className="text-xs p-2">
                    {new Date(report.created_at).toLocaleString()}
                  </p>
                </div>
              </div>

              {report.needs_action && (
                <div className="flex items-center gap-2 p-3 bg-orange-50 border border-orange-200 rounded-lg mb-1">
                  <AlertTriangle className="h-4 w-4 text-orange-600" />
                  <span className="text-sm font-medium text-orange-700">
                    Action Required
                  </span>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            {report.status === "pending" && (
              <div className="flex justify-end gap-3 pt-4 mt-4 border-t mb-1">
                <Button
                  variant="outline"
                  onClick={handleDismiss}
                  disabled={actionLoading !== null}
                  className="text-gray-600 border-gray-300 hover:bg-gray-50"
                >
                  {actionLoading === "dismiss" && (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  )}
                  Dismiss
                </Button>
                <Button
                  onClick={handleVerify}
                  disabled={actionLoading !== null}
                  className="bg-green-600 hover:bg-green-700 text-white"
                >
                  {actionLoading === "verify" && (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  )}
                  Verify
                </Button>
              </div>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
