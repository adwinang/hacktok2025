"use client";

import { useEffect, useMemo, useReducer, useRef, useState } from "react";
import { Card } from "../ui/card";
import { Badge } from "../ui/badge";
import { AlertTriangle, CheckCircle, Clock, XCircle } from "lucide-react";
import {
  AuditReports,
  AuditReport,
  AuditReportStreamEventSchema,
  AuditReportStatus,
} from "@/types/audit_report";
import AuditReportDialog from "./audit-report-dialog";
import { MultiSelect } from "./multi-select";
import { cn } from "@/lib/utils";

type AuditReportsState = {
  auditReports: AuditReports;
  loading: boolean;
  error: string | null;
};

type AuditReportsAction =
  | { type: "LOADING" }
  | { type: "SET_INITIAL_AUDIT_REPORTS"; payload: AuditReports }
  | { type: "ADD_AUDIT_REPORT"; payload: AuditReport }
  | {
      type: "UPDATE_AUDIT_REPORT";
      payload: { auditReportId: string; auditReportData: AuditReport };
    }
  | { type: "DELETE_AUDIT_REPORT"; payload: { auditReportId: string } }
  | { type: "ERROR"; payload: string }
  | { type: "RESET_ERROR" };

function auditReportsReducer(
  state: AuditReportsState,
  action: AuditReportsAction
): AuditReportsState {
  switch (action.type) {
    case "LOADING":
      return { ...state, loading: true, error: null };

    case "SET_INITIAL_AUDIT_REPORTS":
      return {
        auditReports: action.payload,
        loading: false,
        error: null,
      };

    case "ADD_AUDIT_REPORT":
      return {
        ...state,
        auditReports: [action.payload, ...state.auditReports],
      };

    case "UPDATE_AUDIT_REPORT":
      const { auditReportId, auditReportData } = action.payload;
      const updatedReports = state.auditReports.map((report) =>
        report.id === auditReportId ? auditReportData : report
      );
      return {
        ...state,
        auditReports: updatedReports,
      };

    case "DELETE_AUDIT_REPORT":
      const filteredReports = state.auditReports.filter(
        (report) => report.id !== action.payload.auditReportId
      );
      return {
        ...state,
        auditReports: filteredReports,
      };

    case "ERROR":
      return {
        ...state,
        loading: false,
        error: action.payload,
      };

    case "RESET_ERROR":
      return {
        ...state,
        error: null,
      };

    default:
      return state;
  }
}

interface AuditReportItemProps {
  report: AuditReport;
  onClick: () => void;
}

function AuditReportItem({ report, onClick }: AuditReportItemProps) {
  const getStatusConfig = (status: AuditReportStatus) => {
    switch (status) {
      case "pending":
        return {
          icon: <Clock className="h-3 w-3" />,
          variant: "secondary" as const,
          className: "text-yellow-700 bg-yellow-50 border-yellow-200",
        };
      case "verified":
        return {
          icon: <CheckCircle className="h-3 w-3" />,
          variant: "secondary" as const,
          className: "text-green-700 bg-green-50 border-green-200",
        };
      case "dismissed":
        return {
          icon: <XCircle className="h-3 w-3" />,
          variant: "secondary" as const,
          className: "text-gray-700 bg-gray-50 border-gray-200",
        };
      default:
        return {
          icon: <AlertTriangle className="h-3 w-3" />,
          variant: "secondary" as const,
          className: "text-red-700 bg-red-50 border-red-200",
        };
    }
  };

  const statusConfig = getStatusConfig(report.status);
  const confidencePercentage = Math.round(report.confidence);

  return (
    <div
      className="flex flex-col items-start rounded-lg p-3 border bg-card hover:bg-accent/50 transition-colors cursor-pointer"
      onClick={onClick}
    >
      <div className="flex items-center justify-between w-full mb-2">
        <Badge
          variant={statusConfig.variant}
          className={`flex items-center gap-1 text-xs font-medium ${statusConfig.className}`}
        >
          {statusConfig.icon}
          <span className="capitalize">{report.status}</span>
        </Badge>
        <span className="text-xs text-muted-foreground">
          {confidencePercentage}% confidence
        </span>
      </div>

      <h2 className="text-sm font-semibold mb-1 line-clamp-2">
        Status Change:{" "}
        <span
          className={cn(
            report.original_status === "pending" &&
              "text-yellow-700 bg-yellow-50 border-yellow-200",
            report.original_status === "pass" &&
              "text-green-700 bg-green-50 border-green-200",
            report.original_status === "warning" &&
              "text-orange-700 bg-orange-50 border-orange-200",
            report.original_status === "critical" &&
              "text-red-700 bg-red-50 border-red-200"
          )}
        >
          {report.original_status}
        </span>{" "}
        →{" "}
        <span
          className={cn(
            report.status_change_to === "pending" &&
              "text-yellow-700 bg-yellow-50 border-yellow-200",
            report.status_change_to === "pass" &&
              "text-green-700 bg-green-50 border-green-200",
            report.status_change_to === "warning" &&
              "text-orange-700 bg-orange-50 border-orange-200",
            report.status_change_to === "critical" &&
              "text-red-700 bg-red-50 border-red-200"
          )}
        >
          {report.status_change_to}
        </span>
      </h2>

      <p className="text-xs text-muted-foreground mb-2 line-clamp-3">
        {report.reason}
      </p>

      {report.needs_action && report.status === "pending" && (
        <div className="flex items-center gap-1 text-xs text-orange-600 bg-orange-50 px-2 py-1 rounded">
          <AlertTriangle className="h-3 w-3" />
          Action Required
        </div>
      )}

      <div className="text-xs text-muted-foreground mt-2">
        Feature: {report.feature_id.slice(-8)}
      </div>
    </div>
  );
}

