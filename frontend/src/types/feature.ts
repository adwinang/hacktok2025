import { z } from "zod";
import { DateSchema } from "./date";

export const FeatureSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  status: z.enum(["pending", "pass", "warning", "critical"]),
  created_at: DateSchema,
  updated_at: DateSchema.nullable(),
});

export const FeaturesSchema = z.array(FeatureSchema);

export const FeaturesResponseSchema = z.object({
  success: z.boolean(),
  features: FeaturesSchema,
});

export type Feature = z.infer<typeof FeatureSchema>;
export type Features = z.infer<typeof FeaturesSchema>;
export type FeaturesResponse = z.infer<typeof FeaturesResponseSchema>;
