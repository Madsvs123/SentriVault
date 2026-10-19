import { useEffect, useState } from "react";
import api from "../api/client";

export function useApi<T>(url: string | null, deps: unknown[] = []) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(Boolean(url));
  const [error, setError] = useState<string | null>(null);

  const reload = () => {
    if (!url) return;
    setLoading(true);
    api
      .get<T>(url)
      .then((res) => setData(res.data))
      .catch((err) => setError(err.response?.data?.detail || err.message))
      .finally(() => setLoading(false));
  };

  useEffect(reload, [url, ...deps]);
  return { data, loading, error, reload, setData };
}
