import clsx from "clsx";

const tones: Record<string, string> = {
  informational: "bg-sky-500/15 text-sky-300 border-sky-500/30",
  low: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  medium: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  high: "bg-orange-500/15 text-orange-300 border-orange-500/30",
  critical: "bg-rose-500/15 text-rose-300 border-rose-500/30",
  new: "bg-accent-500/15 text-accent-400 border-accent-500/30",
  acknowledged: "bg-violet-500/15 text-violet-300 border-violet-500/30",
  investigating: "bg-cyan-500/15 text-cyan-300 border-cyan-500/30",
  escalated: "bg-rose-500/15 text-rose-300 border-rose-500/30",
  resolved: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  suppressed: "bg-zinc-500/15 text-zinc-300 border-zinc-500/30",
  open: "bg-rose-500/15 text-rose-300 border-rose-500/30",
  closed: "bg-zinc-500/15 text-zinc-300 border-zinc-500/30",
};

export function Badge({ value }: { value?: string | null }) {
  if (!value) return null;
  return (
    <span
      className={clsx(
        "inline-flex rounded border px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wide",
        tones[value] || "bg-ink-700 text-mist-300 border-ink-600"
      )}
    >
      {value}
    </span>
  );
}
