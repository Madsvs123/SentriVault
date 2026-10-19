import { format } from "date-fns";
import { useNavigate } from "react-router-dom";
import { Badge } from "../components/Badge";
import { DataTable } from "../components/DataTable";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { AlertRecord, Paginated } from "../types";

export function Alerts() {
  const { data } = useApi<Paginated<AlertRecord>>("/alerts/");
  const navigate = useNavigate();
  return (
    <div>
      <PageHeader title="Alerts" subtitle="Assignment, escalation, evidence, and investigation timelines" />
      <DataTable
        rows={data?.results || []}
        onRow={(row) => navigate(`/alerts/${row.id}`)}
        columns={[
          { key: "created_at", label: "Opened", render: (r) => format(new Date(r.created_at), "MMM d HH:mm") },
          { key: "severity", label: "Sev", render: (r) => <Badge value={r.severity} /> },
          { key: "status", label: "Status", render: (r) => <Badge value={r.status} /> },
          { key: "title", label: "Alert" },
          { key: "source_ip", label: "IP" },
          { key: "username", label: "User" },
          { key: "assigned_email", label: "Owner" },
        ]}
      />
    </div>
  );
}
