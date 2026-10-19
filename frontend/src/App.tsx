import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./layouts/AppShell";
import { AcceptInvite } from "./pages/AcceptInvite";
import { AlertDetail } from "./pages/AlertDetail";
import { Alerts } from "./pages/Alerts";
import { AssetDetail } from "./pages/AssetDetail";
import { Assets } from "./pages/Assets";
import { EventDetail } from "./pages/EventDetail";
import { Events } from "./pages/Events";
import { IncidentDetail } from "./pages/IncidentDetail";
import { Incidents } from "./pages/Incidents";
import { Indicators } from "./pages/Indicators";
import { Investigations } from "./pages/Investigations";
import { Login } from "./pages/Login";
import { Overview } from "./pages/Overview";
import { Register } from "./pages/Register";
import { Reports } from "./pages/Reports";
import { Rules } from "./pages/Rules";
import { Settings } from "./pages/Settings";
import { UsersPage } from "./pages/Users";

function Guard({ children }: { children: React.ReactNode }) {
  if (!localStorage.getItem("sv_access")) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/invite" element={<AcceptInvite />} />
      <Route
        element={
          <Guard>
            <AppShell />
          </Guard>
        }
      >
        <Route path="/" element={<Overview />} />
        <Route path="/events" element={<Events />} />
        <Route path="/events/:id" element={<EventDetail />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/alerts/:id" element={<AlertDetail />} />
        <Route path="/incidents" element={<Incidents />} />
        <Route path="/incidents/:id" element={<IncidentDetail />} />
        <Route path="/assets" element={<Assets />} />
        <Route path="/assets/:id" element={<AssetDetail />} />
        <Route path="/rules" element={<Rules />} />
        <Route path="/indicators" element={<Indicators />} />
        <Route path="/investigations" element={<Investigations />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
