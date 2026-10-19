import {
  Activity,
  Bell,
  Box,
  FileBarChart,
  Fingerprint,
  Radar,
  Search,
  Settings,
  Shield,
  Siren,
  Users,
  Workflow,
} from "lucide-react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { useAuth } from "../store/auth";
import { useApi } from "../hooks/useApi";
import { useRealtime } from "../hooks/useRealtime";

const nav = [
  { to: "/", label: "Overview", icon: Activity },
  { to: "/events", label: "Events", icon: Search },
  { to: "/alerts", label: "Alerts", icon: Siren },
  { to: "/incidents", label: "Incidents", icon: Workflow },
  { to: "/assets", label: "Assets", icon: Box },
  { to: "/rules", label: "Detection", icon: Radar },
  { to: "/indicators", label: "Threat Intel", icon: Fingerprint },
  { to: "/investigations", label: "Investigations", icon: Shield },
  { to: "/reports", label: "Reports", icon: FileBarChart },
  { to: "/users", label: "Users", icon: Users },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function AppShell() {
  const { user, loadMe, logout, memberships, organizationId } = useAuth();
  const navigate = useNavigate();
  const { data: notes } = useApi<{ results: { is_read: boolean }[] }>("/notifications/", []);
  const [liveAlert, setLiveAlert] = useState<string | null>(null);

  useEffect(() => {
    loadMe().catch(() => navigate("/login"));
  }, []);

  useRealtime("/ws/alerts/", (payload: any) => {
    if (payload?.alert?.title) setLiveAlert(payload.alert.title);
  });

  const unread = notes?.results?.filter((n) => !n.is_read).length || 0;

  return (
    <div className="grid min-h-screen grid-cols-[220px_1fr]">
      <aside className="border-r border-ink-700 bg-ink-900/95">
        <div className="flex items-center gap-2 border-b border-ink-700 px-4 py-4">
          <div className="flex h-8 w-8 items-center justify-center rounded bg-accent-500/20 text-accent-400">
            <Shield size={16} />
          </div>
          <div>
            <div className="text-sm font-semibold">SentriVault</div>
            <div className="font-mono text-[10px] uppercase tracking-widest text-mist-500">SIEM</div>
          </div>
        </div>
        <nav className="flex flex-col gap-0.5 p-2">
          {nav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-2 rounded px-3 py-2 text-[13px] ${
                  isActive ? "bg-ink-800 text-accent-400" : "text-mist-300 hover:bg-ink-800/70"
                }`
              }
            >
              <item.icon size={15} />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="flex min-w-0 flex-col">
        <header className="flex items-center justify-between border-b border-ink-700 bg-ink-900/80 px-5 py-2.5">
          <div className="font-mono text-[11px] text-mist-500">
            {memberships.find((m) => (m.organization_id || m.organization) === organizationId)?.organization_name ||
              "No organization"}
            <span className="mx-2 text-ink-600">/</span>
            live tenant isolation
          </div>
          <div className="flex items-center gap-3 text-xs text-mist-300">
            <span className="relative">
              <Bell size={15} />
              {unread > 0 && (
                <span className="absolute -right-1 -top-1 h-2 w-2 rounded-full bg-rose-500" />
              )}
            </span>
            <span>{user?.display_name || user?.email}</span>
            <button className="rounded border border-ink-600 px-2 py-1" onClick={() => logout().then(() => navigate("/login"))}>
              Sign out
            </button>
          </div>
        </header>
        <main className="min-w-0 flex-1 p-5">
          {liveAlert && (
            <div className="mb-3 rounded border border-rose-500/40 bg-rose-500/10 px-3 py-2 text-xs text-rose-200">
              Live alert · {liveAlert}
            </div>
          )}
          <Outlet />
        </main>
      </div>
    </div>
  );
}
