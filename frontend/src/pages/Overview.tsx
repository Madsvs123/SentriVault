import { format } from "date-fns";
import { Activity, ShieldAlert, Siren, Users } from "lucide-react";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Badge } from "../components/Badge";
import { KpiCard } from "../components/KpiCard";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { OverviewData } from "../types";
import { useNavigate } from "react-router-dom";

export function Overview() {
  const { data } = useApi<OverviewData>("/dashboard/overview/");
  const navigate = useNavigate();
  const trend = (data?.detection_trend || []).map((row) => ({
    ...row,
    hour: row.hour ? format(new Date(row.hour), "HH:mm") : "",
  }));

  return (
    <div>
      <PageHeader title="Security overview" subtitle="Event volume, active alerts, incidents, and analyst load" />
      <div className="grid grid-cols-2 gap-3 xl:grid-cols-4">
        <KpiCard label="Events 24h" value={data?.event_volume_24h ?? "—"} icon={<Activity size={14} />} />
        <KpiCard label="Active alerts" value={data?.active_alerts ?? "—"} icon={<Siren size={14} />} />
        <KpiCard label="Critical incidents" value={data?.critical_incidents ?? "—"} icon={<ShieldAlert size={14} />} />
        <KpiCard label="Auth failures" value={data?.auth_failures_24h ?? "—"} hint={`${data?.affected_assets ?? 0} assets seen`} icon={<Users size={14} />} />
      </div>
      <div className="mt-4 grid grid-cols-1 gap-3 xl:grid-cols-3">
        <div className="rounded-lg border border-ink-700 bg-ink-850/80 p-3 xl:col-span-2">
          <div className="mb-2 text-[11px] uppercase tracking-wider text-mist-500">Detection trend</div>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trend}>
                <XAxis dataKey="hour" tick={{ fill: "#6d7f91", fontSize: 10 }} />
                <YAxis tick={{ fill: "#6d7f91", fontSize: 10 }} />
                <Tooltip contentStyle={{ background: "#10161f", border: "1px solid #1c2533" }} />
                <Area dataKey="count" stroke="#3d9cf0" fill="rgba(61,156,240,0.2)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-lg border border-ink-700 bg-ink-850/80 p-3">
          <div className="mb-2 text-[11px] uppercase tracking-wider text-mist-500">Suspicious IPs</div>
          <div className="space-y-2">
            {(data?.suspicious_ips || []).map((row) => (
              <div key={row.source_ip} className="flex justify-between font-mono text-xs">
                <span>{row.source_ip}</span>
                <span className="text-mist-500">{row.count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="mt-4 grid grid-cols-1 gap-3 xl:grid-cols-2">
        <div className="rounded-lg border border-ink-700 bg-ink-850/80 p-3">
          <div className="mb-2 text-[11px] uppercase tracking-wider text-mist-500">Recent alerts</div>
          {(data?.recent_alerts || []).map((alert) => (
            <button
              key={alert.id}
              onClick={() => navigate(`/alerts/${alert.id}`)}
              className="flex w-full items-center justify-between border-t border-ink-700/70 py-2 text-left text-xs"
            >
              <span>{alert.title}</span>
              <Badge value={alert.severity} />
            </button>
          ))}
        </div>
        <div className="rounded-lg border border-ink-700 bg-ink-850/80 p-3">
          <div className="mb-2 text-[11px] uppercase tracking-wider text-mist-500">Analyst workload</div>
          {(data?.analyst_workload || []).map((row) => (
            <div key={row.assigned_to__email} className="flex justify-between border-t border-ink-700/70 py-2 text-xs">
              <span>{row.assigned_to__display_name || row.assigned_to__email}</span>
              <span className="font-mono text-mist-500">{row.count} alerts</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
