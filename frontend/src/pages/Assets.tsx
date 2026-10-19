import { useNavigate } from "react-router-dom";
import { Badge } from "../components/Badge";
import { DataTable } from "../components/DataTable";
import { PageHeader } from "../components/PageHeader";
import { useApi } from "../hooks/useApi";
import type { AssetRecord, Paginated } from "../types";

export function Assets() {
  const { data } = useApi<Paginated<AssetRecord>>("/assets/");
  const navigate = useNavigate();
  return (
    <div>
      <PageHeader title="Assets" subtitle="Hosts, owners, criticality, last-seen, and vulnerability metadata" />
      <DataTable
        rows={data?.results || []}
        onRow={(row) => navigate(`/assets/${row.id}`)}
        columns={[
          { key: "hostname", label: "Host" },
          { key: "ip_address", label: "IP" },
          { key: "operating_system", label: "OS" },
          { key: "owner", label: "Owner" },
          { key: "criticality", label: "Criticality", render: (r) => <Badge value={r.criticality} /> },
          { key: "vulnerability_count", label: "Vulns" },
          { key: "event_count", label: "Events" },
          { key: "last_seen_at", label: "Last seen" },
        ]}
      />
    </div>
  );
}
