export type Severity = "informational" | "low" | "medium" | "high" | "critical";
export type AlertStatus =
  | "new"
  | "acknowledged"
  | "investigating"
  | "escalated"
  | "resolved"
  | "suppressed";

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Membership {
  id: string;
  organization_id?: string;
  organization?: string;
  organization_name: string;
  role: string;
}

export interface User {
  id: string;
  email: string;
  display_name: string;
  phone?: string;
  timezone?: string;
  is_analyst: boolean;
  mfa_enabled: boolean;
}

export interface EventRecord {
  id: string;
  timestamp: string;
  ingested_at: string;
  event_type: string;
  severity: Severity;
  source_ip?: string | null;
  destination_ip?: string | null;
  source_port?: number | null;
  destination_port?: number | null;
  username: string;
  hostname: string;
  process: string;
  action: string;
  message: string;
  metadata: Record<string, unknown>;
  tags: string[];
  source_name?: string;
  asset_name?: string;
  raw_payload?: Record<string, unknown> | null;
}

export interface AlertRecord {
  id: string;
  title: string;
  severity: Severity;
  status: AlertStatus;
  rule_name?: string;
  assigned_email?: string;
  source_ip?: string | null;
  username: string;
  tags: string[];
  resolution_reason: string;
  notes: { id: string; body: string; author_email?: string; created_at: string }[];
  evidence: { id: string; label: string; kind: string; data: Record<string, unknown> }[];
  timeline: { id: string; action: string; detail: Record<string, unknown>; actor_email?: string; created_at: string }[];
  related_events: EventRecord[];
  created_at: string;
}

export interface IncidentRecord {
  id: string;
  title: string;
  summary: string;
  status: string;
  priority: Severity;
  owner_email?: string;
  affected_users: string[];
  tags: string[];
  tasks: { id: string; title: string; done: boolean }[];
  comments: { id: string; body: string; author_email?: string; created_at: string }[];
  history: { id: string; from_status: string; to_status: string; note: string; created_at: string }[];
  created_at: string;
}

export interface AssetRecord {
  id: string;
  hostname: string;
  ip_address?: string | null;
  operating_system: string;
  owner: string;
  criticality: Severity;
  tags: string[];
  last_seen_at?: string | null;
  vulnerability_count?: number;
  event_count?: number;
}

export interface RuleRecord {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  rule_type: string;
  severity: Severity;
  conditions: Record<string, unknown>;
  threshold_count: number;
  window_minutes: number;
  group_by: string[];
  tags: string[];
  current_version: number;
}

export interface IndicatorRecord {
  id: string;
  indicator_type: string;
  value: string;
  confidence: number;
  source: string;
  expires_at?: string | null;
  is_active: boolean;
  description: string;
  match_count: number;
}

export interface OverviewData {
  event_volume_24h: number;
  active_alerts: number;
  critical_incidents: number;
  auth_failures_24h: number;
  suspicious_ips: { source_ip: string; count: number }[];
  affected_assets: number;
  detection_trend: { hour: string; count: number }[];
  alerts_by_severity: { severity: string; count: number }[];
  analyst_workload: { assigned_to__email: string; assigned_to__display_name: string; count: number }[];
  open_incidents: number;
  recent_alerts: { id: string; title: string; severity: Severity; status: string; created_at: string }[];
}
