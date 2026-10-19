import { useState } from "react";
import { PageHeader } from "../components/PageHeader";
import { DataTable } from "../components/DataTable";
import { useApi } from "../hooks/useApi";
import type { Paginated } from "../types";
import api from "../api/client";

export function Investigations() {
  const { data, reload } = useApi<Paginated<any>>("/investigations/");
  const { data: queries, reload: reloadQueries } = useApi<Paginated<any>>("/saved-queries/");
  const [title, setTitle] = useState("Hunt: failed VPN auth");
  const [query, setQuery] = useState("auth.failure");

  return (
    <div>
      <PageHeader title="Investigations" subtitle="Saved queries, case notes, and related-event workspaces" />
      <div className="mb-4 grid grid-cols-1 gap-3 lg:grid-cols-2">
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-2 text-[11px] uppercase text-mist-500">New investigation</div>
          <input className="mb-2 w-full rounded px-3 py-2 text-sm" value={title} onChange={(e) => setTitle(e.target.value)} />
          <button
            className="rounded bg-accent-500 px-3 py-1.5 text-xs text-ink-950"
            onClick={async () => {
              await api.post("/investigations/", { title, summary: "Opened from console", status: "open" });
              reload();
            }}
          >
            Open case
          </button>
        </section>
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-2 text-[11px] uppercase text-mist-500">Save query</div>
          <input className="mb-2 w-full rounded px-3 py-2 text-sm" value={query} onChange={(e) => setQuery(e.target.value)} />
          <button
            className="rounded border border-ink-600 px-3 py-1.5 text-xs"
            onClick={async () => {
              await api.post("/saved-queries/", { name: query, query, time_range: "24h" });
              reloadQueries();
            }}
          >
            Save
          </button>
          <div className="mt-3 space-y-1 text-xs text-mist-300">
            {(queries?.results || []).map((item) => (
              <div key={item.id} className="font-mono">
                {item.name}
              </div>
            ))}
          </div>
        </section>
      </div>
      <DataTable
        rows={data?.results || []}
        columns={[
          { key: "title", label: "Investigation" },
          { key: "status", label: "Status" },
          { key: "owner_email", label: "Owner" },
          { key: "created_at", label: "Opened" },
        ]}
      />
    </div>
  );
}
