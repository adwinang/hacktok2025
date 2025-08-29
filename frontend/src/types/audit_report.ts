import { z } from "zod";
import { DateSchema } from "./date";

// Enums
export const FeatureStatusSchema = z.enum([
  "pending",
  "pass",
  "warning",
  "critical",
]);
export const AuditReportStatusSchema = z.enum([
  "pending",
  "dismissed",
  "verified",
]);

// Core audit report schema
export const AuditReportSchema = z.object({
  id: z.string(),
  feature_id: z.string(),
  source_ids: z.array(z.string()),
  needs_action: z.boolean(),
  original_status: FeatureStatusSchema,
  status_change_to: FeatureStatusSchema,
  reason: z.string(),
  confidence: z.number(),
  created_at: DateSchema,
  updated_at: DateSchema.nullable(),
  status: AuditReportStatusSchema,
});

export const AuditReportsSchema = z.array(AuditReportSchema);

export const AuditReportsResponseSchema = z.object({
  success: z.boolean(),
  audit_reports: AuditReportsSchema,
});

// Stream event types
export const AuditReportStreamInitialDataSchema = z.object({
  type: z.literal("initial_data"),
  data: z.object({
    audit_reports: AuditReportsSchema,
  }),
});

export const AuditReportStreamAddedSchema = z.object({
  type: z.literal("audit_report_added"),
  data: z.object({
    operation_type: z.string(),
    audit_report_id: z.string(),
    audit_report_data: AuditReportSchema,
    timestamp: z.string(),
  }),
});

export const AuditReportStreamUpdatedSchema = z.object({
  type: z.literal("audit_report_updated"),
  data: z.object({
    operation_type: z.string(),
    audit_report_id: z.string(),
    audit_report_data: AuditReportSchema,
    timestamp: z.string(),
  }),
});

export const AuditReportStreamDeletedSchema = z.object({
  type: z.literal("audit_report_deleted"),
  data: z.object({
    operation_type: z.string(),
    audit_report_id: z.string(),
    audit_report_data: z.null(),
    timestamp: z.string(),
  }),
});

export const AuditReportStreamChangedSchema = z.object({
  type: z.literal("audit_report_changed"),
  data: z.object({
    operation_type: z.string(),
    audit_report_id: z.string(),
    audit_report_data: AuditReportSchema.nullable(),
    timestamp: z.string(),
  }),
});

export const AuditReportStreamErrorSchema = z.object({
  type: z.literal("error"),
  data: z.object({
    message: z.string(),
  }),
});

export const AuditReportStreamEventSchema = z.union([
  AuditReportStreamInitialDataSchema,
  AuditReportStreamAddedSchema,
  AuditReportStreamUpdatedSchema,
  AuditReportStreamDeletedSchema,
  AuditReportStreamChangedSchema,
  AuditReportStreamErrorSchema,
]);

// Type exports
export type FeatureStatus = z.infer<typeof FeatureStatusSchema>;
export type AuditReportStatus = z.infer<typeof AuditReportStatusSchema>;
export type AuditReport = z.infer<typeof AuditReportSchema>;
export type AuditReports = z.infer<typeof AuditReportsSchema>;
export type AuditReportsResponse = z.infer<typeof AuditReportsResponseSchema>;
export type AuditReportStreamEvent = z.infer<
  typeof AuditReportStreamEventSchema
>;
export type AuditReportStreamInitialData = z.infer<
  typeof AuditReportStreamInitialDataSchema
>;
export type AuditReportStreamAdded = z.infer<
  typeof AuditReportStreamAddedSchema
>;
export type AuditReportStreamUpdated = z.infer<
  typeof AuditReportStreamUpdatedSchema
>;
export type AuditReportStreamDeleted = z.infer<
  typeof AuditReportStreamDeletedSchema
>;
export type AuditReportStreamChanged = z.infer<
  typeof AuditReportStreamChangedSchema
>;
export type AuditReportStreamError = z.infer<
  typeof AuditReportStreamErrorSchema
>;
