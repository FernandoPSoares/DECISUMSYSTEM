// frontend/src/features/inventory/products/udm/components/CategoriaUdmForm.jsx

import React, { useState, useEffect } from 'react';
import Spinner from '../../../../../components/ui/Spinner';

export default function CategoriaUdmForm({ categoriaToEdit, onSave, onCancel }) {
    // --- 1. ESTADO ATUALIZADO ---
    // O formulário agora gere os novos campos da unidade de referência.
    const [formData, setFormData] = useState({
        id: '',
        nome: '',
        unidade_referencia_id: '',
        unidade_referencia_nome: '',
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    // A edição de uma Categoria agora foca-se apenas no nome.
    // A unidade de referência, uma vez criada, é imutável.
    const isEditing = !!categoriaToEdit;

    useEffect(() => {
        if (categoriaToEdit) {
            setFormData({
                id: categoriaToEdit.id || '',
                nome: categoriaToEdit.nome || '',
                // Os campos de referência não são editáveis, mas podem ser mostrados.
                unidade_referencia_id: categoriaToEdit.unidade_referencia?.id || '',
                unidade_referencia_nome: categoriaToEdit.unidade_referencia?.nome || '',
            });
        }
    }, [categoriaToEdit]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        try {
            // Apenas os dados do nome são enviados na edição
            const dataToSend = isEditing ? { nome: formData.nome } : formData;
            await onSave(dataToSend);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ocorreu um erro ao guardar a categoria.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col h-full bg-gray-50">
            <div className="flex-1 overflow-y-auto p-6">
                <div className="space-y-6 max-w-lg mx-auto">
                    <div>
                        <label htmlFor="id" className="block text-sm font-medium text-gray-700">ID da Categoria</label>
                        <input type="text" name="id" id="id" value={formData.id} onChange={handleChange} required disabled={isEditing} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm disabled:bg-gray-100 disabled:text-gray-500" placeholder="Ex: PESO, VOLUME" />
                    </div>
                    <div>
                        <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome da Categoria</label>
                        <input type="text" name="nome" id="nome" value={formData.nome} onChange={handleChange} required className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm" placeholder="Ex: Peso, Volume, Comprimento" />
                    </div>

                    {/* --- 2. NOVOS CAMPOS ADICIONADOS --- */}
                    {/* Estes campos só são editáveis na criação. */}
                    <div className="border-t border-gray-200 pt-6">
                        <h3 className="text-base font-semibold text-gray-800">Unidade de Referência</h3>
                        <p className="text-xs text-gray-500 mb-4">Defina a unidade base para esta categoria (ex: para a categoria 'Peso', a referência seria 'Quilograma').</p>
                        <div className="space-y-4">
                            <div>
                                <label htmlFor="unidade_referencia_id" className="block text-sm font-medium text-gray-700">ID da Unidade de Referência</label>
                                <input
                                    type="text" name="unidade_referencia_id" id="unidade_referencia_id"
                                    value={formData.unidade_referencia_id} onChange={handleChange}
                                    required disabled={isEditing}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm disabled:bg-gray-100"
                                    placeholder="Ex: KG, L, M"
                                />
                            </div>
                            <div>
                                <label htmlFor="unidade_referencia_nome" className="block text-sm font-medium text-gray-700">Nome da Unidade de Referência</label>
                                <input
                                    type="text" name="unidade_referencia_nome" id="unidade_referencia_nome"
                                    value={formData.unidade_referencia_nome} onChange={handleChange}
                                    required disabled={isEditing}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm disabled:bg-gray-100"
                                    placeholder="Ex: Quilograma, Litro, Metro"
                                />
                            </div>
                        </div>
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

