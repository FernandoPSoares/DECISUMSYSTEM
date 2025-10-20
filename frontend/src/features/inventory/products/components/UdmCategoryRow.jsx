// frontend/src/features/inventory/products/components/UdmCategoryRow.jsx

import React from 'react';
import UdmPill from './UdmPill';
import { PlusCircleIcon, PencilIcon, ArrowUturnLeftIcon, TrashIcon } from '@heroicons/react/24/outline';
import clsx from 'clsx';

export default function UdmCategoryRow({ 
    category, 
    onEditUdm, 
    onAddUdm, 
    onEditCategory,
    isArchivedView,
    onReactivateCategory,
    onReactivateUdm,
    onDeactivateCategory,
    onDeactivateUdm
}) {
    const isCategoryInactive = !category.is_active;

    return (
        <div className={clsx(
            // --- 1. ALINHAMENTO CORRIGIDO ---
            // A classe 'items-center' garante o alinhamento vertical central
            "grid grid-cols-[250px,1fr] items-center gap-x-6 py-4 px-6 border-b border-gray-200 last:border-b-0 group",
            isArchivedView && !isCategoryInactive && "bg-gray-50/50"
        )}>
            {/* Coluna da Categoria */}
            <div className="flex items-center space-x-2">
                <span className="font-semibold text-gray-800 truncate" title={category.nome}>{category.nome}</span>
                
                {isArchivedView ? (
                    isCategoryInactive && (
                        <button 
                            onClick={() => onReactivateCategory(category)}
                            className="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0"
                            title={`Reativar categoria ${category.nome}`}
                        >
                            <ArrowUturnLeftIcon className="w-4 h-4" />
                        </button>
                    )
                ) : (
                    <div className="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0">
                        <button 
                            onClick={() => onEditCategory(category)}
                            className="text-gray-400 hover:text-indigo-600"
                            title={`Editar categoria ${category.nome}`}
                        >
                            <PencilIcon className="w-4 h-4" />
                        </button>
                        <button 
                            onClick={() => onDeactivateCategory(category)}
                            className="text-gray-400 hover:text-red-600"
                            title={`Desativar categoria ${category.nome}`}
                        >
                            <TrashIcon className="w-4 h-4" />
                        </button>
                    </div>
                )}
            </div>
            
            {/* Coluna das UDMs */}
            <div className="flex items-center flex-wrap gap-2">
                {category.udms.sort((a) => (a.id === category.unidade_referencia_id ? -1 : 1)).map(udm => (
                    <UdmPill
                        key={udm.id}
                        udm={udm}
                        isReference={category.unidade_referencia_id === udm.id}
                        onEdit={onEditUdm}
                        isArchivedView={isArchivedView}
                        onReactivate={onReactivateUdm}
                        onDeactivate={onDeactivateUdm}
                    />
                ))}
                
                {!isArchivedView && (
                    <button 
                        onClick={() => onAddUdm(category)}
                        className="flex items-center justify-center w-8 h-8 text-gray-400 bg-gray-100 rounded-full hover:bg-indigo-100 hover:text-indigo-600 transition-colors opacity-0 group-hover:opacity-100"
                        title={`Adicionar UDM a ${category.nome}`}
                    >
                        <PlusCircleIcon className="w-6 h-6" />
                    </button>
                )}
            </div>
        </div>
    );
}

