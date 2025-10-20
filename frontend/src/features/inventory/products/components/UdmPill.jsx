// frontend/src/features/inventory/udm/components/UdmPill.jsx

import React from 'react';
import clsx from 'clsx';

/**
 * Componente para renderizar uma "pílula" de UDM clicável.
 * @param {object} udm - O objeto da Unidade de Medida.
 * @param {boolean} isReference - Se esta é a unidade de referência da categoria.
 * @param {function} onClick - Função a ser chamada ao clicar.
 */
export default function UdmPill({ udm, isReference, onClick }) {
    return (
        <button
            type="button"
            onClick={() => onClick(udm)}
            className={clsx(
                "px-3 py-1 text-sm font-medium rounded-full border transition-all duration-200 shadow-sm",
                isReference
                    ? "bg-indigo-600 text-white border-transparent cursor-default" // A referência não é editável diretamente
                    : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50 hover:border-gray-400"
            )}
            // Desativa o clique na unidade de referência, pois ela deve ser gerida a nível da categoria
            disabled={isReference}
            title={isReference ? `Unidade de Referência: ${udm.nome}` : `Editar ${udm.nome}`}
        >
            {udm.nome}
        </button>
    );
}

