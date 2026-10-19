import { useEffect, useState } from "react";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import api from "../api/client";

export function Settings() {
  const { data: settings } = useApi<any>("/settings/current/");
  const { data: sources, reload: reloadSources } = useApi<any>("/sources/");
  const { data: routes } = useApi<any>("/alert-routes/");
  const { data: retention } = useApi<any>("/retention/");
  const { data: environments } = useApi<any>("/environments/");
  const { data: teams } = useApi<any>("/teams/");
  const [form, setForm] = useState<any>({});
  const [mfaSecret, setMfaSecret] = useState("");
  const [otp, setOtp] = useState("");

  useEffect(() => {
    if (settings) setForm(settings);
  }, [settings]);

  return (
    <div>
      <PageHeader title="Organization settings" subtitle="Retention, routing, sources, and MFA" />
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-3 text-[11px] uppercase text-mist-500">Tenant preferences</div>
          {["timezone", "branding_name", "alert_email", "session_timeout_minutes"].map((key) => (
            <label key={key} className="mb-2 block text-xs text-mist-500">
              {key.replaceAll("_", " ")}
              <input
                className="mt-1 w-full rounded px-3 py-2 text-sm"
                value={form?.[key] ?? ""}
                onChange={(e) => setForm({ ...form, [key]: e.target.value })}
              />
            </label>
          ))}
          <button
            className="rounded bg-accent-500 px-3 py-1.5 text-xs text-ink-950"
            onClick={() => api.patch(`/settings/${form.id}/`, form)}
          >
            Save settings
          </button>
        </section>
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-3 text-[11px] uppercase text-mist-500">Multi-factor authentication</div>
          <button
            className="mb-2 rounded border border-ink-600 px-3 py-1.5 text-xs"
            onClick={async () => {
              const { data } = await api.post("/auth/mfa/setup/");
              setMfaSecret(data.secret);
            }}
          >
            Setup MFA
          </button>
          {mfaSecret && <div className="mb-2 font-mono text-xs text-accent-400">{mfaSecret}</div>}
          <div className="flex gap-2">
            <input className="rounded px-3 py-2 text-sm" value={otp} onChange={(e) => setOtp(e.target.value)} placeholder="123456" />
            <button className="rounded border border-ink-600 px-3 text-xs" onClick={() => api.post("/auth/mfa/enable/", { otp })}>
              Enable
            </button>
          </div>
        </section>
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-3 text-[11px] uppercase text-mist-500">Data sources</div>
          {(sources?.results || []).map((s: any) => (
            <div key={s.id} className="border-t border-ink-700 py-2 text-xs">
              <div className="font-medium">{s.name}</div>
              <div className="font-mono text-mist-500">{s.source_type} · {s.ingest_method} · {s.api_key}</div>
            </div>
          ))}
          <button
            className="mt-2 rounded border border-ink-600 px-3 py-1.5 text-xs"
            onClick={async () => {
              await api.post("/sources/", { name: "Custom HTTP collector", source_type: "custom", ingest_method: "http" });
              reloadSources();
            }}
          >
            Add HTTP source
          </button>
        </section>
        <section className="rounded-lg border border-ink-700 bg-ink-850 p-4">
          <div className="mb-3 text-[11px] uppercase text-mist-500">Alert routes & retention</div>
          {(routes?.results || []).map((r: any) => (
            <div key={r.id} className="border-t border-ink-700 py-2 text-xs">
              {r.name} · {r.channel} ≥ {r.min_severity}
            </div>
          ))}
          {(retention?.results || []).map((r: any) => (
            <div key={r.id} className="border-t border-ink-700 py-2 text-xs">
              Keep {r.entity_type} for {r.days} days
            </div>
          ))}
          <div className="mt-3 text-[11px] uppercase text-mist-500">Environments</div>
          {(environments?.results || []).map((e: any) => (
            <div key={e.id} className="text-xs text-mist-300">
              {e.name} {e.is_production ? "(prod)" : ""}
            </div>
          ))}
          <div className="mt-3 text-[11px] uppercase text-mist-500">Teams</div>
          {(teams?.results || []).map((t: any) => (
            <div key={t.id} className="text-xs text-mist-300">
              {t.name} {t.on_call ? "· on call" : ""}
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}
