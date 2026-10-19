import { useState } from "react";
import { useParams } from "react-router-dom";
import { format } from "date-fns";
import { Badge } from "../components/Badge";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { AlertRecord } from "../types";
import api from "../api/client";

export function AlertDetail() {
  const { id } = useParams();
  const { data, reload } = useApi<AlertRecord>(id ? `/alerts/${id}/` : null);
  const [note, setNote] = useState("");
  const [reason, setReason] = useState("Contained and monitored");

  async function act(path: string, body?: object) {
    await api.post(`/alerts/${id}/${path}/`, body || {});
    reload();
  }

  if (!data) return null;

  return (
    <div>
      <PageHeader
        title={data.title}
        subtitle={data.rule_name}
        actions={
          <>
            <button className="rounded border border-ink-600 px-3 py-1.5 text-xs" onClick={() => act("acknowledge")}>
              Acknowledge
            </button>
            <button className="rounded border border-ink-600 px-3 py-1.5 text-xs" onClick={() => act("escalate", { note: "Needs senior review" })}>
              Escalate
            </button>
            <button className="rounded bg-accent-500 px-3 py-1.5 text-xs text-ink-950" onClick={() => act("resolve", { reason })}>
              Resolve
            </button>
          </>
        }
      />
      <div className="mb-3 flex gap-2">
        <Badge value={data.severity} />
        <Badge value={data.status} />
        <span className="font-mono text-xs text-mist-500">{data.source_ip} · {data.username}</span>
      </div>
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-3">
        <div className="space-y-3 lg:col-span-2">
          <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
            <div className="mb-2 text-[11px] uppercase text-mist-500">Related events</div>
            {data.related_events?.map((ev) => (
              <div key={ev.id} className="border-t border-ink-700 py-2 text-xs">
                {format(new Date(ev.timestamp), "HH:mm:ss")} · {ev.event_type} · {ev.message}
              </div>
            ))}
          </section>
          <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
            <div className="mb-2 text-[11px] uppercase text-mist-500">Analyst notes</div>
            {data.notes?.map((n) => (
              <div key={n.id} className="border-t border-ink-700 py-2 text-xs">
                <div className="text-mist-500">{n.author_email}</div>
                {n.body}
              </div>
            ))}
            <div className="mt-2 flex gap-2">
              <input className="flex-1 rounded px-2 py-1.5 text-sm" value={note} onChange={(e) => setNote(e.target.value)} placeholder="Add a note" />
              <button className="rounded border border-ink-600 px-3 text-xs" onClick={() => act("notes", { body: note })}>
                Add
              </button>
            </div>
          </section>
        </div>
        <div className="space-y-3">
          <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
            <div className="mb-2 text-[11px] uppercase text-mist-500">Timeline</div>
            {data.timeline?.map((item) => (
              <div key={item.id} className="border-t border-ink-700 py-2 text-xs">
                <div className="font-mono text-accent-400">{item.action}</div>
                <div className="text-mist-500">{format(new Date(item.created_at), "MMM d HH:mm")}</div>
              </div>
            ))}
          </section>
          <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
            <div className="mb-2 text-[11px] uppercase text-mist-500">Resolution reason</div>
            <input className="w-full rounded px-2 py-1.5 text-sm" value={reason} onChange={(e) => setReason(e.target.value)} />
          </section>
        </div>
      </div>
    </div>
  );
}
