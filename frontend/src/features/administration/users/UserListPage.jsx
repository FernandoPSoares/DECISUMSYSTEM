// frontend/src/features/users/UserListPage.jsx

import React, { useState, useEffect } from 'react';
import apiClient from '../../../api/apiClient';
import DataTable from '../../../components/ui/table/DataTable';
import Modal from '../../../components/ui/Modal';
import ConfirmationModal from '../../../components/ui/ConfirmationModal';
import UserForm from './components/UserForm';
import { PlusIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast'; 

export default function UserListPage() {
    const [users, setUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const [isFormModalOpen, setIsFormModalOpen] = useState(false);
    const [editingUser, setEditingUser] = useState(null);

    // --- ESTADO PARA CONTROLAR O MODAL DE CONFIRMAÇÃO ---
    const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
    const [userToConfirm, setUserToConfirm] = useState(null);
    const [isConfirming, setIsConfirming] = useState(false);

    const [sortConfig, setSortConfig] = useState({ key: 'usuario', direction: 'asc' });

    const fetchUsers = async () => {
        setIsLoading(true);
        setError(''); 
        try {
            // --- 4. ATUALIZAR A BUSCA DE DADOS ---
            // A chamada à API agora inclui os parâmetros de ordenação.
            const params = new URLSearchParams({
                sort_by: sortConfig.key,
                sort_order: sortConfig.direction,
            });
            const response = await apiClient.get(`/usuarios/?${params.toString()}`);
            setUsers(response.data);
        } catch (err) {
            if (err.response && err.response.status === 403) {
                setError('Acesso negado. Verifique as suas permissões.');
            } else {
                setError('Falha ao buscar utilizadores.');
            }
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, [sortConfig]);

    const columns = [
        {
            header: 'UTILIZADOR',
            accessor: 'usuario',
            sortable: true, // <-- Ativa a ordenação para esta coluna
            cell: (row) => <div className="font-medium text-gray-900">{row.usuario}</div>
        },
        {
            header: 'EMAIL',
            accessor: 'email',
            sortable: true, // <-- Ativa a ordenação para esta coluna
        },
        {
            header: 'FUNÇÃO',
            accessor: 'role.nome',
            sortable: true,        // Ativamos a ordenação para esta coluna
            cell: (row) => row.role.nome
        },
        {
            header: 'STATUS',
            accessor: 'is_active',
            sortable: true,
            cell: (row) => (
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    row.is_active 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                    {row.is_active ? 'Ativo' : 'Inativo'}
                </span>
            )
        },
    ];

    // --- LÓGICA DO FORMULÁRIO MODAL ---
    const handleOpenFormModal = (user = null) => {
        if (user) {
            setEditingUser(user);
        } else {
            const newUserId = crypto.randomUUID();
            setEditingUser({ id: newUserId });
        }
        setIsFormModalOpen(true);
    };

    const handleCloseFormModal = () => {
        setEditingUser(null);
        setIsFormModalOpen(false);
    };

    const handleSaveUser = async (userData) => {
        const isActuallyEditing = editingUser && Object.keys(editingUser).length > 1;
        
        const savePromise = isActuallyEditing
            ? apiClient.put(`/usuarios/${editingUser.id}`, userData)
            : apiClient.post('/usuarios/', userData);

        await toast.promise(
            savePromise,
            {
                loading: 'A guardar utilizador...',
                success: `Utilizador ${isActuallyEditing ? 'atualizado' : 'criado'} com sucesso!`,
                error: (err) => err.response?.data?.detail || 'Ocorreu um erro ao guardar.',
            }
        );

        fetchUsers();
        handleCloseFormModal();
    };
    
    // --- LÓGICA DO MODAL DE CONFIRMAÇÃO ---
    const openConfirmationModal = (user, isActivating) => {
        setUserToConfirm({ ...user, isActivating });
        setIsConfirmModalOpen(true);
    };

    const handleConfirmStatusChange = async () => {
        if (!userToConfirm) return;
        
        const { id, isActivating } = userToConfirm;
        const endpoint = isActivating ? 'activate' : 'deactivate';
        
        const statusPromise = apiClient.put(`/usuarios/${id}/${endpoint}`);

        setIsConfirming(true);
        await toast.promise(
            statusPromise,
            {
                loading: 'A alterar o status...',
                success: `Status do utilizador alterado com sucesso!`,
                error: (err) => err.response?.data?.detail || 'Não foi possível alterar o status.',
            }
        );
        
        fetchUsers();
        setIsConfirming(false);
        setIsConfirmModalOpen(false);
        setUserToConfirm(null);
    };


    const handleSort = (key) => {
        setSortConfig(prevConfig => {
            // Se já estiver a ordenar por esta coluna, inverte a direção
            if (prevConfig.key === key && prevConfig.direction === 'asc') {
                return { key, direction: 'desc' };
            }
            // Senão, ordena por esta coluna em ordem ascendente
            return { key, direction: 'asc' };
        });
    };

    return (
        <div className="p-6 sm:p-8">
            <header className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Gestão de Utilizadores</h1>
                </div>
                <button 
                    className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    onClick={() => handleOpenFormModal()}
                >
                    <PlusIcon className="w-5 h-5 mr-2" />
                    Novo Utilizador
                </button>
            </header>

            <DataTable
                columns={columns}
                data={users}
                isLoading={isLoading}
                error={error}
                onEdit={handleOpenFormModal}
                onDeactivate={(user) => openConfirmationModal(user, false)}
                onActivate={(user) => openConfirmationModal(user, true)}
                sortConfig={sortConfig}
                onSort={handleSort}
            />
            
            <Modal 
                isOpen={isFormModalOpen} 
                onClose={handleCloseFormModal} 
                title={editingUser && Object.keys(editingUser).length > 1 ? 'Editar Utilizador' : 'Novo Utilizador'}
            >
                <UserForm 
                    userToEdit={editingUser}
                    onSave={handleSaveUser}
                    onCancel={handleCloseFormModal}
                />
            </Modal>

            {userToConfirm && (
                <ConfirmationModal
                    isOpen={isConfirmModalOpen}
                    onClose={() => setIsConfirmModalOpen(false)}
                    onConfirm={handleConfirmStatusChange}
                    isConfirming={isConfirming}
                    title={userToConfirm.isActivating ? "Reativar Utilizador" : "Desativar Utilizador"}
                    message={`Tem a certeza de que deseja ${userToConfirm.isActivating ? 'reativar' : 'desativar'} o utilizador "${userToConfirm.usuario}"?`}
                    confirmButtonText={userToConfirm.isActivating ? "Reativar" : "Desativar"}
                    confirmButtonVariant={userToConfirm.isActivating ? "primary" : "danger"}
                />
            )}
        </div>
    );
}

