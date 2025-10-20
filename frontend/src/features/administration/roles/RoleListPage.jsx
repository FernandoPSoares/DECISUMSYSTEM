// frontend/src/features/administration/roles/RoleListPage.jsx

import React, { useState, useEffect } from 'react';
import apiClient from '../../../api/apiClient';
import DataTable from '../../../components/ui/table/DataTable';
import Modal from '../../../components/ui/Modal';
import ConfirmationModal from '../../../components/ui/ConfirmationModal';
import RoleForm from './components/RoleForm';
import { PlusIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast';

export default function RoleListPage() {
    const [roles, setRoles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const [isFormModalOpen, setIsFormModalOpen] = useState(false);
    const [editingRole, setEditingRole] = useState(null);
    const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
    const [roleToConfirm, setRoleToConfirm] = useState(null);
    const [isConfirming, setIsConfirming] = useState(false);

    const [sortConfig, setSortConfig] = useState({ key: 'nome', direction: 'asc' });

    // --- 2. FUNÇÃO DE BUSCA DE DADOS ATUALIZADA ---
    const fetchRoles = async () => {
        setIsLoading(true);
        setError('');
        try {
            // A chamada à API agora inclui os parâmetros de ordenação.
            const params = new URLSearchParams({
                sort_by: sortConfig.key,
                sort_order: sortConfig.direction,
            });
            const response = await apiClient.get(`/roles/?${params.toString()}`);
            setRoles(response.data);
        } catch (err) {
            if (err.response && err.response.status === 403) {
                setError('Acesso negado. Verifique as suas permissões.');
            } else {
                setError('Falha ao buscar as funções.');
            }
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    // O useEffect agora re-busca os dados sempre que a ordenação muda.
    useEffect(() => {
        fetchRoles();
    }, [sortConfig]);

    // --- 1. DEFINIÇÃO DAS COLUNAS ATUALIZADA ---
    const columns = [
        {
            header: 'NOME DA FUNÇÃO',
            accessor: 'nome',
            sortable: true, // <-- Ativa a ordenação para esta coluna
            cell: (row) => (
                <div className="flex flex-col">
                    <span className="font-medium text-gray-900">{row.nome}</span>
                </div>
            )
        },
        {
            header: 'STATUS',
            accessor: 'is_active',
            sortable: true,
            cell: (row) => (
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    row.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                    {row.is_active ? 'Ativo' : 'Inativo'}
                </span>
            )
        },
    ];

    const handleOpenFormModal = (role = null) => {
        setEditingRole(role);
        setIsFormModalOpen(true);
    };

    const handleCloseFormModal = () => {
        setEditingRole(null);
        setIsFormModalOpen(false);
    };

    const handleSaveRole = async (roleData, permissionIds) => {
        const isEditing = editingRole && editingRole.nome;
        
        const savePromise = isEditing
            ? Promise.all([
                apiClient.put(`/roles/${editingRole.id}`, { nome: roleData.nome }),
                apiClient.put(`/roles/${editingRole.id}/permissions`, { permission_ids: permissionIds })
              ])
            : apiClient.post('/roles/', roleData).then(() => 
                apiClient.put(`/roles/${roleData.id}/permissions`, { permission_ids: permissionIds })
              );

        await toast.promise(
            savePromise,
            {
                loading: 'A guardar função...',
                success: `Função ${isEditing ? 'atualizada' : 'criada'} com sucesso!`,
                error: (err) => err.response?.data?.detail || 'Ocorreu um erro ao guardar.',
            }
        );

        fetchRoles();
        handleCloseFormModal();
    };
    
    const openConfirmationModal = (role, isActivating) => {
        setRoleToConfirm({ ...role, isActivating });
        setIsConfirmModalOpen(true);
    };

    const handleConfirmStatusChange = async () => {
        if (!roleToConfirm) return;
        
        const { id, isActivating } = roleToConfirm;
        const endpoint = isActivating ? 'activate' : 'deactivate';
        const statusPromise = apiClient.put(`/roles/${id}/${endpoint}`);

        setIsConfirming(true);
        await toast.promise(
            statusPromise,
            {
                loading: 'A alterar o status...',
                success: `Status da função alterado com sucesso!`,
                error: (err) => err.response?.data?.detail || 'Não foi possível alterar o status.',
            }
        );
        
        fetchRoles();
        setIsConfirming(false);
        setIsConfirmModalOpen(false);
        setRoleToConfirm(null);
    };

    const handleSort = (key) => {
        setSortConfig(prevConfig => ({
            key,
            direction: prevConfig.key === key && prevConfig.direction === 'asc' ? 'desc' : 'asc',
        }));
    };

    return (
        <div className="p-6 sm:p-8">
            <header className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Gestão de Funções</h1>
                    <p className="mt-1 text-sm text-gray-600">Crie, edite e defina as permissões para cada função do sistema.</p>
                </div>
                <button 
                    className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    onClick={() => handleOpenFormModal()}
                >
                    <PlusIcon className="w-5 h-5 mr-2" />
                    Nova Função
                </button>
            </header>

            <DataTable
                columns={columns}
                data={roles}
                isLoading={isLoading}
                error={error}
                onEdit={handleOpenFormModal}
                onDeactivate={(role) => openConfirmationModal(role, false)}
                onActivate={(role) => openConfirmationModal(role, true)}
                sortConfig={sortConfig}
                onSort={handleSort}
            />
            
            <Modal isOpen={isFormModalOpen} onClose={handleCloseFormModal} title={editingRole && editingRole.nome ? 'Editar Função' : 'Nova Função'}>
                <RoleForm 
                    roleToEdit={editingRole}
                    onSave={handleSaveRole}
                    onCancel={handleCloseFormModal}
                />
            </Modal>

            {roleToConfirm && (
                <ConfirmationModal
                    isOpen={isConfirmModalOpen}
                    onClose={() => setIsConfirmModalOpen(false)}
                    onConfirm={handleConfirmStatusChange}
                    isConfirming={isConfirming}
                    title={roleToConfirm.isActivating ? "Reativar Função" : "Desativar Função"}
                    message={`Tem a certeza de que deseja ${roleToConfirm.isActivating ? 'reativar' : 'desativar'} a função "${roleToConfirm.nome}"?`}
                    confirmButtonText={roleToConfirm.isActivating ? "Reativar" : "Desativar"}
                    confirmButtonVariant={roleToConfirm.isActivating ? "primary" : "danger"}
                />
            )}
        </div>
    );
}

