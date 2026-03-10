import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import AppLayout from "../components/layout/AppLayout";

import DashboardPage from "../pages/dashboard/DashboardPage";
import ReportsListPage from "../pages/reports/ReportsListPage";
import ReportDetailPage from "../pages/reports/ReportDetailPage";
import GenerateReportPage from "../pages/reports/GenerateReportPage";

import UpgradePage from "../pages/upgrade/UpgradePage";
import BillingPage from "../pages/billing/BillingPage";
import SettingsPage from "../pages/settings/SettingsPage";

import AdminUsersPage from "../pages/admin/AdminUsersPage";

import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";

import NotFoundPage from "../pages/errors/NotFoundPage";
import ForbiddenPage from "../pages/errors/ForbiddenPage";

import ProtectedRoute from "../components/ProtectedRoute";
import AdminRoute from "./AdminRoute";

export default function AppRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
        Loading...
      </div>
    );
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={user ? <Navigate to="/dashboard" replace /> : <LoginPage />}
      />

      <Route
        path="/register"
        element={user ? <Navigate to="/dashboard" replace /> : <RegisterPage />}
      />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="reports" element={<ReportsListPage />} />
        <Route path="reports/:id" element={<ReportDetailPage />} />
        <Route path="generate-report" element={<GenerateReportPage />} />
        <Route path="settings" element={<SettingsPage />} />
        <Route path="upgrade" element={<UpgradePage />} />
        <Route path="billing" element={<BillingPage />} />

        <Route
          path="admin"
          element={
            <AdminRoute>
              <Navigate to="/admin/users" replace />
            </AdminRoute>
          }
        />

        <Route
          path="admin/users"
          element={
            <AdminRoute>
              <AdminUsersPage />
            </AdminRoute>
          }
        />
      </Route>

      <Route path="/forbidden" element={<ForbiddenPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
