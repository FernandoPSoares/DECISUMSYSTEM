// frontend/src/features/inventory/products/ProductManagementPage.jsx

import React, { useState } from 'react';
import Tabs from '../../../components/ui/Tabs';
import { Cog6ToothIcon, TagIcon } from '@heroicons/react/24/outline'; // <-- NOVO ÍCONE
import Modal from '../../../components/ui/Modal';
import UdmManager from './components/UdmManager';
import MarcasManager from './brands/MarcasManager'; // <-- NOVO COMPONENTE

const PlaceholderTab = ({ title }) => (
    <div className="p-8 text-center bg-white rounded-lg shadow-md border border-gray-200">
        <p className="text-gray-500">A funcionalidade de {title} será implementada aqui.</p>
    </div>
);

export default function ProductManagementPage() {
    const [activeTab, setActiveTab] = useState('produtos');
    const [isUdmModalOpen, setIsUdmModalOpen] = useState(false);
    // --- NOVO ESTADO PARA O MODAL DE MARCAS ---
    const [isMarcaModalOpen, setIsMarcaModalOpen] = useState(false);

    // --- ABAS ATUALIZADAS CONFORME O PEDIDO ---
    const tabs = [
        { id: 'produtos', name: 'Produtos' },
        { id: 'variantes', name: 'Variantes' },
        { id: 'categorias', name: 'Categorias de Produto' },
        { id: 'lotes', name: 'Lotes' },
        { id: 'pacotes', name: 'Pacotes' },
    ];

    return (
        <>
            <div className="p-6 sm:p-8">
                <header className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Gestão de Produtos</h1>
                        <p className="mt-1 text-sm text-gray-600">Gira o seu catálogo completo, desde as unidades de medida até aos produtos finais.</p>
                    </div>
                    {/* --- NOVOS BOTÕES DE CONFIGURAÇÃO --- */}
                    <div className="flex items-center space-x-2">
                        <button 
                            className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50"
                            onClick={() => setIsUdmModalOpen(true)}
                        >
                            <Cog6ToothIcon className="w-5 h-5 mr-2" />
                            Gerir UdM
                        </button>
                        <button 
                            className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50"
                            onClick={() => setIsMarcaModalOpen(true)}
                        >
                            <TagIcon className="w-5 h-5 mr-2" />
                            Gerir Marcas
                        </button>
                    </div>
                </header>

                <Tabs tabs={tabs} activeTab={activeTab} onTabClick={setActiveTab} />

                <div className="mt-6">
                    {activeTab === 'produtos' && <PlaceholderTab title="Produtos" />}
                    {activeTab === 'variantes' && <PlaceholderTab title="Variantes" />}
                    {activeTab === 'categorias' && <PlaceholderTab title="Categorias de Produto" />}
                    {activeTab === 'lotes' && <PlaceholderTab title="Lotes" />}
                    {activeTab === 'pacotes' && <PlaceholderTab title="Pacotes" />}
                </div>
            </div>

            <Modal 
                isOpen={isUdmModalOpen} 
                onClose={() => setIsUdmModalOpen(false)} 
                title="Configuração de Unidades de Medida"
            >
                <UdmManager />
            </Modal> 

            {/* --- NOVO MODAL PARA GERIR MARCAS --- */}
            <Modal 
                isOpen={isMarcaModalOpen} 
                onClose={() => setIsMarcaModalOpen(false)} 
                title="Configuração de Marcas"
            >
                <MarcasManager />
            </Modal>
        </>
    );
}
