import { useState } from "react";
import { Badge } from "../components/Badge";
import { DataTable } from "../components/DataTable";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { Paginated, RuleRecord } from "../types";
import api from "../api/client";

export function Rules() {
  const { data, reload } = useApi<Paginated<RuleRecord>>("/rules/");
  const { data: allowlists, reload: reloadAllow } = useApi<Paginated<any>>("/allowlists/");
  const { data: suppressions } = useApi<Paginated<any>>("/suppressions/");
  const [name, setName] = useState("Suspicious source IP burst");
  const [eventType, setEventType] = useState("firewall.deny");

  async function create() {
    await api.post("/rules/", {
      name,
      description: "Generated from console",
      rule_type: "threshold",
      severity: "high",
      threshold_count: 8,
      window_minutes: 10,
      group_by: ["source_ip"],
      conditions: {
        operator: "and",
        conditions: [{ field: "event_type", op: "contains", value: eventType }],
      },
    });
    reload();
  }

  return (
    <div>
      <PageHeader title="Detection rules" subtitle="Match, threshold, and correlation rules with version history" />
      <div className="mb-3 flex gap-2">
        <input className="rounded px-3 py-2 text-sm" value={name} onChange={(e) => setName(e.target.value)} />
        <input className="rounded px-3 py-2 text-sm" value={eventType} onChange={(e) => setEventType(e.target.value)} />
        <button className="rounded bg-accent-500 px-3 text-xs text-ink-950" onClick={create}>
          Create rule
        </button>
      </div>
      <div className="mb-3 grid grid-cols-1 gap-3 lg:grid-cols-2">
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-3">
          <div className="mb-2 flex items-center justify-between text-[11px] uppercase text-mist-500">
            <span>Allowlists</span>
            <button
              className="rounded border border-ink-600 px-2 py-1 normal-case"
              onClick={async () => {
                await api.post("/allowlists/", { name: "Known scanner", field: "source_ip", value: "192.0.2.10" });
                reloadAllow();
              }}
            >
              Add
            </button>
          </div>
          {(allowlists?.results || []).map((item: any) => (
            <div key={item.id} className="font-mono text-xs text-mist-300">
              {item.field}={item.value}
            </div>
          ))}
        </section>
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-3">
          <div className="mb-2 text-[11px] uppercase text-mist-500">Suppressions</div>
          {(suppressions?.results || []).map((item: any) => (
            <div key={item.id} className="font-mono text-xs text-mist-300">
              {item.field}={item.value} until {item.until || "indefinite"}
            </div>
          ))}
        </section>
      </div>
      <DataTable
        rows={data?.results || []}
        columns={[
          { key: "name", label: "Rule" },
          { key: "rule_type", label: "Type" },
          { key: "severity", label: "Sev", render: (r) => <Badge value={r.severity} /> },
          { key: "enabled", label: "Enabled", render: (r) => (r.enabled ? "yes" : "no") },
          { key: "threshold_count", label: "Threshold" },
          { key: "window_minutes", label: "Window" },
          { key: "current_version", label: "Ver" },
        ]}
      />
    </div>
  );
}
