import { format } from "date-fns";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Badge } from "../components/Badge";
import { DataTable } from "../components/DataTable";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { EventRecord, Paginated } from "../types";
import api from "../api/client";

export function Events() {
  const [q, setQ] = useState("");
  const [severity, setSeverity] = useState("");
  const navigate = useNavigate();
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  if (severity) params.set("severity", severity);
  const { data, reload } = useApi<Paginated<EventRecord>>(`/events/?${params.toString()}`, [q, severity]);

  async function exportCsv() {
    const res = await api.get("/events/export/?format=csv", { responseType: "blob" });
    const url = URL.createObjectURL(res.data);
    const a = document.createElement("a");
    a.href = url;
    a.download = "events.csv";
    a.click();
  }

  return (
    <div>
      <PageHeader
        title="Events"
        subtitle="Normalized security records with full-text search and export"
        actions={
          <>
            <button className="rounded border border-ink-600 px-3 py-1.5 text-xs" onClick={exportCsv}>
              Export
            </button>
            <button className="rounded border border-ink-600 px-3 py-1.5 text-xs" onClick={reload}>
              Refresh
            </button>
          </>
        }
      />
      <div className="mb-3 flex gap-2">
        <input
          className="w-full max-w-md rounded px-3 py-2 text-sm"
          placeholder="Search user, IP, host, message..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <select className="rounded px-3 py-2 text-sm" value={severity} onChange={(e) => setSeverity(e.target.value)}>
          <option value="">All severities</option>
          {["informational", "low", "medium", "high", "critical"].map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>
      </div>
      <DataTable
        rows={data?.results || []}
        onRow={(row) => navigate(`/events/${row.id}`)}
        columns={[
          { key: "timestamp", label: "Time", render: (r) => format(new Date(r.timestamp), "MMM d HH:mm:ss") },
          { key: "severity", label: "Sev", render: (r) => <Badge value={r.severity} /> },
          { key: "event_type", label: "Type" },
          { key: "source_ip", label: "Source IP" },
          { key: "username", label: "User" },
          { key: "hostname", label: "Asset" },
          { key: "message", label: "Message" },
        ]}
      />
    </div>
  );
}
