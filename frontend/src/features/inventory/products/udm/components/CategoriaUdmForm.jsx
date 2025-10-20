// frontend/src/features/inventory/products/udm/components/CategoriaUdmForm.jsx

import React, { useState, useEffect } from 'react';

export default function CategoriaUdmForm({ categoriaToEdit, onSave, onCancel, onChangeReference }) {
    const isEditing = !!categoriaToEdit;
    
    const [formData, setFormData] = useState({
        id: '',
        nome: '',
        unidade_referencia_id: '',
        unidade_referencia_nome: ''
    });

    useEffect(() => {
        if (isEditing) {
            setFormData({
                id: categoriaToEdit.id || '',
                nome: categoriaToEdit.nome || '',
                unidade_referencia_id: categoriaToEdit.unidade_referencia?.id || '',
                unidade_referencia_nome: categoriaToEdit.unidade_referencia?.nome || ''
            });
        }
    }, [categoriaToEdit, isEditing]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const dataToSend = isEditing ? { nome: formData.nome } : formData;
        onSave(dataToSend);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label htmlFor="id" className="block text-sm font-medium text-gray-700">ID da Categoria</label>
                <input
                    type="text"
                    name="id"
                    id="id"
                    value={formData.id}
                    onChange={handleChange}
                    disabled={isEditing}
                    required
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm disabled:bg-gray-100"
                />
            </div>

            <div>
                <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome da Categoria</label>
                <input
                    type="text"
                    name="nome"
                    id="nome"
                    value={formData.nome}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
            </div>
            
            {/* --- 2. CAMPO DE REFERÊNCIA COM OPÇÃO DE ALTERAR --- */}
            <div>
                <label htmlFor="unidade_referencia_id" className="block text-sm font-medium text-gray-700">Unidade de Referência</label>
                <div className="flex items-center space-x-2 mt-1">
                    <input
                        type="text"
                        value={isEditing ? `${formData.unidade_referencia_nome} (${formData.unidade_referencia_id})` : formData.unidade_referencia_id}
                        onChange={(e) => isEditing ? null : handleChange(e)}
                        name="unidade_referencia_id"
                        id="unidade_referencia_id"
                        placeholder={isEditing ? '' : 'ID da UDM de Referência'}
                        disabled={isEditing}
                        required
                        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm disabled:bg-gray-100"
                    />
                    {isEditing && (
                        <button 
                            type="button"
                            onClick={onChangeReference}
                            className="px-4 py-2 text-sm font-medium text-indigo-700 bg-indigo-100 border border-transparent rounded-md hover:bg-indigo-200"
                        >
                            Alterar
                        </button>
                    )}
                </div>
            </div>

            {!isEditing && (
                 <div>
                    <label htmlFor="unidade_referencia_nome" className="block text-sm font-medium text-gray-700">Nome da Unidade de Referência</label>
                    <input
                        type="text"
                        name="unidade_referencia_nome"
                        id="unidade_referencia_nome"
                        value={formData.unidade_referencia_nome}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                </div>
            )}
            
            <div className="flex justify-end space-x-2 pt-4">
                <button type="button" onClick={onCancel} className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50">
                    Cancelar
                </button>
                <button type="submit" className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700">
                    {isEditing ? 'Guardar Alterações' : 'Criar Categoria'}
                </button>
            </div>
        </form>
    );
}
