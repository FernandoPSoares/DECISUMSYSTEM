// frontend/src/components/ui/table/DataTable.jsx

import React from 'react';
// --- 1. IMPORTAÇÕES DE ÍCONES CORRIGIDAS ---
import { 
    PencilIcon, 
    TrashIcon, 
    CheckCircleIcon, 
    ChevronUpIcon, 
    ChevronDownIcon 
} from '@heroicons/react/24/outline';
import Spinner from '../Spinner';
import clsx from 'clsx';

export default function DataTable({
    columns,
    data,
    isLoading,
    error,
    onEdit,
    onDeactivate,
    onActivate,
    onRowClick,
    
    // As nossas novas propriedades para ordenação e paginação
    sortConfig,
    onSort,
    pagination,
}) {
    const hasActions = onEdit || onDeactivate || onActivate;
    // Adiciona a coluna de "Ações" apenas se uma das funções de ação for fornecida
    const finalColumns = hasActions
        ? [...columns, { header: 'Ações', accessor: 'actions' }]
        : columns;

    const isRowClickable = !!onRowClick;

    // --- 2. FUNÇÃO EM FALTA ADICIONADA AQUI ---
    // Esta função renderiza o ícone de seta correto com base no estado da ordenação.
    const renderSortIcon = (columnKey) => {
        if (!sortConfig || sortConfig.key !== columnKey) {
            // Retorna um ícone invisível para manter o alinhamento
            return <ChevronUpIcon className="w-4 h-4 text-transparent" />; 
        }
        if (sortConfig.direction === 'asc') {
            return <ChevronUpIcon className="w-4 h-4 text-gray-600" />;
        }
        return <ChevronDownIcon className="w-4 h-4 text-gray-600" />;
    };

    return (
        <div className="bg-white shadow-md rounded-lg overflow-hidden flex flex-col h-full">
            <div className="overflow-x-auto flex-grow">
                {isLoading && (
                    <div className="flex items-center justify-center h-64">
                        <Spinner />
                    </div>
                )}
                {error && (
                    <div className="p-6 text-center text-red-600">
                        <p>{error}</p>
                    </div>
                )}
                {!isLoading && !error && data && data.length === 0 && (
                    <div className="p-6 text-center text-gray-500">
                        <p>Nenhum resultado encontrado.</p>
                    </div>
                )}
                
                {!isLoading && !error && data && data.length > 0 && (
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                {finalColumns.map((col) => (
                                    <th
                                        key={col.header}
                                        scope="col"
                                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        {col.sortable ? (
                                            <button
                                                onClick={() => onSort(col.accessor)}
                                                className="flex items-center space-x-1 group focus:outline-none"
                                            >
                                                <span>{col.header}</span>
                                                <span className={clsx(
                                                    'transition-opacity', 
                                                    sortConfig && sortConfig.key === col.accessor 
                                                        ? 'opacity-100' 
                                                        : 'opacity-0 group-hover:opacity-100'
                                                )}>
                                                    {renderSortIcon(col.accessor)}
                                                </span>
                                            </button>
                                        ) : (
                                            col.header
                                        )}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {data.map((row) => (
                                <tr 
                                    key={row.id} 
                                    onClick={() => isRowClickable && onRowClick(row)}
                                    className={clsx('transition-colors', isRowClickable ? 'cursor-pointer hover:bg-indigo-50' : 'hover:bg-gray-50')}
                                >
                                    {columns.map((col) => (
                                        <td key={col.accessor} className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            {/* O operador 'get' opcional previne erros se o accessor for aninhado (ex: 'role.nome') e o objeto for nulo */}
                                            {col.cell ? col.cell(row) : col.accessor.split('.').reduce((o, i) => o?.[i], row)}
                                        </td>
                                    ))}
                                    {hasActions && (
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-4 text-right">
                                            {onEdit && (
                                                <button onClick={(e) => { e.stopPropagation(); onEdit(row); }} className="text-indigo-600 hover:text-indigo-900 transition-colors" title="Editar">
                                                    <PencilIcon className="w-5 h-5" />
                                                </button>
                                            )}
                                            {row.is_active && onDeactivate && (
                                                <button onClick={(e) => { e.stopPropagation(); onDeactivate(row); }} className="text-red-600 hover:text-red-900 transition-colors" title="Desativar">
                                                    <TrashIcon className="w-5 h-5" />
                                                </button>
                                            )}
                                            {!row.is_active && onActivate && (
                                                <button onClick={(e) => { e.stopPropagation(); onActivate(row); }} className="text-green-600 hover:text-green-900 transition-colors" title="Ativar">
                                                    <CheckCircleIcon className="w-5 h-5" />
                                                </button>
                                            )}
                                        </td>
                                    )}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>

            {pagination && pagination.totalPages > 1 && !isLoading && (
                <div className="px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 bg-white rounded-b-lg">
                    <div>
                        <p className="text-sm text-gray-700">
                            Página <span className="font-medium">{pagination.currentPage}</span> de <span className="font-medium">{pagination.totalPages}</span>
                        </p>
                    </div>
                    <div>
                        <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                            <button
                                onClick={() => pagination.onPageChange(pagination.currentPage - 1)}
                                disabled={pagination.currentPage === 1}
                                className="relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Anterior
                            </button>
                            <button
                                onClick={() => pagination.onPageChange(pagination.currentPage + 1)}
                                disabled={pagination.currentPage >= pagination.totalPages}
                                className="relative inline-flex items-center px-4 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Próximo
                            </button>
                        </nav>
                    </div>
                </div>
            )}
        </div>
    );
}

