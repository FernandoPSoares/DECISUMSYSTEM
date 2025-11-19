// File: frontend/src/components/ui/SearchableSelect.jsx

import React from 'react';
import AsyncSelect from 'react-select/async';
import PropTypes from 'prop-types';

/**
 * SearchableSelect - Componente de Seleção Assíncrona de Alta Performance.
 * * Características:
 * 1. Usa react-select/async para carregamento sob demanda.
 * 2. Usa Portais para renderizar o menu fora do fluxo do DOM (resolve problemas de z-index em Modais).
 * 3. Estilização compatível com Tailwind CSS.
 */
const SearchableSelect = ({
  value,            // Pode ser um ID (string/number) ou Objeto {value, label}
  onChange,         // Retorna o objeto {value, label} ou null
  options,          // Array de opções para modo síncrono
  loadOptions,      // Função (inputValue) => Promise<Options[]>
  defaultOptions = true, // Se true, carrega opções iniciais imediatamente. Se array, usa como iniciais.
  placeholder = "Selecione...",
  isDisabled = false,
  isClearable = true,
  error = null,     // Mensagem de erro para exibir borda vermelha
  className = "",
}) => {

  // --- Estilos Customizados (Tailwind-like) ---
  const customStyles = {
    control: (base, state) => ({
      ...base,
      minHeight: '38px',
      borderRadius: '0.5rem', // rounded-lg
      borderColor: error ? '#EF4444' : state.isFocused ? '#3B82F6' : '#D1D5DB', // red-500 / blue-500 / gray-300
      boxShadow: state.isFocused 
        ? error ? '0 0 0 1px #EF4444' : '0 0 0 1px #3B82F6' 
        : 'none',
      '&:hover': {
        borderColor: error ? '#EF4444' : state.isFocused ? '#3B82F6' : '#9CA3AF', // gray-400
      },
      backgroundColor: isDisabled ? '#F3F4F6' : 'white',
    }),
    menu: (base) => ({
      ...base,
      zIndex: 9999, // Fallback, mas o Portal resolve isto
      borderRadius: '0.5rem',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    }),
    menuPortal: (base) => ({ 
      ...base, 
      zIndex: 9999 // Garante que fica acima de qualquer Modal
    }),
    placeholder: (base) => ({
      ...base,
      color: '#9CA3AF',
      fontSize: '0.875rem',
    }),
    singleValue: (base) => ({
      ...base,
      color: '#111827',
      fontSize: '0.875rem',
    }),
    option: (base, state) => ({
      ...base,
      backgroundColor: state.isSelected 
        ? '#2563EB' // blue-600
        : state.isFocused 
          ? '#EFF6FF' // blue-50
          : 'transparent',
      color: state.isSelected ? 'white' : '#1F2937',
      cursor: 'pointer',
      fontSize: '0.875rem',
      ':active': {
        backgroundColor: '#2563EB',
        color: 'white',
      },
    }),
  };

  return (
    <div className={className}>
      <AsyncSelect
        // --- Propriedades Core ---
        value={value}
        onChange={onChange}
        options={options} // Adicionado para modo síncrono
        loadOptions={loadOptions}
        defaultOptions={defaultOptions}
        
        // --- Comportamento ---
        isClearable={isClearable}
        isDisabled={isDisabled}
        cacheOptions={true} // Cacheia resultados da pesquisa para performance
        
        // --- UI/UX ---
        placeholder={placeholder}
        loadingMessage={() => "A carregar..."}
        noOptionsMessage={({ inputValue }) => 
          inputValue ? "Nenhum resultado encontrado" : "Digite para pesquisar..."
        }
        
        // --- A Mágica do Portal (Resolve Z-Index) ---
        menuPortalTarget={typeof document !== 'undefined' ? document.body : null}
        styles={customStyles}
        
        // --- Classes CSS ---
        classNames={{
          container: () => "w-full",
        }}
      />
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  );
};

SearchableSelect.propTypes = {
  value: PropTypes.any,
  onChange: PropTypes.func.isRequired,
  loadOptions: PropTypes.func, // Não é mais obrigatório
  options: PropTypes.array,
};

export default SearchableSelect;