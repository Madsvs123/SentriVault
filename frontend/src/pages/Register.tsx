import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../store/auth";

export function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    organization_name: "",
    organization_slug: "",
    email: "",
    password: "",
    display_name: "",
  });
  const [error, setError] = useState("");

  function set<K extends keyof typeof form>(key: K, value: string) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    try {
      await register(form);
      navigate("/");
    } catch (err: any) {
      setError(JSON.stringify(err.response?.data || "Registration failed"));
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <form onSubmit={submit} className="w-full max-w-md rounded-xl border border-ink-700 bg-ink-900 p-6 shadow-panel">
        <h1 className="mb-4 text-lg font-semibold">Create a SentriVault tenant</h1>
        {Object.entries(form).map(([key, value]) => (
          <label key={key} className="mb-3 block text-xs capitalize text-mist-500">
            {key.replaceAll("_", " ")}
            <input
              type={key === "password" ? "password" : "text"}
              className="mt-1 w-full rounded px-3 py-2 text-sm"
              value={value}
              onChange={(e) => set(key as keyof typeof form, e.target.value)}
            />
          </label>
        ))}
        {error && <div className="mb-3 text-xs text-rose-300">{error}</div>}
        <button className="w-full rounded bg-accent-500 py-2 text-sm font-medium text-ink-950">Create organization</button>
        <Link to="/login" className="mt-4 block text-center text-xs text-mist-500">
          Back to sign in
        </Link>
      </form>
    </div>
  );
}
