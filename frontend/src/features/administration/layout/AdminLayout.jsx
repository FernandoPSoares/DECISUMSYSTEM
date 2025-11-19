// frontend/src/features/administration/layout/AdminLayout.jsx

import React from 'react';
import { NavLink, Link, Outlet } from 'react-router-dom';
// --- IMPORTAÇÃO CORRIGIDA ---
// Agora precisa de subir 3 níveis para encontrar a pasta 'context'
import { useAuth } from '../../../context/AuthContext'; 
import { 
    UsersIcon, 
    ShieldCheckIcon, 
    ArrowLeftOnRectangleIcon 
} from '@heroicons/react/24/outline';
import PropTypes from 'prop-types';

// Componente para um item da navegação, com estilo para a rota ativa
const NavItem = ({ to, icon: Icon, children }) => {
    const navLinkClasses = `
        flex items-center px-4 py-3 text-gray-200 rounded-lg
        transition-colors duration-200
        hover:bg-gray-700 hover:text-white
    `;
    const activeNavLinkClasses = 'bg-gray-900 text-white';

    return (
        <NavLink
            to={to}
            className={({ isActive }) => `${navLinkClasses} ${isActive ? activeNavLinkClasses : ''}`}
        >
            <Icon className="w-5 h-5 mr-3" />
            <span className="font-medium">{children}</span>
        </NavLink>
    );
};

NavItem.propTypes = {
    to: PropTypes.string.isRequired,
    icon: PropTypes.elementType.isRequired,
    children: PropTypes.node.isRequired,
};

export default function AdminLayout() {
    const { logout } = useAuth();

    return (
        <div className="flex h-screen bg-gray-100 font-sans">
            <aside className="fixed top-0 left-0 w-64 h-full bg-gray-800 text-white flex flex-col z-20">
                <Link 
                    to="/" 
                    className="flex items-center justify-center h-20 border-b border-gray-700 hover:bg-gray-700/50 transition-colors duration-200"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
                    </svg>
                    <h1 className="ml-3 text-xl font-bold tracking-wider">DecisumSystem</h1>
                </Link>
                
                <nav className="flex-1 px-4 py-6 space-y-2">
                    <NavItem to="/administration/users" icon={UsersIcon}>Utilizadores</NavItem>
                    <NavItem to="/administration/roles" icon={ShieldCheckIcon}>Funções</NavItem>
                </nav>

                <div className="px-4 py-4 border-t border-gray-700">
                    <button
                        onClick={logout}
                        className="w-full flex items-center px-4 py-3 text-gray-200 rounded-lg hover:bg-gray-700 hover:text-white transition-colors duration-200"
                    >
                        <ArrowLeftOnRectangleIcon className="w-5 h-5 mr-3" />
                        <span className="font-medium">Sair</span>
                    </button>
                </div>
            </aside>

            <main className="flex-1 ml-64 overflow-y-auto">
                <Outlet />
            </main>
        </div>
    );
}
