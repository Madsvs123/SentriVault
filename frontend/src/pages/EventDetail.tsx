import { useParams } from "react-router-dom";
import { format } from "date-fns";
import { Badge } from "../components/Badge";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { EventRecord } from "../types";

export function EventDetail() {
  const { id } = useParams();
  const { data } = useApi<EventRecord>(id ? `/events/${id}/` : null);
  const { data: related } = useApi<EventRecord[]>(id ? `/events/related/?event=${id}` : null);

  if (!data) return <div className="text-sm text-mist-500">Loading event...</div>;

  return (
    <div>
      <PageHeader title={data.event_type} subtitle={format(new Date(data.timestamp), "PPpp")} />
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-3">
        <div className="rounded-lg border border-ink-700 bg-ink-850 p-4 lg:col-span-2">
          <div className="mb-3 flex gap-2">
            <Badge value={data.severity} />
            {data.tags?.map((t) => (
              <Badge key={t} value={t} />
            ))}
          </div>
          <p className="text-sm text-mist-100">{data.message}</p>
          <dl className="mt-4 grid grid-cols-2 gap-2 font-mono text-xs">
            {[
              ["Source IP", data.source_ip],
              ["Destination IP", data.destination_ip],
              ["User", data.username],
              ["Host", data.hostname],
              ["Process", data.process],
              ["Action", data.action],
              ["Source", data.source_name],
              ["Asset", data.asset_name],
            ].map(([k, v]) => (
              <div key={k as string} className="rounded bg-ink-800 px-2 py-1.5">
                <div className="text-[10px] uppercase text-mist-500">{k}</div>
                <div>{String(v || "—")}</div>
              </div>
            ))}
          </dl>
          <pre className="mt-4 overflow-auto rounded bg-ink-950 p-3 text-[11px] text-mist-300">
            {JSON.stringify(data.metadata || data.raw_payload, null, 2)}
          </pre>
        </div>
        <div className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-2 text-[11px] uppercase text-mist-500">Related events</div>
          {(related || []).slice(0, 12).map((ev) => (
            <div key={ev.id} className="border-t border-ink-700 py-2 text-xs">
              <div className="font-mono text-mist-300">{ev.event_type}</div>
              <div className="text-mist-500">{ev.source_ip || ev.username}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
