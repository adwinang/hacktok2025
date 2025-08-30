import { z } from "zod";
import { DateSchema } from "./date";

export const FeatureSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  tags: z.array(z.string()),
  status: z.enum(["pending", "pass", "warning", "critical"]),
  created_at: DateSchema,
  updated_at: DateSchema.nullable(),
});

export const FeaturesSchema = z.array(FeatureSchema);

export const FeaturesResponseSchema = z.object({
  success: z.boolean(),
  features: FeaturesSchema,
});

// Stream event types
export const StreamInitialDataSchema = z.object({
  type: z.literal("initial_data"),
  data: z.object({
    features: FeaturesSchema,
  }),
});

export const StreamFeatureUpdateSchema = z.object({
  type: z.literal("feature_update"),
  data: z.object({
    operation_type: z.string(),
    feature_id: z.string(),
    feature_data: FeatureSchema,
    timestamp: z.string(),
  }),
});

export const StreamErrorSchema = z.object({
  type: z.literal("error"),
  data: z.object({
    message: z.string(),
  }),
});

export const StreamEventSchema = z.union([
  StreamInitialDataSchema,
  StreamFeatureUpdateSchema,
  StreamErrorSchema,
]);

export type Feature = z.infer<typeof FeatureSchema>;
export type Features = z.infer<typeof FeaturesSchema>;
export type FeaturesResponse = z.infer<typeof FeaturesResponseSchema>;
export type StreamEvent = z.infer<typeof StreamEventSchema>;
export type StreamInitialData = z.infer<typeof StreamInitialDataSchema>;
export type StreamFeatureUpdate = z.infer<typeof StreamFeatureUpdateSchema>;
export type StreamError = z.infer<typeof StreamErrorSchema>;
