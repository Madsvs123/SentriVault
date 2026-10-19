import { useParams } from "react-router-dom";
import { Badge } from "../components/Badge";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { AssetRecord, EventRecord } from "../types";

export function AssetDetail() {
  const { id } = useParams();
  const { data } = useApi<AssetRecord>(id ? `/assets/${id}/` : null);
  const { data: events } = useApi<EventRecord[]>(id ? `/assets/${id}/events/` : null);
  const { data: vulns } = useApi<any[]>(id ? `/assets/${id}/vulnerabilities/` : null);
  if (!data) return null;
  return (
    <div>
      <PageHeader title={data.hostname} subtitle={`${data.ip_address || "no IP"} · ${data.operating_system || "unknown OS"}`} />
      <div className="mb-3 flex gap-2">
        <Badge value={data.criticality} />
        {data.tags?.map((t) => (
          <Badge key={t} value={t} />
        ))}
      </div>
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-2 text-[11px] uppercase text-mist-500">Vulnerabilities</div>
          {(vulns || []).map((v) => (
            <div key={v.id} className="flex justify-between border-t border-ink-700 py-2 text-xs">
              <span>{v.cve_id} · {v.title}</span>
              <Badge value={v.severity} />
            </div>
          ))}
        </section>
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-2 text-[11px] uppercase text-mist-500">Event history</div>
          {(events || []).slice(0, 12).map((ev) => (
            <div key={ev.id} className="border-t border-ink-700 py-2 text-xs">
              {ev.event_type} · {ev.message}
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}
