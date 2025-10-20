// frontend/src/features/dashboard/ModuleSelectionPage.jsx

import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

// O nosso componente de cartão de módulo, já otimizado para o design minimalista.
const ModuleCard = ({ to, title, icon, disabled = false }) => {
    const content = (
        <div className={`
            p-6 bg-white rounded-xl shadow-md border border-gray-200 
            flex flex-col items-center justify-center text-center h-full
            transition-all duration-300
            ${disabled 
                ? 'opacity-50 cursor-not-allowed bg-gray-50' 
                : 'hover:shadow-lg hover:scale-105 hover:border-indigo-300'
            }
        `}>
            {icon}
            <h3 className="mt-4 text-lg font-semibold text-gray-800">{title}</h3>
        </div>
    );
    
    return disabled ? <div>{content}</div> : <Link to={to}>{content}</Link>;
};

export default function ModuleSelectionPage() {
    const { logout } = useAuth();

    // --- ÍCONES ATUALIZADOS E MAIS CONDICENTES ---
    
    const AdminIcon = (
        <svg xmlns="http://www.w3.org/2000/svg" className="w-12 h-12 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-9.75 0h9.75" />
        </svg>
    );
    const InventoryIcon = (
        <svg xmlns="http://www.w3.org/2000/svg" className="w-12 h-12 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
        </svg>
    );
    const PurchasingIcon = ( // Ícone de "Cartão de Crédito", como solicitado
        <svg xmlns="http://www.w3.org/2000/svg" className="w-13 h-12 text-indigo-500" fill="none" viewBox="0 0 25 25" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.5 3.75h17.25a2.25 2.25 0 002.25-2.25v-13.5a2.25 2.25 0 00-2.25-2.25H3.75a2.25 2.25 0 00-2.25 2.25v13.5a2.25 2.25 0 002.25 2.25z" />
        </svg>
    );
    const ProductionIcon = ( // Ícone de "Engrenagem", como solicitado
        <svg xmlns="http://www.w3.org/2000/svg" className="w-12 h-12 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <circle cx="12" cy="12" r="4"></circle>
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
        </svg>
    );

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
                    <h1 className="text-2xl font-bold text-gray-900">Módulos do Sistema</h1>
                    <button
                        onClick={logout}
                        className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none"
                    >
                        Sair
                    </button>
                </div>
            </header>
            <main className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 auto-rows-fr">
                    <ModuleCard 
                        to="/administration/users" 
                        title="Administração" 
                        icon={AdminIcon}
                    />
                    <ModuleCard 
                        to="/inventory" 
                        title="Inventário" 
                        icon={InventoryIcon}
                        disabled={false}
                    />
                    <ModuleCard 
                        to="#" 
                        title="Compras" 
                        icon={PurchasingIcon}
                        disabled={true}
                    />
                     <ModuleCard 
                        to="#" 
                        title="Produção" 
                        icon={ProductionIcon}
                        disabled={true}
                    />
                </div>
            </main>
        </div>
    );
}

