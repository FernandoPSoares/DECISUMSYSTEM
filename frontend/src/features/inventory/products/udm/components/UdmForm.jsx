// frontend/src/features/inventory/products/udm/components/UdmForm.jsx

import React, { useState, useEffect } from 'react';
import Spinner from '../../../../../components/ui/Spinner';
import apiClient from '../../../../../api/apiClient';
import SearchableSelect from '../../../../../components/ui/SearchableSelect';
import { toast } from 'react-hot-toast';

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

    const isEditing = !!udmToEdit?.nome;

    useEffect(() => {
        if (udmToEdit) {
            setFormData({
                id: udmToEdit.id || '',
                nome: udmToEdit.nome || '',
                proporcao_combinada: udmToEdit.proporcao_combinada || 1,
                categoria_udm_id: udmToEdit.categoria_udm?.id || '',
            });

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
        setFormData(prev => ({ ...prev, categoria_udm_id: selectedOption ? selectedOption.value : null }));
    };

    // --- CORREÇÃO: A função agora é async e retorna uma Promise com as opções ---
    const loadCategoriaOptions = async (inputValue) => {
        try {
            const params = new URLSearchParams({ q: inputValue, is_active: true });
            const response = await apiClient.get(`/inventory/categorias-udm/?${params.toString()}`);
            return response.data.map(cat => ({ 
                value: cat.id, 
                label: `${cat.nome} (${cat.id})` 
            }));
        } catch (err) {
            toast.error("Falha ao carregar categorias.");
            return []; // Retorna um array vazio em caso de erro
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (parseFloat(formData.proporcao_combinada) <= 0) {
            toast.error('A proporção deve ser um número positivo maior que zero.');
            return;
        }
        
        onSave(formData);
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
                            required
                        />
                    </div>
                     <div>
                        <label htmlFor="proporcao_combinada" className="block text-sm font-medium text-gray-700">Proporção</label>
                        <input
                            type="number"
                            name="proporcao_combinada"
                            id="proporcao_combinada"
                            value={formData.proporcao_combinada}
                            onChange={handleChange}
                            required
                            min="0.0001"
                            step="any"
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm"
                        />
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
