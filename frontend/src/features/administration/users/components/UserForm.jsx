// frontend/src/features/users/components/UserForm.jsx

import React, { useState, useEffect } from 'react';
import Spinner from '../../../../components/ui/Spinner';
import apiClient from '../../../../api/apiClient';
import SearchableSelect from '../../../../components/ui/SearchableSelect';
import SearchModal from '../../../../components/ui/SearchModal';

export default function UserForm({ userToEdit, onSave, onCancel }) {
    const [formData, setFormData] = useState({
        id: '',
        usuario: '',
        email: '',
        senha: '',
        role_id: '',
    });
    
    // Estado para gerir o valor do react-select, que usa o formato { value, label }
    const [selectedRoleOption, setSelectedRoleOption] = useState(null);
    
    // Estado para controlar a visibilidade do modal de pesquisa avançada
    const [isSearchModalOpen, setIsSearchModalOpen] = useState(false);

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const isEditing = userToEdit && Object.keys(userToEdit).length > 1;

    // Preenche o formulário com os dados iniciais para um novo utilizador ou para edição
    useEffect(() => {
        if (userToEdit) {
            setFormData({
                id: userToEdit.id || '',
                usuario: userToEdit.usuario || '',
                email: userToEdit.email || '',
                senha: '', // Senha nunca é pré-preenchida por segurança
                role_id: userToEdit.role?.id || '',
            });

            // Se estiver a editar um utilizador que já tem uma função, pré-seleciona-a
            if (isEditing && userToEdit.role) {
                setSelectedRoleOption({
                    value: userToEdit.role.id,
                    label: userToEdit.role.nome,
                });
            } else {
                setSelectedRoleOption(null); // Garante que o campo está limpo para um novo utilizador
            }
        }
    }, [userToEdit, isEditing]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    // --- LÓGICA OTIMIZADA PARA O SEARCHABLE SELECT ---

    // Função que o SearchableSelect irá chamar para buscar opções na API
    const loadRoleOptions = (inputValue, callback) => {
        const params = new URLSearchParams({
            is_active: 'true',
            limit: '7' // Mostra um número limitado de opções
        });
        if (inputValue) {
            // Pede ao backend para filtrar os resultados
            params.append('search', inputValue);
        }

        apiClient.get(`/roles/?${params.toString()}`)
            .then(response => {
                const options = response.data.map(role => ({
                    value: role.id,
                    label: role.nome,
                }));
                callback(options);
            })
            .catch(err => {
                console.error("Falha ao carregar funções", err);
                callback([]); // Devolve um array vazio em caso de erro
            });
    };

    // Função chamada quando uma opção é selecionada no dropdown
    const handleRoleChange = (selectedOption) => {
        setSelectedRoleOption(selectedOption);
        setFormData(prev => ({ ...prev, role_id: selectedOption ? selectedOption.value : '' }));
    };

    // --- LÓGICA PARA O MODAL DE PESQUISA AVANÇADA ---
    
    const handleOpenSearchModal = () => setIsSearchModalOpen(true);

    const handleSelectFromModal = (selectedRole) => {
        const newOption = { value: selectedRole.id, label: selectedRole.nome };
        handleRoleChange(newOption);
        setIsSearchModalOpen(false);
    };
    
    const roleSearchColumns = [
        { header: 'Nome da Função', accessor: 'nome', sortable: true, cell: (row) => <div className="font-medium text-gray-900">{row.nome}</div> },
        { header: 'ID', accessor: 'id', sortable: true, cell: (row) => <code className="text-xs">{row.id}</code> },
    ];

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        try {
            const dataToSend = { ...formData };
            if (isEditing && !dataToSend.senha) {
                delete dataToSend.senha;
            }
            await onSave(dataToSend);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ocorreu um erro ao guardar o utilizador.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit} className="flex flex-col h-full bg-gray-50">
                <div className="flex-1 overflow-y-auto p-6">
                    <div className="space-y-6 max-w-lg mx-auto">
                        <div>
                            <label htmlFor="id" className="block text-sm font-medium text-gray-700">ID do Utilizador</label>
                            <input
                                type="text" name="id" id="id" value={formData.id}
                                readOnly
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm bg-gray-100 text-gray-500 sm:text-sm"
                            />
                        </div>
                        <div>
                            <label htmlFor="usuario" className="block text-sm font-medium text-gray-700">Nome de Utilizador</label>
                            <input
                                type="text" name="usuario" id="usuario" value={formData.usuario} onChange={handleChange}
                                required
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                            />
                        </div>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                            <input
                                type="email" name="email" id="email" value={formData.email} onChange={handleChange}
                                required
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                            />
                        </div>
                        <div>
                            <label htmlFor="senha" className="block text-sm font-medium text-gray-700">Senha</label>
                            <input
                                type="password" name="senha" id="senha" value={formData.senha} onChange={handleChange}
                                required={!isEditing}
                                placeholder={isEditing ? 'Deixar em branco para não alterar' : ''}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                            />
                        </div>
                        
                        <div>
                            <label htmlFor="role_id" className="block text-sm font-medium text-gray-700">Função</label>
                            <div className="mt-1">
                                <SearchableSelect
                                    id="role_id"
                                    value={selectedRoleOption}
                                    onChange={handleRoleChange}
                                    loadOptions={loadRoleOptions}
                                    placeholder="Pesquise por uma função..."
                                    onAdvancedSearchClick={handleOpenSearchModal}
                                    required
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {error && <p className="mt-4 text-sm text-center text-red-600">{error}</p>}

                <div className="flex-shrink-0 border-t border-gray-200 px-6 py-4 flex justify-end space-x-3 bg-white">
                    <button 
                        type="button" 
                        onClick={onCancel}
                        className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        Cancelar
                    </button>
                    <button 
                        type="submit" 
                        disabled={isLoading}
                        className="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400"
                    >
                        {isLoading ? <Spinner size="h-5 w-5" /> : 'Guardar'}
                    </button>
                </div>
            </form>

            <SearchModal
                isOpen={isSearchModalOpen}
                onClose={() => setIsSearchModalOpen(false)}
                onSelect={handleSelectFromModal}
                title="Pesquisa Avançada de Funções"
                apiEndpoint="/roles/?is_active=true" // O modal adicionará os outros parâmetros
                columns={roleSearchColumns}
            />
        </>
    );
}

