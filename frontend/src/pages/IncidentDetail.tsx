import { useState } from "react";
import { useParams } from "react-router-dom";
import { Badge } from "../components/Badge";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { IncidentRecord } from "../types";
import api from "../api/client";

export function IncidentDetail() {
  const { id } = useParams();
  const { data, reload } = useApi<IncidentRecord>(id ? `/incidents/${id}/` : null);
  const [comment, setComment] = useState("");
  const [task, setTask] = useState("");

  if (!data) return null;

  return (
    <div>
      <PageHeader
        title={data.title}
        subtitle={data.summary}
        actions={
          <select
            className="rounded px-2 py-1.5 text-xs"
            value={data.status}
            onChange={async (e) => {
              await api.post(`/incidents/${id}/status/`, { status: e.target.value });
              reload();
            }}
          >
            {["open", "containing", "eradicating", "recovering", "closed"].map((s) => (
              <option key={s}>{s}</option>
            ))}
          </select>
        }
      />
      <div className="mb-3 flex gap-2">
        <Badge value={data.priority} />
        <Badge value={data.status} />
        <span className="text-xs text-mist-500">Owner {data.owner_email}</span>
      </div>
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-2 text-[11px] uppercase text-mist-500">Tasks</div>
          {data.tasks?.map((item) => (
            <label key={item.id} className="flex items-center gap-2 border-t border-ink-700 py-2 text-sm">
              <input
                type="checkbox"
                checked={item.done}
                onChange={async () => {
                  await api.post(`/incidents/${id}/tasks/${item.id}/toggle/`);
                  reload();
                }}
              />
              {item.title}
            </label>
          ))}
          <div className="mt-2 flex gap-2">
            <input className="flex-1 rounded px-2 py-1.5 text-sm" value={task} onChange={(e) => setTask(e.target.value)} placeholder="New task" />
            <button
              className="rounded border border-ink-600 px-3 text-xs"
              onClick={async () => {
                await api.post(`/incidents/${id}/tasks/`, { title: task });
                setTask("");
                reload();
              }}
            >
              Add
            </button>
          </div>
        </section>
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-2 text-[11px] uppercase text-mist-500">Comments</div>
          {data.comments?.map((item) => (
            <div key={item.id} className="border-t border-ink-700 py-2 text-xs">
              <div className="text-mist-500">{item.author_email}</div>
              {item.body}
            </div>
          ))}
          <div className="mt-2 flex gap-2">
            <input className="flex-1 rounded px-2 py-1.5 text-sm" value={comment} onChange={(e) => setComment(e.target.value)} />
            <button
              className="rounded border border-ink-600 px-3 text-xs"
              onClick={async () => {
                await api.post(`/incidents/${id}/comments/`, { body: comment });
                setComment("");
                reload();
              }}
            >
              Comment
            </button>
          </div>
        </section>
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4 lg:col-span-2">
          <div className="mb-2 text-[11px] uppercase text-mist-500">Status history</div>
          {data.history?.map((item) => (
            <div key={item.id} className="border-t border-ink-700 py-2 font-mono text-xs">
              {item.from_status || "new"} → {item.to_status} {item.note && `· ${item.note}`}
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}
