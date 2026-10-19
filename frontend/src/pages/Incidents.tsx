import { format } from "date-fns";
import { useNavigate } from "react-router-dom";
import { Badge } from "../components/Badge";
import { DataTable } from "../components/DataTable";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { IncidentRecord, Paginated } from "../types";

export function Incidents() {
  const { data } = useApi<Paginated<IncidentRecord>>("/incidents/");
  const navigate = useNavigate();
  return (
    <div>
      <PageHeader title="Incidents" subtitle="Grouped alerts with owners, tasks, evidence, and status history" />
      <DataTable
        rows={data?.results || []}
        onRow={(row) => navigate(`/incidents/${row.id}`)}
        columns={[
          { key: "created_at", label: "Opened", render: (r) => format(new Date(r.created_at), "MMM d HH:mm") },
          { key: "priority", label: "Priority", render: (r) => <Badge value={r.priority} /> },
          { key: "status", label: "Status", render: (r) => <Badge value={r.status} /> },
          { key: "title", label: "Incident" },
          { key: "owner_email", label: "Owner" },
        ]}
      />
    </div>
  );
}
