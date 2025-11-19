// frontend/src/features/inventory/products/brands/MarcasManager.jsx

import React, { useState, useEffect, useCallback } from 'react';
import apiClient from '../../../../api/apiClient';
import DataTable from '../../../../components/ui/table/DataTable';
import Modal from '../../../../components/ui/Modal';
import ConfirmationModal from '../../../../components/ui/ConfirmationModal';
import { PlusIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast';
import MarcaForm from './components/MarcaForm';
import Spinner from '../../../../components/ui/Spinner';

export default function MarcasManager() {
    const [marcas, setMarcas] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    
    const [isFormModalOpen, setIsFormModalOpen] = useState(false);
    const [editingMarca, setEditingMarca] = useState(null);
    
    const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
    const [marcaToConfirm, setMarcaToConfirm] = useState(null);
    const [isConfirming, setIsConfirming] = useState(false);
    
    const [sortConfig, setSortConfig] = useState({ key: 'nome', direction: 'asc' });

    const fetchMarcas = useCallback(async () => {
        setIsLoading(true);
        setError('');
        try {
            const params = new URLSearchParams({
                sort_by: sortConfig.key,
                sort_order: sortConfig.direction,
            });
            const response = await apiClient.get(`/inventory/brands/?${params.toString()}`);
            setMarcas(response.data);
        } catch (err) {
            setError('Falha ao buscar as marcas.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    }, [sortConfig]);

    useEffect(() => {
        fetchMarcas();
    }, [fetchMarcas]);

    const columns = [
        { header: 'ID', accessor: 'id', sortable: true },
        { header: 'Nome da Marca', accessor: 'nome', sortable: true },
        {
            header: 'Status', accessor: 'is_active', sortable: true, cell: (row) => (
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${row.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {row.is_active ? 'Ativo' : 'Inativo'}
                </span>
            )
        },
    ];

    const handleOpenFormModal = (marca = null) => {
        setEditingMarca(marca);
        setIsFormModalOpen(true);
    };

    const handleCloseFormModal = () => {
        setEditingMarca(null);
        setIsFormModalOpen(false);
    };

    const handleSaveMarca = async (data) => {
        const isEditing = !!editingMarca;
        const promise = isEditing
            ? apiClient.put(`/inventory/brands/${editingMarca.id}`, data)
            : apiClient.post('/inventory/brands/', data);
        
        await toast.promise(promise, {
            loading: 'A guardar marca...',
            success: `Marca ${isEditing ? 'atualizada' : 'criada'}!`,
            error: (err) => err.response?.data?.detail || 'Ocorreu um erro.'
        });
        
        fetchMarcas();
        handleCloseFormModal();
    };

    const openConfirmationModal = (marca, isActivating) => {
        setMarcaToConfirm({ ...marca, isActivating });
        setIsConfirmModalOpen(true);
    };

    const handleConfirmStatusChange = async () => {
        if (!marcaToConfirm) return;
        const { id, isActivating } = marcaToConfirm;
        const endpoint = `/inventory/brands/${id}/${isActivating ? 'activate' : 'deactivate'}`;
        const promise = apiClient.put(endpoint);
        
        setIsConfirming(true);
        await toast.promise(promise, {
            loading: 'A alterar status...',
            success: 'Status da marca alterado!',
            error: 'Não foi possível alterar o status.'
        });
        
        fetchMarcas();
        setIsConfirming(false);
        setIsConfirmModalOpen(false);
        setMarcaToConfirm(null);
    };

    const handleSort = (key) => {
        setSortConfig(prev => ({ key, direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc' }));
    };

    if (isLoading && marcas.length === 0) {
        return <div className="flex justify-center items-center p-8"><Spinner /></div>;
    }

    if (error) {
        return <p className="text-center text-red-600 p-8">{error}</p>;
    }

    return (
        <div className="p-1 sm:p-4">
            <header className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Gerir Marcas</h2>
                <button 
                    className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700"
                    onClick={() => handleOpenFormModal()}
                >
                    <PlusIcon className="w-5 h-5 mr-2" />
                    Nova Marca
                </button>
            </header>

            <DataTable
                columns={columns}
                data={marcas}
                isLoading={isLoading}
                onEdit={handleOpenFormModal}
                onDeactivate={(item) => openConfirmationModal(item, false)}
                onActivate={(item) => openConfirmationModal(item, true)}
                sortConfig={sortConfig}
                onSort={handleSort}
            />

            <Modal isOpen={isFormModalOpen} onClose={handleCloseFormModal} title={editingMarca ? 'Editar Marca' : 'Nova Marca'}>
                <MarcaForm
                    marcaToEdit={editingMarca}
                    onSave={handleSaveMarca}
                    onCancel={handleCloseFormModal}
                />
            </Modal>

            {marcaToConfirm && (
                <ConfirmationModal
                    isOpen={isConfirmModalOpen}
                    onClose={() => setIsConfirmModalOpen(false)}
                    onConfirm={handleConfirmStatusChange}
                    isConfirming={isConfirming}
                    title={`${marcaToConfirm.isActivating ? 'Reativar' : 'Desativar'} Marca`}
                    message={`Tem a certeza de que deseja ${marcaToConfirm.isActivating ? 'reativar' : 'desativar'} a marca "${marcaToConfirm.nome}"?`}
                    confirmButtonText={marcaToConfirm.isActivating ? "Reativar" : "Desativar"}
                    confirmButtonVariant={marcaToConfirm.isActivating ? "primary" : "danger"}
                />
            )}
        </div>
    );
}
