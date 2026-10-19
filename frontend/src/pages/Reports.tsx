import { PageHeader } from "../components/PageHeader";
import { DataTable } from "../components/DataTable";
import { Badge } from "../components/Badge";
import { useApi } from "../hooks/useApi";
import type { Paginated } from "../types";
import api from "../api/client";

export function Reports() {
  const { data, reload } = useApi<Paginated<any>>("/reports/");
  return (
    <div>
      <PageHeader
        title="Reports"
        subtitle="Executive, alert, incident, asset, and detection coverage reports"
        actions={
          <button
            className="rounded bg-accent-500 px-3 py-1.5 text-xs text-ink-950"
            onClick={async () => {
              await api.post("/reports/", { name: "Daily SOC brief", report_type: "executive" });
              reload();
            }}
          >
            Generate executive report
          </button>
        }
      />
      <DataTable
        rows={data?.results || []}
        columns={[
          { key: "name", label: "Report" },
          { key: "report_type", label: "Type" },
          { key: "status", label: "Status", render: (r) => <Badge value={r.status === "completed" ? "resolved" : "new"} /> },
          { key: "created_at", label: "Created" },
        ]}
      />
    </div>
  );
}
