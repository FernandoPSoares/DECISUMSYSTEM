// frontend/src/features/inventory/products/brands/components/MarcaForm.jsx

import React, { useState, useEffect } from 'react';
import Spinner from '../../../../../components/ui/Spinner';

export default function MarcaForm({ marcaToEdit, onSave, onCancel }) {
    const [formData, setFormData] = useState({
        id: '',
        nome: '',
    });
    const [isLoading, setIsLoading] = useState(false);

    const isEditing = !!marcaToEdit?.nome;

    useEffect(() => {
        if (marcaToEdit) {
            setFormData({
                id: marcaToEdit.id || '',
                nome: marcaToEdit.nome || '',
            });
        }
    }, [marcaToEdit]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        // Em edição, enviamos apenas o que pode ser alterado (nome)
        const dataToSend = isEditing ? { nome: formData.nome } : formData;
        await onSave(dataToSend);
        setIsLoading(false);
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col h-full bg-gray-50">
            <div className="flex-1 overflow-y-auto p-6">
                <div className="space-y-6 max-w-lg mx-auto">
                    <div>
                        <label htmlFor="id" className="block text-sm font-medium text-gray-700">ID da Marca</label>
                        <input
                            type="text"
                            name="id"
                            id="id"
                            value={formData.id}
                            onChange={handleChange}
                            required
                            disabled={isEditing}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm disabled:bg-gray-100 disabled:text-gray-500"
                            placeholder="Ex: NIKE, ADIDAS, etc."
                        />
                    </div>
                    <div>
                        <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome da Marca</label>
                        <input
                            type="text"
                            name="nome"
                            id="nome"
                            value={formData.nome}
                            onChange={handleChange}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                            placeholder="Ex: Nike, Adidas, etc."
                        />
                    </div>
                </div>
            </div>

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
                    {isLoading ? <Spinner size="sm" /> : (isEditing ? 'Guardar Alterações' : 'Criar Marca')}
                </button>
            </div>
        </form>
    );
}
