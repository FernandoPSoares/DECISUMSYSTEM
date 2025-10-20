// frontend/src/features/inventory/products/components/UdmManager.jsx

import React, { useState, useEffect, useCallback } from 'react';
import apiClient from '../../../../api/apiClient';
import { PlusIcon, ArchiveBoxIcon, ArrowUturnLeftIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast';
import Spinner from '../../../../components/ui/Spinner';
import Modal from '../../../../components/ui/Modal';
import ConfirmationModal from '../../../../components/ui/ConfirmationModal';
import UdmCategoryRow from './UdmCategoryRow';
import CategoriaUdmForm from '../udm/components/CategoriaUdmForm';
import UdmForm from '../udm/components/UdmForm';
import SearchableSelect from '../../../../components/ui/SearchableSelect';

export default function UdmManager() {
    const [categories, setCategories] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    
    const [isCategoriaModalOpen, setIsCategoriaModalOpen] = useState(false);
    const [isUdmModalOpen, setIsUdmModalOpen] = useState(false);
    const [editingItem, setEditingItem] = useState(null);

    const [showArchived, setShowArchived] = useState(false);
    
    const [itemToConfirm, setItemToConfirm] = useState(null);
    const [isConfirming, setIsConfirming] = useState(false);

    const [isChangeRefModalOpen, setIsChangeRefModalOpen] = useState(false);
    const [categoryToChangeRef, setCategoryToChangeRef] = useState(null);
    const [newReferenceUdmId, setNewReferenceUdmId] = useState(null);


    const fetchData = useCallback(async () => {
        setIsLoading(true);
        setError('');
        try {
            const params = new URLSearchParams({ is_active: !showArchived });
            const response = await apiClient.get(`/inventory/categorias-udm/?${params.toString()}`);
            setCategories(response.data);
        } catch (err) {
            setError(`Falha ao buscar os dados de Unidades de Medida ${showArchived ? 'arquivadas' : 'ativas'}.`);
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    }, [showArchived]);

    useEffect(() => { fetchData(); }, [fetchData]);

    const handleOpenCategoriaModal = (categoria = null) => {
        setEditingItem(categoria);
        setIsCategoriaModalOpen(true);
    };

    const handleOpenUdmModal = (udm = null, category = null) => {
        let itemToEdit = udm ? { ...udm } : { categoria_udm: category };
        if (udm) {
            const parentCategory = categories.find(cat => cat.udms.some(u => u.id === udm.id));
            if (parentCategory && parentCategory.unidade_referencia_id === udm.id) {
                itemToEdit.isReference = true;
            }
        }
        setEditingItem(itemToEdit);
        setIsUdmModalOpen(true);
    };


    const handleCloseModals = () => {
        setIsCategoriaModalOpen(false);
        setIsUdmModalOpen(false);
        setIsChangeRefModalOpen(false);
        setEditingItem(null);
        setItemToConfirm(null);
        setCategoryToChangeRef(null);
        setNewReferenceUdmId(null);
    };

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
        const promise = data.id
            ? apiClient.put(`/inventory/udm/${data.id}`, data)
            : apiClient.post('/inventory/udm/', data);
        
        await toast.promise(promise, { 
            loading: 'A guardar...', 
            success: `Unidade de Medida ${data.id ? 'atualizada' : 'criada'}!`, 
            error: (err) => err.response?.data?.detail || 'Ocorreu um erro.' 
        });
        
        fetchData();
        handleCloseModals();
    };

    const openConfirmationModal = (item, type, action) => {
        setItemToConfirm({ ...item, type, action });
    };

    const handleConfirmAction = async () => {
        if (!itemToConfirm) return;
        const { id, type, nome, action } = itemToConfirm;
        const endpoint = type === 'categoria' ? `/inventory/categorias-udm/${id}/${action}` : `/inventory/udm/${id}/${action}`;
        const actionVerb = action === 'deactivate' ? 'Desativar' : 'Reativar';
        const promise = apiClient.put(endpoint);
        setIsConfirming(true);
        await toast.promise(promise, { loading: `${actionVerb.slice(0,-1)}ando ${nome}...`, success: `${type === 'categoria' ? 'Categoria' : 'Unidade'} "${nome}" ${action === 'deactivate' ? 'desativada' : 'reativada'}!`, error: (err) => err.response?.data?.detail || `Não foi possível ${actionVerb.toLowerCase()} o item.` });
        fetchData();
        handleCloseModals();
        setIsConfirming(false);
    };

    const handleOpenChangeRefModal = () => {
        const fullCategory = categories.find(cat => cat.id === editingItem.id);
        if (fullCategory) {
            setCategoryToChangeRef(fullCategory);
            setIsCategoriaModalOpen(false);
            setIsChangeRefModalOpen(true);
        } else {
            toast.error("Não foi possível encontrar os dados da categoria. Tente novamente.");
        }
    };

    const handleConfirmChangeReference = async () => {
        if (!categoryToChangeRef || !newReferenceUdmId) {
            toast.error('Selecione uma nova unidade de referência.');
            return;
        }
        const promise = apiClient.put(`/inventory/categorias-udm/${categoryToChangeRef.id}/change-reference`, {
            new_reference_udm_id: newReferenceUdmId.value
        });
        setIsConfirming(true);
        await toast.promise(promise, {
            loading: 'A alterar a referência e a recalcular proporções...',
            success: 'Unidade de referência alterada com sucesso!',
            error: (err) => err.response?.data?.detail || 'Ocorreu um erro ao alterar a referência.'
        });
        fetchData();
        handleCloseModals();
        setIsConfirming(false);
    };
    
    // --- CORREÇÃO DEFINITIVA: A função agora é async e retorna uma Promise ---
    const loadReferenceOptions = async (inputValue) => {
        if (!categoryToChangeRef) {
            return [];
        }
        // Filtra a lista de UDMs localmente
        const filteredOptions = categoryToChangeRef.udms
            ?.filter(udm => 
                udm.is_active && 
                udm.id !== categoryToChangeRef.unidade_referencia_id &&
                udm.nome.toLowerCase().includes(inputValue.toLowerCase())
            )
            .map(udm => ({ label: `${udm.nome} (${udm.id})`, value: udm.id })) || [];
        
        // Retorna a lista, que será implicitamente envolvida numa Promise
        return filteredOptions;
    };


    return (
        <div className="p-1 sm:p-4">
            <header className="flex items-start justify-between mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">{showArchived ? 'Arquivo de Unidades de Medida' : 'Gerir Unidades de Medida'}</h2>
                    <p className="mt-1 text-sm text-gray-600">{showArchived ? 'Consulte as categorias e unidades inativas.' : 'Gira as categorias e as unidades de medida (UDM) ativas.'}</p>
                </div>
                <div className="flex-shrink-0 flex items-center gap-x-2">
                    {!showArchived && (<button className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700" onClick={() => handleOpenCategoriaModal()}><PlusIcon className="w-5 h-5 mr-2" />Nova Categoria</button>)}
                    <button className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50" onClick={() => setShowArchived(!showArchived)}>
                        {showArchived ? (<ArrowUturnLeftIcon className="w-5 h-5 mr-2" />) : (<ArchiveBoxIcon className="w-5 h-5 mr-2" />)}
                        {showArchived ? 'Ver Ativos' : 'Ver Arquivados'}
                    </button>
                </div>
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
                        <UdmCategoryRow key={category.id} category={category} onEditCategory={handleOpenCategoriaModal} onEditUdm={(udm) => handleOpenUdmModal(udm)} onAddUdm={(cat) => handleOpenUdmModal(null, cat)} isArchivedView={showArchived} onReactivateCategory={(cat) => openConfirmationModal(cat, 'categoria', 'activate')} onReactivateUdm={(udm) => openConfirmationModal(udm, 'udm', 'activate')} onDeactivateCategory={(cat) => openConfirmationModal(cat, 'categoria', 'deactivate')} onDeactivateUdm={(udm) => openConfirmationModal(udm, 'udm', 'deactivate')} />
                    ))}
                     {categories.length === 0 && (<p className="text-center text-gray-500 py-8">{showArchived ? 'Nenhum item arquivado encontrado.' : 'Nenhuma categoria encontrada.'}</p>)}
                </div>
            )}
            
            <Modal isOpen={isCategoriaModalOpen} onClose={handleCloseModals} title={editingItem ? 'Editar Categoria' : 'Nova Categoria'}>
                <CategoriaUdmForm categoriaToEdit={editingItem} onSave={handleSaveCategoria} onCancel={handleCloseModals} onChangeReference={handleOpenChangeRefModal} />
            </Modal>
            
            <Modal isOpen={isUdmModalOpen} onClose={handleCloseModals} title={editingItem?.nome ? 'Editar UDM' : 'Nova UDM'}>
                <UdmForm udmToEdit={editingItem} onSave={handleSaveUdm} onCancel={handleCloseModals} />
            </Modal>

            <Modal isOpen={isChangeRefModalOpen} onClose={handleCloseModals} title={`Alterar UDM de Referência para "${categoryToChangeRef?.nome}"`}>
                <div className="space-y-4 p-2">
                    <p className="text-sm text-gray-600">Selecione a nova unidade de medida que servirá como base para esta categoria. Todas as outras unidades terão as suas proporções recalculadas automaticamente.</p>
                    <div>
                        <label htmlFor="new_ref_udm" className="block text-sm font-medium text-gray-700">Nova Unidade de Referência</label>
                        <SearchableSelect
                            id="new_ref_udm"
                            value={newReferenceUdmId}
                            onChange={setNewReferenceUdmId}
                            loadOptions={loadReferenceOptions}
                            placeholder="Selecione uma UDM..."
                            key={categoryToChangeRef?.id}
                        />
                    </div>
                     <div className="flex justify-end space-x-2 pt-4">
                        <button type="button" onClick={handleCloseModals} className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50">Cancelar</button>
                        <button type="button" onClick={handleConfirmChangeReference} disabled={!newReferenceUdmId || isConfirming} className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 disabled:bg-indigo-300">
                            {isConfirming ? <Spinner size="sm" /> : 'Confirmar Alteração'}
                        </button>
                    </div>
                </div>
            </Modal>

            {itemToConfirm && (<ConfirmationModal isOpen={!!itemToConfirm} onClose={handleCloseModals} onConfirm={handleConfirmAction} isConfirming={isConfirming} title={`${itemToConfirm.action === 'deactivate' ? 'Desativar' : 'Reativar'} ${itemToConfirm.type === 'categoria' ? 'Categoria' : 'Unidade'}`} message={`Tem a certeza de que deseja ${itemToConfirm.action === 'deactivate' ? 'desativar' : 'reativar'} "${itemToConfirm.nome}"?`} confirmButtonText={itemToConfirm.action === 'deactivate' ? 'Desativar' : 'Reativar'} confirmButtonVariant={itemToConfirm.action === 'deactivate' ? 'danger' : 'primary'}/>)}
        </div>
    );
}

