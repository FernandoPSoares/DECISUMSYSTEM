// frontend/src/features/inventory/layout/InventoryLayout.jsx

import React from 'react';
import { NavLink, Link, Outlet } from 'react-router-dom';
import { useAuth } from '../../../context/AuthContext';
import { 
    ChartPieIcon, 
    CubeIcon, 
    ArrowLeftOnRectangleIcon 
} from '@heroicons/react/24/outline';
import PropTypes from 'prop-types';

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

export default function InventoryLayout() {
    const { logout } = useAuth();

    return (
        <div className="flex h-screen bg-gray-100 font-sans">
            <aside className="fixed top-0 left-0 w-64 h-full bg-gray-800 text-white flex flex-col z-20">
                <Link to="/" className="flex items-center justify-center h-20 border-b border-gray-700 hover:bg-gray-700/50">
                    {/* ... (logótipo) ... */}
                    <h1 className="ml-3 text-xl font-bold tracking-wider">DecisumSystem</h1>
                </Link>
                
                <nav className="flex-1 px-4 py-6 space-y-2">
                    <NavItem to="/inventory" icon={ChartPieIcon}>Painel Geral</NavItem>
                    {/* --- LINK CORRIGIDO --- */}
                    {/* O link agora aponta para a nossa página "hub" de produtos */}
                    <NavItem to="/inventory/products" icon={CubeIcon}>Produtos</NavItem>
                </nav>

                <div className="px-4 py-4 border-t border-gray-700">
                    <button onClick={logout} className="w-full flex items-center px-4 py-3 ...">
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

