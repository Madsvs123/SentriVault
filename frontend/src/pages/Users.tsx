import { useState } from "react";
import { PageHeader } from "../components/PageHeader";
import { DataTable } from "../components/DataTable";
import { useApi } from "../hooks/useApi";
import type { Paginated, User } from "../types";
import api from "../api/client";

export function UsersPage() {
  const { data } = useApi<Paginated<User>>("/auth/users/");
  const { data: invites, reload } = useApi<Paginated<any>>("/auth/invitations/");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("analyst");

  return (
    <div>
      <PageHeader title="Users & invitations" subtitle="Roles, analyst accounts, and staff onboarding" />
      <div className="mb-4 flex gap-2">
        <input className="rounded px-3 py-2 text-sm" placeholder="analyst@company.com" value={email} onChange={(e) => setEmail(e.target.value)} />
        <select className="rounded px-3 py-2 text-sm" value={role} onChange={(e) => setRole(e.target.value)}>
          {["owner", "admin", "analyst", "responder", "viewer"].map((r) => (
            <option key={r}>{r}</option>
          ))}
        </select>
        <button
          className="rounded bg-accent-500 px-3 text-xs text-ink-950"
          onClick={async () => {
            await api.post("/auth/invitations/", { email, role });
            setEmail("");
            reload();
          }}
        >
          Invite
        </button>
      </div>
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
        <div>
          <div className="mb-2 text-[11px] uppercase text-mist-500">Directory</div>
          <DataTable
            rows={data?.results || []}
            columns={[
              { key: "display_name", label: "Name" },
              { key: "email", label: "Email" },
              { key: "mfa_enabled", label: "MFA", render: (r) => (r.mfa_enabled ? "on" : "off") },
            ]}
          />
        </div>
        <div>
          <div className="mb-2 text-[11px] uppercase text-mist-500">Pending invitations</div>
          <DataTable
            rows={invites?.results || []}
            columns={[
              { key: "email", label: "Email" },
              { key: "role", label: "Role" },
              { key: "token", label: "Token" },
            ]}
          />
        </div>
      </div>
    </div>
  );
}
