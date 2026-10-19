import { create } from "zustand";
import api from "../api/client";
import type { Membership, User } from "../types";

interface AuthState {
  user: User | null;
  memberships: Membership[];
  organizationId: string | null;
  loading: boolean;
  login: (email: string, password: string, otp?: string) => Promise<void>;
  register: (payload: Record<string, string>) => Promise<void>;
  loadMe: () => Promise<void>;
  logout: () => Promise<void>;
  setOrganization: (id: string) => void;
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  memberships: [],
  organizationId: localStorage.getItem("sv_org"),
  loading: false,
  async login(email, password, otp) {
    const { data } = await api.post("/auth/login/", { email, password, otp });
    localStorage.setItem("sv_access", data.access);
    localStorage.setItem("sv_refresh", data.refresh);
    const orgId = data.memberships?.[0]?.organization_id;
    if (orgId) localStorage.setItem("sv_org", orgId);
    set({ user: data.user, memberships: data.memberships || [], organizationId: orgId });
  },
  async register(payload) {
    const { data } = await api.post("/auth/register/", payload);
    localStorage.setItem("sv_access", data.access);
    localStorage.setItem("sv_refresh", data.refresh);
    localStorage.setItem("sv_org", data.organization.id);
    set({ user: data.user, organizationId: data.organization.id });
  },
  async loadMe() {
    if (!localStorage.getItem("sv_access")) return;
    const { data } = await api.get("/auth/me/");
    set({ user: data.user, memberships: data.memberships || [] });
  },
  async logout() {
    try {
      await api.post("/auth/logout/", { refresh: localStorage.getItem("sv_refresh") });
    } finally {
      localStorage.clear();
      set({ user: null, memberships: [], organizationId: null });
    }
  },
  setOrganization(id) {
    localStorage.setItem("sv_org", id);
    set({ organizationId: id });
  },
}));
