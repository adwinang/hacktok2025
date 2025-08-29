import { AlertTriangle, Ban, Check, Clock } from "lucide-react";

export const statuses = [
  {
    value: "pending",
    label: "Pending",
    icon: Clock,
  },
  {
    value: "pass",
    label: "Pass",
    icon: Check,
  },
  {
    value: "warning",
    label: "Warning",
    icon: AlertTriangle,
  },
  {
    value: "critical",
    label: "Critical",
    icon: Ban,
  },
];
