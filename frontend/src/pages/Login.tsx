import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Shield } from "lucide-react";
import { useAuth } from "../store/auth";

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("analyst@sentrivault.local");
  const [password, setPassword] = useState("ChangeMe!234");
  const [otp, setOtp] = useState("");
  const [needsMfa, setNeedsMfa] = useState(false);
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password, otp);
      navigate("/");
    } catch (err: any) {
      const data = err.response?.data;
      if (data?.mfa_required || JSON.stringify(data).includes("mfa_required")) {
        setNeedsMfa(true);
        return;
      }
      setError(data?.detail || "Unable to authenticate.");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <form onSubmit={submit} className="w-full max-w-md rounded-xl border border-ink-700 bg-ink-900 p-6 shadow-panel">
        <div className="mb-6 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent-500/15 text-accent-400">
            <Shield size={18} />
          </div>
          <div>
            <div className="text-lg font-semibold">SentriVault</div>
            <div className="text-xs text-mist-500">Security operations console</div>
          </div>
        </div>
        <label className="mb-3 block text-xs text-mist-500">
          Email
          <input className="mt-1 w-full rounded px-3 py-2 text-sm" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label className="mb-3 block text-xs text-mist-500">
          Password
          <input type="password" className="mt-1 w-full rounded px-3 py-2 text-sm" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        {needsMfa && (
          <label className="mb-3 block text-xs text-mist-500">
            MFA code
            <input className="mt-1 w-full rounded px-3 py-2 font-mono text-sm" value={otp} onChange={(e) => setOtp(e.target.value)} />
          </label>
        )}
        {error && <div className="mb-3 text-xs text-rose-300">{error}</div>}
        <button className="w-full rounded bg-accent-500 py-2 text-sm font-medium text-ink-950">Sign in</button>
        <div className="mt-4 flex justify-between text-xs text-mist-500">
          <Link to="/register">Create organization</Link>
          <Link to="/invite">Accept invitation</Link>
        </div>
      </form>
    </div>
  );
}
