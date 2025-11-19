// frontend/src/router/AppRouter.jsx

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import PropTypes from 'prop-types';

// Importa os nossos layouts de módulo
import AdminLayout from '../features/administration/layout/AdminLayout';
import InventoryLayout from '../features/inventory/layout/InventoryLayout';
import MaintenanceLayout from '../features/maintenance/layout/MaintenanceLayout';

// Importa TODAS as nossas páginas
import LoginPage from '../features/auth/LoginPage';
import ForgotPasswordPage from '../features/auth/ForgotPasswordPage';
import ResetPasswordPage from '../features/auth/ResetPasswordPage';
import ModuleSelectionPage from '../features/dashboard/ModuleSelectionPage';
import UserListPage from '../features/administration/users/UserListPage';
import RoleListPage from '../features/administration/roles/RoleListPage';
import InventoryDashboardPage from '../features/inventory/dashboard/InventoryDashboardPage';
import ProductManagementPage from '../features/inventory/products/ProductManagementPage';

// --- PÁGINAS DO MÓDULO DE MANUTENÇÃO (CMMS) ---
import MaintenanceDashboardPage from '../features/maintenance/dashboard/MaintenanceDashboardPage';
import WorkOrderListPage from '../features/maintenance/work_orders/WorkOrderListPage';
import WorkOrderDetailPage from '../features/maintenance/work_orders/WorkOrderDetailPage'; // <--- NOVO IMPORT
import AssetManagementPage from '../features/maintenance/assets/AssetManagementPage';
import MaintenanceSettingsPage from '../features/maintenance/settings/MaintenanceSettingsPage';
import AssetDetailPage from '../features/maintenance/assets/AssetDetailPage';

// Componente "Segurança"
function ProtectedRoute({ children }) {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired,
};

export default function AppRouter() {
  const { token } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        {/* --- ROTAS PÚBLICAS --- */}
        <Route path="/login" element={token ? <Navigate to="/" replace /> : <LoginPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />

        {/* --- ROTAS PROTEGIDAS --- */}
        <Route element={<ProtectedRoute><Outlet /></ProtectedRoute>}>
            
            <Route path="/" element={<ModuleSelectionPage />} />
            
            {/* Grupo de Administração */}
            <Route path="/administration" element={<AdminLayout />}>
                <Route index element={<Navigate to="users" replace />} />
                <Route path="users" element={<UserListPage />} />
                <Route path="roles" element={<RoleListPage />} />
            </Route>
            
            {/* Grupo de Inventário */}
            <Route path="/inventory" element={<InventoryLayout />}>
                <Route index element={<InventoryDashboardPage />} />
                <Route path="products" element={<ProductManagementPage />} />
            </Route>

            {/* --- GRUPO DE ROTAS DE MANUTENÇÃO (CMMS) --- */}
            <Route path="/maintenance" element={<MaintenanceLayout />}>
                <Route index element={<Navigate to="dashboard" replace />} />
                
                <Route path="dashboard" element={<MaintenanceDashboardPage />} />
                
                {/* Rotas de Work Orders */}
                <Route path="work-orders" element={<WorkOrderListPage />} />
                <Route path="work-orders/:id" element={<WorkOrderDetailPage />} /> {/* <--- NOVA ROTA */}
                
                <Route path="assets" element={<AssetManagementPage />} />
                <Route path="assets/:id" element={<AssetDetailPage />} />
                <Route path="settings" element={<MaintenanceSettingsPage />} />
            </Route>

        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}