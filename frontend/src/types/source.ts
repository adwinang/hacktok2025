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
