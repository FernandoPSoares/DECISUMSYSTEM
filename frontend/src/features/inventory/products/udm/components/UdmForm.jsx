// frontend/src/features/inventory/products/udm/components/UdmForm.jsx

import React, { useState, useEffect } from 'react';
import Spinner from '../../../../../components/ui/Spinner';
import apiClient from '../../../../../api/apiClient';
import SearchableSelect from '../../../../../components/ui/SearchableSelect';

export default function UdmForm({ udmToEdit, onSave, onCancel }) {
    const [formData, setFormData] = useState({
        id: '',
        nome: '',
        proporcao_combinada: 1,
        categoria_udm_id: '',
    });
    const [selectedCategoriaOption, setSelectedCategoriaOption] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    // --- LÓGICA DE EDIÇÃO CORRIGIDA ---
    // Consideramos que estamos a editar apenas se o objeto já tiver um nome.
    // Se for uma criação contextual, 'udmToEdit' existe, mas 'udmToEdit.nome' não.
    const isEditing = !!udmToEdit?.nome;

    useEffect(() => {
        if (udmToEdit) {
            // Preenche todos os campos com os dados do item a ser editado ou com o contexto
            setFormData({
                id: udmToEdit.id || '',
                nome: udmToEdit.nome || '',
                proporcao_combinada: udmToEdit.proporcao_combinada || 1,
                // A categoria_udm_id agora é preenchida corretamente em ambos os cenários
                categoria_udm_id: udmToEdit.categoria_udm?.id || '',
            });

            // Prepara o objeto para o SearchableSelect, tanto para edição como para criação contextual
            if (udmToEdit.categoria_udm) {
                setSelectedCategoriaOption({
                    value: udmToEdit.categoria_udm.id,
                    label: udmToEdit.categoria_udm.nome,
                });
            } else {
                setSelectedCategoriaOption(null);
            }
        }
    }, [udmToEdit]);

    const handleChange = (e) => setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
    const handleCategoriaChange = (selectedOption) => {
        setSelectedCategoriaOption(selectedOption);
        setFormData(prev => ({ ...prev, categoria_udm_id: selectedOption ? selectedOption.value : '' }));
    };

    const loadCategoriaOptions = (inputValue, callback) => {
        apiClient.get(`/inventory/categorias-udm/?is_active=true&search=${inputValue}`)
            .then(response => {
                const options = response.data.map(cat => ({ value: cat.id, label: cat.nome }));
                callback(options);
            })
            .catch(err => {
                console.error("Falha ao carregar funções", err);
                callback([]);
            });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        try {
            await onSave(formData);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ocorreu um erro ao guardar a unidade.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col h-full bg-gray-50">
            <div className="flex-1 overflow-y-auto p-6">
                <div className="space-y-6 max-w-lg mx-auto">
                    <div>
                        <label htmlFor="id" className="block text-sm font-medium text-gray-700">ID da Unidade</label>
                        <input
                            type="text" name="id" id="id" value={formData.id} onChange={handleChange}
                            required
                            // O campo ID só é bloqueado no modo de edição real.
                            disabled={isEditing}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm disabled:bg-gray-100"
                            placeholder="Ex: KG, UN, L"
                        />
                    </div>
                    <div>
                        <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome da Unidade</label>
                        <input type="text" name="nome" id="nome" value={formData.nome} onChange={handleChange} required className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm" placeholder="Ex: Quilograma, Unidade, Litro" />
                    </div>
                    <div>
                        <label htmlFor="categoria_udm_id" className="block text-sm font-medium text-gray-700">Categoria</label>
                        <SearchableSelect
                            id="categoria_udm_id"
                            value={selectedCategoriaOption}
                            onChange={handleCategoriaChange}
                            loadOptions={loadCategoriaOptions}
                            placeholder="Pesquise por uma categoria..."
                            // O campo fica desativado tanto na edição como na criação contextual.
                            isDisabled={isEditing || !!udmToEdit?.categoria_udm}
                            required
                        />
                    </div>
                     <div>
                        <label htmlFor="proporcao_combinada" className="block text-sm font-medium text-gray-700">Proporção</label>
                        <input type="number" name="proporcao_combinada" id="proporcao_combinada" value={formData.proporcao_combinada} onChange={handleChange} required step="0.0001" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm" />
                        <p className="mt-1 text-xs text-gray-500">Proporção em relação à unidade de referência da categoria (ex: 1 para KG, 0.001 para G).</p>
                    </div>
                </div>
            </div>
            {error && <p className="mt-4 text-sm text-center text-red-600">{error}</p>}
            <div className="flex-shrink-0 border-t border-gray-200 px-6 py-4 flex justify-end space-x-3 bg-white">
                <button type="button" onClick={onCancel} className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50">Cancelar</button>
                <button type="submit" disabled={isLoading} className="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 border-transparent rounded-md shadow-sm hover:bg-indigo-700 disabled:bg-indigo-400">
                    {isLoading ? <Spinner size="h-5 w-5" /> : 'Guardar'}
                </button>
            </div>
        </form>
    );
}

