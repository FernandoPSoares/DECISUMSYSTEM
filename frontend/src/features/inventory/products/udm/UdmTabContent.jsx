// frontend/src/features/inventory/products/udm/components/UdmTabContent.jsx

import React, { useState, useEffect, useCallback } from 'react';
import apiClient from '../../../../../api/apiClient';
import DataTable from '../../../../../components/ui/table/DataTable';
import Modal from '../../../../../components/ui/Modal';
import ConfirmationModal from '../../../../../components/ui/ConfirmationModal';
import { PlusIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast';
import UdmForm from './UdmForm';

export default function UdmTabContent() {
    const [udms, setUdms] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [isFormModalOpen, setIsFormModalOpen] = useState(false);
    const [editingUdm, setEditingUdm] = useState(null);
    const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
    const [udmToConfirm, setUdmToConfirm] = useState(null);
    const [isConfirming, setIsConfirming] = useState(false);
    const [sortConfig, setSortConfig] = useState({ key: 'nome', direction: 'asc' });

    const fetchUdms = useCallback(async () => {
        setIsLoading(true);
        setError('');
        try {
            const params = new URLSearchParams({ sort_by: sortConfig.key, sort_order: sortConfig.direction });
            const response = await apiClient.get(`/inventory/udm/?${params.toString()}`);
            setUdms(response.data);
        } catch (err) {
            setError('Falha ao buscar as unidades de medida.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    }, [sortConfig]);

    useEffect(() => { fetchUdms(); }, [fetchUdms]);

    const columns = [
        { header: 'Nome da Unidade', accessor: 'nome', sortable: true },
        { header: 'Categoria', accessor: 'categoria_udm.nome', cell: row => row.categoria_udm.nome, sortable: true },
        { header: 'Proporção', accessor: 'proporcao_combinada', sortable: true },
        { header: 'Status', accessor: 'is_active', sortable: true, cell: (row) => (
            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${row.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {row.is_active ? 'Ativo' : 'Inativo'}
            </span>
        )},
    ];

    const handleOpenFormModal = (item = null) => { setEditingUdm(item); setIsFormModalOpen(true); };
    const handleCloseFormModal = () => { setEditingUdm(null); setIsFormModalOpen(false); };

    const handleSave = async (data) => {
        const isEditing = !!editingUdm;
        const promise = isEditing
            ? apiClient.put(`/inventory/udm/${editingUdm.id}`, data)
            : apiClient.post('/inventory/udm/', data);
        await toast.promise(promise, { loading: 'A guardar UDM...', success: `UDM ${isEditing ? 'atualizada' : 'criada'}!`, error: (err) => err.response?.data?.detail || 'Ocorreu um erro.' });
        fetchUdms();
        handleCloseFormModal();
    };
    
    const openConfirmationModal = (item, isActivating) => { setUdmToConfirm({ ...item, isActivating }); setIsConfirmModalOpen(true); };
    const closeConfirmationModal = () => setUdmToConfirm(null);

    const handleConfirmStatusChange = async () => {
        if (!udmToConfirm) return;
        const { id, isActivating } = udmToConfirm;
        const endpoint = `/inventory/udm/${id}/${isActivating ? 'activate' : 'deactivate'}`;
        const promise = apiClient.put(endpoint);
        setIsConfirming(true);
        await toast.promise(promise, { loading: 'A alterar status...', success: 'Status da UDM alterado!', error: 'Não foi possível alterar o status.' });
        fetchUdms();
        setIsConfirming(false);
        closeConfirmationModal();
    };
    
    const handleSort = (key) => setSortConfig(prev => ({ key, direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc' }));

    return (
        <div>
            <div className="flex justify-end mb-4">
                 <button onClick={() => handleOpenFormModal()} className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700">
                    <PlusIcon className="w-5 h-5 mr-2" />
                    Nova Unidade de Medida
                </button>
            </div>
            <DataTable columns={columns} data={udms} isLoading={isLoading} error={error} onEdit={handleOpenFormModal} onDeactivate={(item) => openConfirmationModal(item, false)} onActivate={(item) => openConfirmationModal(item, true)} sortConfig={sortConfig} onSort={handleSort} />
            <Modal isOpen={isFormModalOpen} onClose={handleCloseFormModal} title={editingUdm ? 'Editar Unidade de Medida' : 'Nova Unidade de Medida'}>
                <UdmForm udmToEdit={editingUdm} onSave={handleSave} onCancel={handleCloseFormModal} />
            </Modal>
            {udmToConfirm && <ConfirmationModal isOpen={!!udmToConfirm} onClose={closeConfirmationModal} onConfirm={handleConfirmStatusChange} isConfirming={isConfirming} title={udmToConfirm.isActivating ? "Reativar UDM" : "Desativar UDM"} message={`Tem a certeza de que deseja ${udmToConfirm.isActivating ? 'reativar' : 'desativar'} a unidade "${udmToConfirm.nome}"?`} confirmButtonText={udmToConfirm.isActivating ? "Reativar" : "Desativar"} confirmButtonVariant={udmToConfirm.isActivating ? "primary" : "danger"} />}
        </div>
    );
}
