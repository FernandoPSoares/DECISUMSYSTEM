// frontend/src/features/inventory/dashboard/InventoryDashboardPage.jsx

import React from 'react';
// --- ÍCONES CORRIGIDOS ---
// Importamos ícones que realmente existem na biblioteca Heroicons.
import { 
    CubeIcon, 
    DocumentChartBarIcon, 
    ExclamationTriangleIcon, 
    ClipboardDocumentListIcon, 
    PlusCircleIcon,
    ArrowsRightLeftIcon
} from '@heroicons/react/24/outline';

// Componente para os cartões de KPI
const KpiCard = ({ title, value, icon: Icon, variant = 'default' }) => {
    const variants = {
        default: 'bg-indigo-100 text-indigo-600',
        warning: 'bg-yellow-100 text-yellow-600',
        danger: 'bg-red-100 text-red-600',
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
            <div className="flex justify-between items-start">
                <div>
                    <p className="text-sm font-medium text-gray-500">{title}</p>
                    <p className="mt-1 text-3xl font-bold text-gray-900">{value}</p>
                </div>
                <div className={`p-2 rounded-lg ${variants[variant]}`}>
                    <Icon className="w-6 h-6" />
                </div>
            </div>
        </div>
    );
};


// Componente para os botões de Ação Rápida
const ActionButton = ({ title, icon: Icon, onClick }) => (
    <button
        onClick={onClick}
        className="w-full p-6 bg-white rounded-xl shadow-md border border-gray-200 flex flex-col items-center justify-center text-center hover:shadow-lg hover:border-indigo-300 transition-all duration-300 group"
    >
        <div className="p-3 bg-gray-100 rounded-full group-hover:bg-indigo-100 transition-colors">
            <Icon className="w-8 h-8 text-indigo-500 transition-colors group-hover:text-indigo-600"/>
        </div>
        <span className="mt-3 text-sm font-semibold text-gray-700">{title}</span>
    </button>
);

export default function InventoryDashboardPage() {
    return (
        <div className="p-6 sm:p-8">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Painel Geral de Inventário</h1>
                <p className="mt-1 text-sm text-gray-600">Uma visão geral do estado e das operações do seu inventário.</p>
            </header>

            {/* Secção de KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KpiCard title="Valor do Inventário" value="152.3k €" icon={DocumentChartBarIcon} />
                <KpiCard title="Itens (SKUs)" value="852" icon={CubeIcon} />
                <KpiCard title="Itens com Stock Baixo" value="18" icon={ExclamationTriangleIcon} variant="warning" />
                <KpiCard title="Contagens em Aberto" value="2" icon={ClipboardDocumentListIcon} />
            </div>
            
            {/* Secção de Ações Rápidas */}
            <div className="mt-12">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Ações Rápidas</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                    {/* Este ícone de 'Círculo com Mais' é um padrão universal para "Adicionar Novo" */}
                    <ActionButton title="Novo Produto" icon={PlusCircleIcon} onClick={() => alert("Abrir formulário de novo produto")} />
                    <ActionButton title="Iniciar Contagem" icon={ClipboardDocumentListIcon} onClick={() => alert("Iniciar contagem de stock")} />
                    <ActionButton title="Nova Transferência" icon={ArrowsRightLeftIcon} onClick={() => alert("Iniciar nova transferência")} />
                </div>
            </div>
        </div>
    );
}

