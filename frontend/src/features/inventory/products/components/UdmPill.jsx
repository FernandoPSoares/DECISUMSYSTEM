// frontend/src/features/inventory/products/components/UdmPill.jsx

import React from 'react';
import { StarIcon, PencilIcon, TrashIcon, ArrowUturnLeftIcon } from '@heroicons/react/24/solid';
import clsx from 'clsx';

export default function UdmPill({
    udm,
    isReference,
    onEdit,
    isArchivedView,
    onReactivate,
    onDeactivate
}) {

    if (isArchivedView) {
        return (
            <button
                onClick={() => onReactivate(udm)}
                title={`Reativar ${udm.nome}`}
                className={clsx(
                    "flex items-center gap-1.5 h-8 px-3 rounded-full text-xs font-semibold transition-colors",
                    isReference
                        ? "bg-amber-100 text-amber-800 hover:bg-amber-200"
                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                )}
            >
                {isReference && <StarIcon className="w-4 h-4 text-amber-600" />}
                <span className="truncate">{udm.nome}</span>
                <ArrowUturnLeftIcon className="w-4 h-4" />
            </button>
        );
    }
    
    // --- 3. COMPONENTE DE REFERÊNCIA AGORA É UM GRUPO COM BOTÃO DE EDITAR ---
    if (isReference) {
        return (
            <div
                title="Unidade de Referência"
                className="relative flex items-center gap-2 h-8 px-4 rounded-full text-sm font-bold bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg group/pill"
            >
                <StarIcon className="w-5 h-5" />
                <span className="truncate">{udm.nome}</span>
                <div className="absolute inset-0 flex items-center justify-end pr-2 opacity-0 group-hover/pill:opacity-100 transition-opacity">
                     <button onClick={() => onEdit(udm)} className="p-1 rounded-full hover:bg-white/20" title={`Editar ${udm.nome}`}>
                        <PencilIcon className="w-4 h-4" />
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="relative group/pill">
            <div className="flex items-center gap-1.5 h-8 px-3 rounded-full text-xs font-semibold bg-gray-100 text-gray-800">
                <span className="truncate">{udm.nome}</span>
            </div>
            <div className="absolute inset-0 flex items-center justify-center gap-x-2 bg-gray-800/70 rounded-full opacity-0 group-hover/pill:opacity-100 transition-opacity">
                <button onClick={() => onEdit(udm)} className="text-white hover:text-indigo-300" title={`Editar ${udm.nome}`}>
                    <PencilIcon className="w-4 h-4" />
                </button>
                <button onClick={() => onDeactivate(udm)} className="text-white hover:text-red-400" title={`Desativar ${udm.nome}`}>
                    <TrashIcon className="w-4 h-4" />
                </button>
            </div>
        </div>
    );
}

