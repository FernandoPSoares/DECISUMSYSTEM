// frontend/src/features/administration/roles/components/RoleForm.jsx

import React, { useState, useEffect, useMemo } from 'react';
import Spinner from '../../../../components/ui/Spinner';
import apiClient from '../../../../api/apiClient';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function RoleForm({ roleToEdit, onSave, onCancel }) {
    const [formData, setFormData] = useState({ id: '', nome: '' });
    const [allPermissions, setAllPermissions] = useState([]);
    const [selectedPermissions, setSelectedPermissions] = useState(new Set());
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    
    const [activeGroup, setActiveGroup] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

    const isEditing = !!(roleToEdit && roleToEdit.nome);

    useEffect(() => {
        apiClient.get('/permissions/').then(response => {
            const permissionsData = response.data;
            setAllPermissions(permissionsData);
            if (permissionsData.length > 0) {
                const firstGroup = permissionsData[0].id.split(':')[0];
                setActiveGroup(firstGroup);
            }
        }).catch(err => {
            console.error("Falha ao carregar permissões", err);
            setError("Não foi possível carregar a lista de permissões.");
        });
    }, []);

    useEffect(() => {
        if (isEditing) {
            setFormData({ id: roleToEdit.id, nome: roleToEdit.nome });
            setSelectedPermissions(new Set(roleToEdit.permissions.map(p => p.id)));
        } else if (roleToEdit) {
            setFormData({ id: roleToEdit.id, nome: '' });
            setSelectedPermissions(new Set());
        }
    }, [roleToEdit, isEditing]);

    const handlePermissionChange = (permissionId) => {
        setSelectedPermissions(prev => {
            const newSet = new Set(prev);
            newSet.has(permissionId) ? newSet.delete(permissionId) : newSet.add(permissionId);
            return newSet;
        });
    };

    const groupedPermissions = useMemo(() => {
        return allPermissions.reduce((acc, permission) => {
            const group = permission.id.split(':')[0];
            if (!acc[group]) {
                acc[group] = [];
            }
            acc[group].push(permission);
            return acc;
        }, {});
    }, [allPermissions]);

    const filteredPermissions = useMemo(() => {
        if (!activeGroup) return [];
        const groupPerms = groupedPermissions[activeGroup] || [];
        if (!searchTerm) return groupPerms;
        return groupPerms.filter(p => 
            p.id.toLowerCase().includes(searchTerm.toLowerCase()) || 
            p.descricao.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }, [activeGroup, searchTerm, groupedPermissions]);

    const handleSelectAllPermissions = () => {
        const allIds = allPermissions.map(p => p.id);
        setSelectedPermissions(new Set(allIds));
    };

    const handleDeselectAllPermissions = () => {
        setSelectedPermissions(new Set());
    };

    // --- NOVA FUNÇÃO PARA SELEÇÃO EM GRUPO ---
    const handleGroupToggle = (groupName, shouldSelect) => {
        const groupPermissionIds = (groupedPermissions[groupName] || []).map(p => p.id);
        setSelectedPermissions(prev => {
            const newSet = new Set(prev);
            if (shouldSelect) {
                groupPermissionIds.forEach(id => newSet.add(id));
            } else {
                groupPermissionIds.forEach(id => newSet.delete(id));
            }
            return newSet;
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        try {
            await onSave(formData, Array.from(selectedPermissions));
        } catch (err) {
            setError(err.response?.data?.detail || 'Ocorreu um erro ao guardar a função.');
        } finally {
            setIsLoading(false);
        }
    };

    // --- NOVA VARIÁVEL PARA CONTROLAR O ESTADO DA CHECKBOX DE GRUPO ---
    const isGroupSelected = useMemo(() => {
        const groupPerms = groupedPermissions[activeGroup] || [];
        if (groupPerms.length === 0) return false;
        return groupPerms.every(p => selectedPermissions.has(p.id));
    }, [activeGroup, selectedPermissions, groupedPermissions]);

    return (
        <form onSubmit={handleSubmit} className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto p-6">
                <div className="space-y-6">
                    <div>
                        <label htmlFor="id" className="block text-sm font-medium text-gray-700">ID da Função</label>
                        <input type="text" name="id" id="id" value={formData.id} onChange={(e) => setFormData(p => ({...p, id: e.target.value}))} required disabled={isEditing} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm disabled:bg-gray-100" />
                    </div>
                    <div>
                        <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome da Função</label>
                        <input type="text" name="nome" id="nome" value={formData.nome} onChange={(e) => setFormData(p => ({...p, nome: e.target.value}))} required className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm" />
                    </div>
                </div>

                <div className="mt-8">
                    <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Permissões</h3>
                        <div className="flex space-x-2">
                            <button type="button" onClick={handleSelectAllPermissions} className="text-xs font-semibold text-indigo-600 hover:text-indigo-800">Marcar Todas</button>
                            <button type="button" onClick={handleDeselectAllPermissions} className="text-xs font-semibold text-gray-500 hover:text-gray-700">Desmarcar Todas</button>
                        </div>
                    </div>
                    <div className="mt-4 h-[400px] flex rounded-lg border border-gray-300 bg-white">
                        <nav className="w-1/3 border-r border-gray-200 bg-gray-50/50 overflow-y-auto">
                            <ul className="p-2 space-y-1">
                                {Object.keys(groupedPermissions).map(groupName => (
                                    <li key={groupName}>
                                        <button
                                            type="button"
                                            onClick={() => setActiveGroup(groupName)}
                                            className={`w-full text-left px-3 py-2 text-sm rounded-md transition-colors ${activeGroup === groupName ? 'bg-indigo-100 text-indigo-700 font-semibold' : 'text-gray-600 hover:bg-gray-100'}`}
                                        >
                                            <span className="capitalize">{groupName}</span>
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </nav>
                        
                        <div className="w-2/3 flex flex-col">
                            <div className="p-4 border-b border-gray-200">
                                <div className="relative">
                                    <MagnifyingGlassIcon className="pointer-events-none absolute top-1/2 left-3 h-5 w-5 -translate-y-1/2 text-gray-400" />
                                    <input type="search" placeholder="Filtrar permissões..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="w-full rounded-md border-gray-300 pl-10 sm:text-sm" />
                                </div>
                            </div>
                            <div className="flex-1 p-4 overflow-y-auto">
                                {/* --- NOVA CHECKBOX PARA SELEÇÃO EM GRUPO --- */}
                                <div className="flex items-center justify-end mb-4">
                                    <input 
                                        id="select-all-group" 
                                        type="checkbox" 
                                        className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                                        checked={isGroupSelected} 
                                        onChange={(e) => handleGroupToggle(activeGroup, e.target.checked)} 
                                    />
                                    <label htmlFor="select-all-group" className="ml-2 text-sm font-medium text-gray-700">Selecionar Todos no Grupo</label>
                                </div>
                                <div className="space-y-4">
                                    {filteredPermissions.map(permission => (
                                        <div key={permission.id} className="relative flex items-start">
                                            <div className="flex h-5 items-center">
                                                <input id={permission.id} type="checkbox" className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" checked={selectedPermissions.has(permission.id)} onChange={() => handlePermissionChange(permission.id)} />
                                            </div>
                                            <div className="ml-3 text-sm">
                                                <label htmlFor={permission.id} className="font-medium text-gray-700">{permission.id.split(':')[1]}</label>
                                                <p className="text-xs text-gray-500">{permission.descricao}</p>
                                            </div>
                                        </div>
                                    ))}
                                    {filteredPermissions.length === 0 && (
                                        <p className="text-sm text-gray-500 text-center py-4">Nenhuma permissão encontrada para este grupo ou filtro.</p>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {error && <p className="mt-4 text-sm text-center text-red-600">{error}</p>}

            <div className="flex-shrink-0 border-t border-gray-200 px-6 py-4 flex justify-end space-x-3 bg-gray-50">
                <button type="button" onClick={onCancel} className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    Cancelar
                </button>
                <button type="submit" disabled={isLoading} className="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400">
                    {isLoading ? <Spinner size="h-5 w-5" /> : 'Guardar'}
                </button>
            </div>
        </form>
    );
}

