import type { ReactNode } from "react";

export function DataTable({
  columns,
  rows,
  onRow,
}: {
  columns: { key: string; label: string; render?: (row: any) => ReactNode }[];
  rows: any[];
  onRow?: (row: any) => void;
}) {
  return (
    <div className="overflow-auto rounded-lg border border-ink-700 bg-ink-850/70">
      <table className="table-dense w-full text-left text-xs">
        <thead className="sticky top-0 bg-ink-800 text-[10px] uppercase tracking-wider text-mist-500">
          <tr>
            {columns.map((col) => (
              <th key={col.key}>{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.id || idx}
              onClick={() => onRow?.(row)}
              className="cursor-pointer border-t border-ink-700/80 hover:bg-ink-800/80"
            >
              {columns.map((col) => (
                <td key={col.key} className="text-mist-100">
                  {col.render ? col.render(row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
          {!rows.length && (
            <tr>
              <td colSpan={columns.length} className="py-8 text-center text-mist-500">
                No records in the current scope.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
