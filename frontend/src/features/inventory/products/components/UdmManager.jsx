// frontend/src/features/inventory/products/components/UdmManager.jsx

import React, { useState, useEffect, useCallback } from 'react';
import apiClient from '../../../../api/apiClient';
import { PlusIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast';
import Spinner from '../../../../components/ui/Spinner';
import Modal from '../../../../components/ui/Modal';
import UdmCategoryRow from './UdmCategoryRow';
import CategoriaUdmForm from '../udm/components/CategoriaUdmForm';
import UdmForm from '../udm/components/UdmForm';

export default function UdmManager() {
    const [categories, setCategories] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    
    // Estado para os modais de formulário
    const [isCategoriaModalOpen, setIsCategoriaModalOpen] = useState(false);
    const [isUdmModalOpen, setIsUdmModalOpen] = useState(false);
    const [editingItem, setEditingItem] = useState(null);

    const fetchData = useCallback(async () => {
        setIsLoading(true);
        setError('');
        try {
            const response = await apiClient.get('/inventory/categorias-udm/');
            setCategories(response.data);
        } catch (err) {
            setError('Falha ao buscar os dados de Unidades de Medida.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => { fetchData(); }, [fetchData]);

    // --- Lógica de Abertura de Modais ---
    const handleOpenCategoriaModal = (categoria = null) => {
        setEditingItem(categoria);
        setIsCategoriaModalOpen(true);
    };

    const handleOpenUdmModal = (udm = null, category = null) => {
        const itemToEdit = udm ? udm : { categoria_udm: category };
        setEditingItem(itemToEdit);
        setIsUdmModalOpen(true);
    };

    const handleCloseModals = () => {
        setIsCategoriaModalOpen(false);
        setIsUdmModalOpen(false);
        setEditingItem(null);
    };

    // --- Lógica de "Guardar" ---
    const handleSaveCategoria = async (data) => {
        const isEditing = !!(editingItem && editingItem.is_active !== undefined);
        const promise = isEditing
            ? apiClient.put(`/inventory/categorias-udm/${editingItem.id}`, data)
            : apiClient.post('/inventory/categorias-udm/', data);
        await toast.promise(promise, { loading: 'A guardar...', success: `Categoria ${isEditing ? 'atualizada' : 'criada'}!`, error: (err) => err.response?.data?.detail || 'Ocorreu um erro.' });
        fetchData();
        handleCloseModals();
    };

    const handleSaveUdm = async (data) => {
        const isEditing = !!editingItem.nome;
        const promise = isEditing
            ? apiClient.put(`/inventory/udm/${editingItem.id}`, data)
            : apiClient.post('/inventory/udm/', data);
        await toast.promise(promise, { loading: 'A guardar...', success: `Unidade de Medida ${isEditing ? 'atualizada' : 'criada'}!`, error: (err) => err.response?.data?.detail || 'Ocorreu um erro.' });
        fetchData();
        handleCloseModals();
    };

    return (
        <div className="p-1 sm:p-4">
            <header className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">Gerir Unidades de Medida</h2>
                    <p className="mt-1 text-sm text-gray-600">Gira as categorias e as unidades de medida (UDM) do sistema.</p>
                </div>
                <button 
                    className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700"
                    onClick={() => handleOpenCategoriaModal()}
                >
                    <PlusIcon className="w-5 h-5 mr-2" />
                    Nova Categoria
                </button>
            </header>

            {isLoading && <div className="flex justify-center p-8"><Spinner /></div>}
            {error && <p className="text-center text-red-600">{error}</p>}
            
            {!isLoading && !error && (
                <div className="bg-white shadow-md rounded-lg divide-y divide-gray-200">
                    <div className="grid grid-cols-[250px,1fr] items-center gap-x-6 px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider rounded-t-lg">
                        <span>Categoria</span>
                        <span>Unidades de Medida (UDM)</span>
                    </div>
                    {categories.map(category => (
                        <UdmCategoryRow
                            key={category.id}
                            category={category}
                            onEditCategory={handleOpenCategoriaModal}
                            onEditUdm={(udm) => handleOpenUdmModal(udm)}
                            onAddUdm={(cat) => handleOpenUdmModal(null, cat)}
                        />
                    ))}
                     {categories.length === 0 && <p className="text-center text-gray-500 py-8">Nenhuma categoria encontrada. Clique em "Nova Categoria" para começar.</p>}
                </div>
            )}
            
            {/* Modais de Formulário */}
            <Modal isOpen={isCategoriaModalOpen} onClose={handleCloseModals} title={editingItem ? 'Editar Categoria' : 'Nova Categoria'}>
                <CategoriaUdmForm categoriaToEdit={editingItem} onSave={handleSaveCategoria} onCancel={handleCloseModals} />
            </Modal>
            
            <Modal isOpen={isUdmModalOpen} onClose={handleCloseModals} title={editingItem?.nome ? 'Editar UDM' : 'Nova UDM'}>
                <UdmForm udmToEdit={editingItem} onSave={handleSaveUdm} onCancel={handleCloseModals} />
            </Modal>
        </div>
    );
}

