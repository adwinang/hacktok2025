import { z } from "zod";
import { DateSchema } from "./date";

// Core source schema
export const SourceSchema = z.object({
  id: z.string(),
  source_url: z.string(),
  tags: z.array(z.string()).nullable(),
  created_at: DateSchema,
  updated_at: DateSchema.nullable(),
});

export const SourcesSchema = z.array(SourceSchema);

export const SourcesResponseSchema = z.object({
  success: z.boolean(),
  sources: SourcesSchema,
});

// Request schemas
export const SourceIdsRequestSchema = z.object({
  source_ids: z.array(z.string()),
});

// Type exports
export type Source = z.infer<typeof SourceSchema>;
export type Sources = z.infer<typeof SourcesSchema>;
export type SourcesResponse = z.infer<typeof SourcesResponseSchema>;
export type SourceIdsRequest = z.infer<typeof SourceIdsRequestSchema>;

// SSE event schemas
export const SourceStreamInitialDataSchema = z.object({
  type: z.literal("initial_data"),
  data: z.object({
    sources: SourcesSchema,
  }),
});

export const SourceStreamUpdateSchema = z.object({
  type: z.literal("source_update"),
  data: z.object({
    operation_type: z.string(),
    source_id: z.string(),
    source_data: SourceSchema,
    timestamp: z.string(),
  }),
});

export const SourceStreamErrorSchema = z.object({
  type: z.literal("error"),
  data: z.object({
    message: z.string(),
  }),
});

export const SourceStreamEventSchema = z.union([
  SourceStreamInitialDataSchema,
  SourceStreamUpdateSchema,
  SourceStreamErrorSchema,
]);

export type SourceStreamEvent = z.infer<typeof SourceStreamEventSchema>;
export type SourceStreamInitialData = z.infer<typeof SourceStreamInitialDataSchema>;
export type SourceStreamUpdate = z.infer<typeof SourceStreamUpdateSchema>;
export type SourceStreamError = z.infer<typeof SourceStreamErrorSchema>;
