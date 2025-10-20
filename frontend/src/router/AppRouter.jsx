// frontend/src/router/AppRouter.jsx

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import PropTypes from 'prop-types';

// Importa os nossos layouts de módulo
import AdminLayout from '../features/administration/layout/AdminLayout';
import InventoryLayout from '../features/inventory/layout/InventoryLayout';

// Importa TODAS as nossas páginas
import LoginPage from '../features/auth/LoginPage';
import ForgotPasswordPage from '../features/auth/ForgotPasswordPage';
import ResetPasswordPage from '../features/auth/ResetPasswordPage';
import ModuleSelectionPage from '../features/dashboard/ModuleSelectionPage';
import UserListPage from '../features/administration/users/UserListPage';
import RoleListPage from '../features/administration/roles/RoleListPage';
import InventoryDashboardPage from '../features/inventory/dashboard/InventoryDashboardPage';
import ProductManagementPage from '../features/inventory/products/ProductManagementPage';

// Componente "Segurança": Garante que apenas utilizadores autenticados podem aceder a certas rotas.
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
            
            {/* Grupo de rotas de Administração, que usam o AdminLayout */}
            <Route path="/administration" element={<AdminLayout />}>
                <Route index element={<Navigate to="users" replace />} />
                <Route path="users" element={<UserListPage />} />
                <Route path="roles" element={<RoleListPage />} />
            </Route>
            
            {/* --- GRUPO DE ROTAS DE INVENTÁRIO CORRIGIDO --- */}
            {/* A rota "pai" agora renderiza o InventoryLayout.
                Todas as rotas "filhas" serão renderizadas no seu <Outlet />. */}
            <Route path="/inventory" element={<InventoryLayout />}>
                <Route index element={<InventoryDashboardPage />} />
                <Route path="products" element={<ProductManagementPage />} />
            </Route>

        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