export default function EventsPanel() {
  const [state, dispatch] = useReducer(auditReportsReducer, {
    auditReports: [],
    loading: true,
    error: null,
  });

  const [selectedReport, setSelectedReport] = useState<AuditReport | null>(
    null
  );
  const [dialogOpen, setDialogOpen] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  const handleReportClick = (report: AuditReport) => {
    setSelectedReport(report);
    setDialogOpen(true);
  };

  const handleDialogClose = (open: boolean) => {
    setDialogOpen(open);
    if (!open) {
      setSelectedReport(null);
    }
  };

  useEffect(() => {
    dispatch({ type: "LOADING" });

    // Create SSE connection
    const eventSource = new EventSource(
      `${process.env.NEXT_PUBLIC_API_URL}/audit-report/stream`
    );

    eventSourceRef.current = eventSource;

    eventSource.onmessage = (event) => {
      try {
        // Parse and validate the event data
        const eventData = JSON.parse(event.data);
        const validatedEvent = AuditReportStreamEventSchema.parse(eventData);

        if (validatedEvent.type === "initial_data") {
          dispatch({
            type: "SET_INITIAL_AUDIT_REPORTS",
            payload: validatedEvent.data.audit_reports,
          });
        } else if (validatedEvent.type === "audit_report_added") {
          if (validatedEvent.data.audit_report_data) {
            dispatch({
              type: "ADD_AUDIT_REPORT",
              payload: validatedEvent.data.audit_report_data,
            });
          }
        } else if (
          validatedEvent.type === "audit_report_updated" ||
          validatedEvent.type === "audit_report_changed"
        ) {
          if (validatedEvent.data.audit_report_data) {
            dispatch({
              type: "UPDATE_AUDIT_REPORT",
              payload: {
                auditReportId: validatedEvent.data.audit_report_id,
                auditReportData: validatedEvent.data.audit_report_data,
              },
            });
            // Update the selected report if it's currently being viewed
            if (
              selectedReport &&
              selectedReport.id === validatedEvent.data.audit_report_id
            ) {
              setSelectedReport(validatedEvent.data.audit_report_data);
            }
          }
        } else if (validatedEvent.type === "audit_report_deleted") {
          dispatch({
            type: "DELETE_AUDIT_REPORT",
            payload: {
              auditReportId: validatedEvent.data.audit_report_id,
            },
          });
          // Close dialog if the selected report was deleted
          if (
            selectedReport &&
            selectedReport.id === validatedEvent.data.audit_report_id
          ) {
            setDialogOpen(false);
          }
        } else if (validatedEvent.type === "error") {
          dispatch({
            type: "ERROR",
            payload: validatedEvent.data.message,
          });
        }
      } catch (error) {
        console.error(
          "Error parsing or validating audit report event data:",
          error
        );
        dispatch({
          type: "ERROR",
          payload: `Failed to parse stream event: ${
            error instanceof Error ? error.message : "Unknown error"
          }`,
        });
      }
    };

    eventSource.onerror = (error) => {
      console.error("EventSource error:", error);
      dispatch({
        type: "ERROR",
        payload: "Connection to audit reports stream failed",
      });
    };

    eventSource.onopen = () => {
      console.log("Audit reports EventSource connection opened");
      dispatch({ type: "RESET_ERROR" });
    };

    // Cleanup function
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    };
  }, [selectedReport]);

  const [statusFilter, setStatusFilter] = useState<AuditReportStatus[]>([]);

  const filteredAuditReports = useMemo(() => {
    if (statusFilter.length === 0) {
      return state.auditReports.sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    }
    return state.auditReports
      .filter((report) => statusFilter.includes(report.status))
      .sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
  }, [state.auditReports, statusFilter]);

  return (
    <>
      <div className="flex flex-col h-[calc(100vh-16px)] w-[420px] sticky top-4 mt-4 mr-4 pb-4">
        <Card className="flex flex-col h-full w-full p-4">
          <div className="flex flex-col gap-2 h-full w-full">
            <h1 className="text-lg font-bold w-full flex items-center">
              <span>Real-time audit reports</span>
              <span className="ml-auto flex items-center gap-1">
                <span className="text-xs text-green-600">Agent Live</span>
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-green-600"></span>
                </span>
              </span>
            </h1>

            <MultiSelect
              options={[
                { label: "Pending", value: "pending" },
                { label: "Verified", value: "verified" },
                { label: "Dismissed", value: "dismissed" },
              ]}
              onValueChange={(value) =>
                setStatusFilter(value as AuditReportStatus[])
              }
              hideSelectAll
            />

            {state.error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm mb-2">
                  Error: {state.error}
                </p>
                <button
                  onClick={() => window.location.reload()}
                  className="px-3 py-1 bg-red-100 text-red-700 rounded text-xs hover:bg-red-200"
                >
                  Retry
                </button>
              </div>
            )}

            {/* {state.loading && (
              <div className="p-3 text-center text-sm text-muted-foreground">
                Loading audit reports...
              </div>
            )} */}

            {!state.loading &&
              (state.auditReports.length === 0 ||
                filteredAuditReports.length === 0) &&
              !state.error && (
                <div className="p-3 text-center text-sm text-muted-foreground">
                  No audit reports yet
                </div>
              )}

            <div className="flex flex-col gap-2 overflow-y-scroll h-full">
              {filteredAuditReports.map((report) => (
                <AuditReportItem
                  key={report.id}
                  report={report}
                  onClick={() => handleReportClick(report)}
                />
              ))}
            </div>
          </div>
        </Card>
      </div>

      <AuditReportDialog
        report={selectedReport}
        open={dialogOpen}
        onOpenChange={handleDialogClose}
      />
    </>
  );
}
