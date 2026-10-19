import { useState } from "react";
import { Badge } from "../components/Badge";
import { DataTable } from "../components/DataTable";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { IndicatorRecord, Paginated } from "../types";
import api from "../api/client";

export function Indicators() {
  const { data, reload } = useApi<Paginated<IndicatorRecord>>("/indicators/");
  const [value, setValue] = useState("");
  const [type, setType] = useState("ip");

  async function create() {
    await api.post("/indicators/", {
      indicator_type: type,
      value,
      confidence: 80,
      source: "Analyst",
      description: "Added from console",
    });
    setValue("");
    reload();
  }

  return (
    <div>
      <PageHeader title="Threat indicators" subtitle="IPs, domains, hashes, usernames, and custom indicators" />
      <div className="mb-3 flex gap-2">
        <select className="rounded px-3 py-2 text-sm" value={type} onChange={(e) => setType(e.target.value)}>
          {["ip", "domain", "hash", "username", "url", "email", "custom"].map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
        <input className="rounded px-3 py-2 text-sm" value={value} onChange={(e) => setValue(e.target.value)} placeholder="Indicator value" />
        <button className="rounded bg-accent-500 px-3 text-xs text-ink-950" onClick={create}>
          Add indicator
        </button>
      </div>
      <DataTable
        rows={data?.results || []}
        columns={[
          { key: "indicator_type", label: "Type" },
          { key: "value", label: "Value" },
          { key: "confidence", label: "Confidence" },
          { key: "source", label: "Source" },
          { key: "match_count", label: "Matches" },
          { key: "is_active", label: "Active", render: (r) => (r.is_active ? <Badge value="open" /> : <Badge value="closed" />) },
        ]}
      />
    </div>
  );
}
