// frontend/src/features/inventory/products/ProductManagementPage.jsx

import React, { useState } from 'react';
import Tabs from '../../../components/ui/Tabs';
import { Cog6ToothIcon } from '@heroicons/react/24/outline';
import Modal from '../../../components/ui/Modal'; // <-- Importamos o nosso Modal
import UdmManager from './components/UdmManager'; // <-- Importamos o nosso novo gestor de UDM

const PlaceholderTab = ({ title }) => (
    <div className="p-8 text-center bg-white rounded-lg shadow-md border border-gray-200">
        <p className="text-gray-500">A funcionalidade de {title} será implementada aqui.</p>
    </div>
);

export default function ProductManagementPage() {
    const [activeTab, setActiveTab] = useState('produtos');
    
    // --- ESTADO PARA CONTROLAR O MODAL DE UDM ---
    const [isUdmModalOpen, setIsUdmModalOpen] = useState(false);

    const tabs = [
        { id: 'produtos', name: 'Produtos & Variantes' },
        { id: 'categorias', name: 'Categorias de Produto' },
    ];

    return (
        <>
            <div className="p-6 sm:p-8">
                <header className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Gestão de Produtos</h1>
                        <p className="mt-1 text-sm text-gray-600">Gira o seu catálogo completo, desde as unidades de medida até aos produtos finais.</p>
                    </div>
                    {/* Botão para abrir o modal de gestão de UDM */}
                    <button 
                        className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50"
                        onClick={() => setIsUdmModalOpen(true)}
                    >
                        <Cog6ToothIcon className="w-5 h-5 mr-2" />
                        Gerir Unidades de Medida
                    </button>
                </header>

                <Tabs tabs={tabs} activeTab={activeTab} onTabClick={setActiveTab} />

                <div className="mt-6">
                    {activeTab === 'produtos' && <PlaceholderTab title="Produtos & Variantes" />}
                    {activeTab === 'categorias' && <PlaceholderTab title="Categorias de Produto" />}
                </div>
            </div>

            {/* --- INTEGRAÇÃO FINAL DO MODAL --- */}
            {/* O nosso Modal agora envolve o UdmManager. */}
            <Modal 
                isOpen={isUdmModalOpen} 
                onClose={() => setIsUdmModalOpen(false)} 
                title="Configuração de Unidades de Medida"
            >
                <UdmManager />
            </Modal> 
        </>
    );
}

