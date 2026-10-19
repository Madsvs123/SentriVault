import { useEffect } from "react";

export function useRealtime(path: string, onMessage: (payload: unknown) => void) {
  useEffect(() => {
    const token = localStorage.getItem("sv_access");
    const org = localStorage.getItem("sv_org");
    if (!token || !org) return;
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${protocol}://${window.location.host}${path}${org}/?token=${token}`);
    socket.onmessage = (event) => {
      try {
        onMessage(JSON.parse(event.data));
      } catch {
        onMessage(event.data);
      }
    };
    return () => socket.close();
  }, [path, onMessage]);
}
