import axios from "axios";

const api = axios.create({
  baseURL: "/api/v1",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("sv_access");
  const org = localStorage.getItem("sv_org");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  if (org) config.headers["X-Organization-Id"] = org;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401 && localStorage.getItem("sv_refresh")) {
      try {
        const { data } = await axios.post("/api/v1/auth/refresh/", {
          refresh: localStorage.getItem("sv_refresh"),
        });
        localStorage.setItem("sv_access", data.access);
        error.config.headers.Authorization = `Bearer ${data.access}`;
        return api.request(error.config);
      } catch {
        localStorage.clear();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
