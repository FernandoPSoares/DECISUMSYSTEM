// frontend/src/features/inventory/catalog/components/CategoriaProdutoForm.jsx

import React, { useState, useEffect } from 'react';
import Spinner from '../../../../components/ui/Spinner';
import apiClient from '../../../../api/apiClient';
import SearchableSelect from '../../../../components/ui/SearchableSelect';

export default function CategoriaProdutoForm({ categoriaToEdit, onSave, onCancel }) {
    const [formData, setFormData] = useState({
        id: '',
        nome: '',
        metodo_custeio: 'FIFO', // Valor padrão
        categoria_pai_id: null,
    });
    const [selectedParentOption, setSelectedParentOption] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const isEditing = !!categoriaToEdit;

    useEffect(() => {
        if (categoriaToEdit) {
            setFormData({
                id: categoriaToEdit.id || '',
                nome: categoriaToEdit.nome || '',
                metodo_custeio: categoriaToEdit.metodo_custeio || 'FIFO',
                categoria_pai_id: categoriaToEdit.categoria_pai?.id || null,
            });
            if (categoriaToEdit.categoria_pai) {
                setSelectedParentOption({
                    value: categoriaToEdit.categoria_pai.id,
                    label: categoriaToEdit.categoria_pai.nome,
                });
            } else {
                setSelectedParentOption(null);
            }
        }
    }, [categoriaToEdit]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleParentChange = (selectedOption) => {
        setSelectedParentOption(selectedOption);
        setFormData(prev => ({ ...prev, categoria_pai_id: selectedOption ? selectedOption.value : null }));
    };

    const loadParentOptions = (inputValue, callback) => {
        const params = new URLSearchParams({ is_active: 'true' });
        if (inputValue) params.append('search', inputValue);
        // Exclui a própria categoria da lista de pais para evitar loops de referência
        if (isEditing) params.append('exclude_id', categoriaToEdit.id);

        apiClient.get(`/inventory/categorias-produto/?${params.toString()}`)
            .then(response => {
                const options = response.data.map(cat => ({
                    value: cat.id,
                    label: cat.nome,
                }));
                callback(options);
            });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        try {
            // Garante que o categoria_pai_id é enviado como null se não for selecionado
            const dataToSend = {
                ...formData,
                categoria_pai_id: formData.categoria_pai_id || null,
            };
            await onSave(dataToSend);
        } catch (err) {
            const formattedError = (err.response?.status === 422 && err.response?.data?.detail)
                ? `Erro de validação: ${err.response.data.detail[0].msg}`
                : err.response?.data?.detail || 'Ocorreu um erro ao guardar a categoria.';
            setError(formattedError);
            console.error("Erro detalhado:", err.response?.data);
        } finally {
            setIsLoading(false);
        }
    };
    
    const metodosCusteio = ['FIFO', 'LIFO', 'Custo Médio'];

    return (
        <form onSubmit={handleSubmit} className="flex flex-col h-full bg-gray-50">
            <div className="flex-1 overflow-y-auto p-6">
                <div className="space-y-6 max-w-lg mx-auto">
                    <div>
                        <label htmlFor="id" className="block text-sm font-medium text-gray-700">ID</label>
                        <input
                            type="text" name="id" id="id" value={formData.id} onChange={handleChange}
                            required disabled={isEditing}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm disabled:bg-gray-100 disabled:text-gray-500"
                        />
                    </div>
                    <div>
                        <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome da Categoria</label>
                        <input
                            type="text" name="nome" id="nome" value={formData.nome} onChange={handleChange}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        />
                    </div>
                    <div>
                        <label htmlFor="metodo_custeio" className="block text-sm font-medium text-gray-700">Método de Custeio</label>
                        <select
                            id="metodo_custeio" name="metodo_custeio" value={formData.metodo_custeio} onChange={handleChange}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        >
                            {metodosCusteio.map(metodo => <option key={metodo} value={metodo}>{metodo}</option>)}
                        </select>
                    </div>
                    <div>
                        <label htmlFor="categoria_pai_id" className="block text-sm font-medium text-gray-700">Categoria Pai (Opcional)</label>
                        <SearchableSelect
                            id="categoria_pai_id"
                            value={selectedParentOption}
                            onChange={handleParentChange}
                            loadOptions={loadParentOptions}
                            isClearable
                            placeholder="Pesquise por uma categoria pai..."
                        />
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
    );
}

