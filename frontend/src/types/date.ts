import { z } from "zod";

export const DateSchema = z.union([
  z.date(), // JavaScript Date
  z.instanceof(Date).transform((date) => date), // Native JavaScript Date
  z
    .string()
    .regex(
      /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?$/,
      "Invalid ISO date string"
    ) // ISO Date String - supports microseconds and optional timezone
    .transform((isoString) => new Date(isoString)), // Convert ISO string to Date
]);
