// File: frontend/src/features/maintenance/layout/MaintenanceLayout.jsx
import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/AuthContext';
import { 
  ArrowLeft, 
  LayoutDashboard, 
  ListTodo, 
  HardDrive, 
  Settings 
} from 'lucide-react';

/**
 * MaintenanceLayout é o componente "casca" (shell) para todo o módulo CMMS.
 * Renderiza a Sidebar, o Header e o conteúdo da página filha (<Outlet />).
 */
const MaintenanceLayout = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  // Ação de voltar para a seleção de módulos
  const handleBack = () => navigate('/');

  // Ação de logout
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Links de navegação específicos do módulo de Manutenção
  const navLinks = [
    { name: 'Dashboard', href: '/maintenance/dashboard', icon: LayoutDashboard },
    { name: 'Ordens de Serviço', href: '/maintenance/work-orders', icon: ListTodo },
    { name: 'Ativos', href: '/maintenance/assets', icon: HardDrive },
    { name: 'Configurações', href: '/maintenance/settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-white shadow-md flex-shrink-0 flex flex-col">
        <div className="p-4 border-b flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-xl font-bold text-gray-800">CMMS</h2>
            <span className="text-xs text-gray-500 uppercase tracking-wider">Manutenção</span>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {navLinks.map((link) => (
            <NavLink
              key={link.name}
              to={link.href}
              className={({ isActive }) =>
                `flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 group ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 shadow-sm' // Estilo ativo
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900' // Estilo inativo
                }`
              }
            >
              <link.icon className={`w-5 h-5 mr-3 transition-colors ${
                // Ícone muda de cor se ativo (lógica CSS inline simplificada pelo NavLink class)
                '' 
              }`} />
              {link.name}
            </NavLink>
          ))}
        </nav>
        
        {/* Footer da Sidebar (Opcional - info do utilizador ou versão) */}
        <div className="p-4 border-t text-xs text-gray-400 text-center">
            v1.0.0
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header (Top Bar) */}
        <header className="flex items-center justify-between px-6 py-4 bg-white border-b shadow-sm z-10">
          <button
            onClick={handleBack}
            className="flex items-center text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar aos Módulos
          </button>
          
          <div className="flex items-center space-x-4">
             {/* Aqui poderíamos ter notificações, perfil, etc. */}
            <button
                onClick={handleLogout}
                className="text-sm font-medium text-red-500 hover:text-red-700 transition-colors"
            >
                Sair
            </button>
          </div>
        </header>

        {/* Page Content (Renderiza a rota filha, ex: WorkOrderListPage) */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-6">
          <div className="max-w-7xl mx-auto">
             <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default MaintenanceLayout;