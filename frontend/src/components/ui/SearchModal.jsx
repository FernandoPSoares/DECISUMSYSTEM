// File: frontend/src/components/ui/SearchModal.jsx
import React, { useState, useEffect, useRef } from 'react';
import Modal from './Modal';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

/**
 * Modal de Pesquisa Simplificado (Client-Side).
 * Recebe uma lista de 'options' e filtra localmente.
 * Ideal para Lookup Tables (Fabricantes, Locais, etc).
 */
const SearchModal = ({ isOpen, onClose, title, options = [], onSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredOptions, setFilteredOptions] = useState([]);
  const inputRef = useRef(null);

  // 1. Focar no input e reiniciar lista ao abrir
  useEffect(() => {
    if (isOpen) {
      // Pequeno delay para garantir que o modal renderizou
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
      
      setSearchTerm('');
      setFilteredOptions(options || []);
    }
  }, [isOpen, options]);

  // 2. Lógica de Filtro Local (em tempo real)
  useEffect(() => {
    if (!options) return;

    const lowerTerm = searchTerm.toLowerCase();
    
    // Filtra as opções baseado no label
    const results = options.filter((opt) =>
      String(opt.label).toLowerCase().includes(lowerTerm)
    );
    
    setFilteredOptions(results);
  }, [searchTerm, options]);

  const handleSelect = (option) => {
    onSelect(option); // Devolve o objeto selecionado {value, label}
    onClose();
  };

  return (
    // zIndex alto para garantir que fica acima de outros modais
    <Modal 
      isOpen={isOpen} 
      onClose={onClose} 
      title={title || "Selecionar Item"} 
      maxWidth="md" 
      zIndex={60} 
    >
      
      {/* Barra de Pesquisa */}
      <div className="relative mb-4">
        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
          <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
        </div>
        <input
          ref={inputRef}
          type="text"
          className="block w-full rounded-md border-0 py-2.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 outline-none"
          placeholder="Digite para filtrar..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Lista de Resultados */}
      <div className="max-h-60 overflow-y-auto pr-1 border-t border-gray-100 pt-2">
        {filteredOptions.length > 0 ? (
          <ul className="divide-y divide-gray-50">
            {filteredOptions.map((option) => (
              <li
                key={option.value}
                onClick={() => handleSelect(option)}
                className="cursor-pointer py-3 px-3 hover:bg-blue-50 rounded-md transition-colors flex items-center justify-between group"
              >
                <span className="text-sm font-medium text-gray-700 group-hover:text-blue-700">
                  {option.label}
                </span>
                {/* Você pode adicionar um ícone de check se option.value === selectedValue */}
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center py-8 text-gray-500 text-sm flex flex-col items-center">
            <MagnifyingGlassIcon className="h-8 w-8 text-gray-300 mb-2" />
            <span>Nenhum resultado encontrado.</span>
          </div>
        )}
      </div>
    </Modal>
  );
};

export default SearchModal;