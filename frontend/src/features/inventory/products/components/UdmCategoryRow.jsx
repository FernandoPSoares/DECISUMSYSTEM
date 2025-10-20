// frontend/src/features/inventory/products/components/UdmCategoryRow.jsx

import React from 'react';
import UdmPill from './UdmPill';
import { PlusCircleIcon, PencilIcon } from '@heroicons/react/24/outline';

/**
 * Componente para renderizar uma linha completa de Categoria com as suas UDMs.
 */
export default function UdmCategoryRow({ category, onEditUdm, onAddUdm, onEditCategory }) {
    return (
        <div className="grid grid-cols-[250px,1fr] items-start gap-x-6 py-4 border-b border-gray-200 last:border-b-0 group">
            {/* Coluna da Categoria */}
            <div className="flex items-center space-x-2 sticky left-0">
                <span className="font-semibold text-gray-800">{category.nome}</span>
                <button 
                    onClick={() => onEditCategory(category)}
                    className="text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity"
                    title={`Editar categoria ${category.nome}`}
                >
                    <PencilIcon className="w-4 h-4" />
                </button>
            </div>
            
            {/* Coluna das UDMs */}
            <div className="flex items-center flex-wrap gap-2">
                {category.udms.sort((a) => (a.id === category.unidade_referencia_id ? -1 : 1)).map(udm => (
                    <UdmPill
                        key={udm.id}
                        udm={udm}
                        isReference={category.unidade_referencia_id === udm.id}
                        onClick={onEditUdm}
                    />
                ))}
                <button 
                    onClick={() => onAddUdm(category)}
                    className="flex items-center justify-center w-8 h-8 text-gray-400 bg-gray-100 rounded-full hover:bg-indigo-100 hover:text-indigo-600 transition-colors opacity-0 group-hover:opacity-100"
                    title={`Adicionar UDM a ${category.nome}`}
                >
                    <PlusCircleIcon className="w-6 h-6" />
                </button>
            </div>
        </div>
    );
}
