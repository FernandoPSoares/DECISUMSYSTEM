// frontend/src/components/ui/SearchModal.jsx

import React, { Fragment, useState, useEffect } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import apiClient from '../../api/apiClient';
import DataTable from './table/DataTable';
import useDebounce from '../../hooks/useDebounce';

const ITEMS_PER_PAGE = 10;

export default function SearchModal({
    isOpen,
    onClose,
    onSelect,
    title,
    apiEndpoint,
    columns,
}) {
    const [data, setData] = useState([]);
    const [totalItems, setTotalItems] = useState(0);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    
    const [searchTerm, setSearchTerm] = useState('');
    const [sortConfig, setSortConfig] = useState({ key: 'id', direction: 'asc' });
    const [currentPage, setCurrentPage] = useState(1);
    
    const debouncedSearchTerm = useDebounce(searchTerm, 500);

    useEffect(() => {
        // --- 1. ATUALIZAÇÃO: Reinicialização do Estado ---
        // Se o modal não estiver aberto, não fazemos nada e limpamos o estado.
        if (!isOpen) {
            setSearchTerm('');
            setCurrentPage(1);
            setSortConfig({ key: 'id', direction: 'asc' });
            return;
        };

        setIsLoading(true);
        setError('');
        
        const skip = (currentPage - 1) * ITEMS_PER_PAGE;
        
        const params = new URLSearchParams({
            skip: String(skip),
            limit: String(ITEMS_PER_PAGE),
        });

        if (sortConfig.key) {
            params.append('sort_by', sortConfig.key);
            params.append('sort_order', sortConfig.direction);
        }

        if (debouncedSearchTerm) {
            params.append('search', debouncedSearchTerm);
        }
        
        const separator = apiEndpoint.includes('?') ? '&' : '?';
        const fullUrl = `${apiEndpoint}${separator}${params.toString()}`;

        apiClient.get(fullUrl)
            .then(response => {
                setData(response.data);
                
                // --- 2. ATUALIZAÇÃO: Cálculo de Paginação Seguro ---
                const total = parseInt(response.headers['x-total-count'], 10);
                if (!isNaN(total)) {
                    setTotalItems(total);
                } else {
                    // Fallback seguro se o cabeçalho não estiver presente
                    setTotalItems(response.data.length);
                    if (response.data.length >= ITEMS_PER_PAGE) {
                        console.warn("Cabeçalho 'x-total-count' não encontrado. A paginação pode não funcionar corretamente para mais de uma página.");
                    }
                }
            })
            .catch(err => {
                console.error(`Falha ao buscar dados para ${title}`, err);
                setError(`Não foi possível carregar os dados.`);
                setData([]);
                setTotalItems(0);
            })
            .finally(() => {
                setIsLoading(false);
            });
    }, [isOpen, debouncedSearchTerm, sortConfig, currentPage, apiEndpoint, title]);

    const handleSelectRow = (row) => {
        onSelect(row);
        onClose();
    };

    const handleSort = (key) => {
        setSortConfig(prevConfig => ({
            key,
            direction: prevConfig.key === key && prevConfig.direction === 'asc' ? 'desc' : 'asc',
        }));
        setCurrentPage(1);
    };

    const handlePageChange = (newPage) => {
        if (newPage > 0 && newPage <= totalPages) {
            setCurrentPage(newPage);
        }
    };
    
    const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);

    return (
        <Transition.Root show={isOpen} as={Fragment}>
            <Dialog as="div" className="relative z-30" onClose={onClose}>
                <Transition.Child as={Fragment} enter="ease-out duration-300" enterFrom="opacity-0" enterTo="opacity-100" leave="ease-in duration-200" leaveFrom="opacity-100" leaveTo="opacity-0">
                    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
                </Transition.Child>
                <div className="fixed inset-0 z-10 overflow-y-auto">
                    <div className="flex min-h-full items-start justify-center p-4 text-center sm:p-6">
                        <Transition.Child as={Fragment} enter="ease-out duration-300" enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enterTo="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200" leaveFrom="opacity-100 translate-y-0 sm:scale-100" leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
                            <Dialog.Panel className="relative transform rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 w-full sm:max-w-3xl">
                                <div className="flex flex-col h-[70vh]">
                                    <div className="p-4 sm:p-6 border-b border-gray-200">
                                        <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900">{title}</Dialog.Title>
                                        <div className="mt-4 relative">
                                            <MagnifyingGlassIcon className="pointer-events-none absolute top-1/2 left-3 h-5 w-5 -translate-y-1/2 text-gray-400" />
                                            <input
                                                type="search"
                                                placeholder="Pesquisar..."
                                                value={searchTerm}
                                                onChange={(e) => setSearchTerm(e.target.value)}
                                                className="w-full rounded-md border-gray-300 pl-10 sm:text-sm shadow-sm"
                                            />
                                        </div>
                                    </div>
                                    <div className="flex-1 overflow-hidden">
                                        <DataTable
                                            columns={columns}
                                            data={data}
                                            isLoading={isLoading}
                                            error={error}
                                            onRowClick={handleSelectRow}
                                            sortConfig={sortConfig}
                                            onSort={handleSort}
                                            pagination={{ currentPage, totalPages, onPageChange: handlePageChange }}
                                        />
                                    </div>
                                </div>
                            </Dialog.Panel>
                        </Transition.Child>
                    </div>
                </div>
            </Dialog>
        </Transition.Root>
    );
}

