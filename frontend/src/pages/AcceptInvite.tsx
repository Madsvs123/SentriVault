import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";

export function AcceptInvite() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ token: "", display_name: "", password: "" });
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    try {
      const { data } = await api.post("/auth/accept-invite/", form);
      localStorage.setItem("sv_access", data.access);
      localStorage.setItem("sv_refresh", data.refresh);
      navigate("/");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Invitation could not be accepted.");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <form onSubmit={submit} className="w-full max-w-md rounded-xl border border-ink-700 bg-ink-900 p-6 shadow-panel">
        <h1 className="mb-4 text-lg font-semibold">Accept staff invitation</h1>
        <label className="mb-3 block text-xs text-mist-500">
          Invitation token
          <input className="mt-1 w-full rounded px-3 py-2 font-mono text-sm" value={form.token} onChange={(e) => setForm({ ...form, token: e.target.value })} />
        </label>
        <label className="mb-3 block text-xs text-mist-500">
          Display name
          <input className="mt-1 w-full rounded px-3 py-2 text-sm" value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} />
        </label>
        <label className="mb-3 block text-xs text-mist-500">
          Password
          <input type="password" className="mt-1 w-full rounded px-3 py-2 text-sm" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        </label>
        {error && <div className="mb-3 text-xs text-rose-300">{error}</div>}
        <button className="w-full rounded bg-accent-500 py-2 text-sm font-medium text-ink-950">Join organization</button>
        <Link to="/login" className="mt-4 block text-center text-xs text-mist-500">
          Back to sign in
        </Link>
      </form>
    </div>
  );
}
