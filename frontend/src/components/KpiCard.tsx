import type { ReactNode } from "react";

export function KpiCard({
  label,
  value,
  hint,
  icon,
}: {
  label: string;
  value: ReactNode;
  hint?: string;
  icon?: ReactNode;
}) {
  return (
    <div className="rounded-lg border border-ink-700 bg-ink-850/80 p-3 shadow-panel">
      <div className="flex items-center justify-between text-[11px] uppercase tracking-wider text-mist-500">
        <span>{label}</span>
        {icon}
      </div>
      <div className="mt-1 font-mono text-2xl font-semibold text-mist-100">{value}</div>
      {hint && <div className="mt-1 text-[11px] text-mist-500">{hint}</div>}
    </div>
  );
}
