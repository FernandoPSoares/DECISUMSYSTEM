// frontend/src/components/ui/SearchableSelect.jsx

import React from 'react';
// --- CORREÇÃO: Alterado para importar o componente base do 'react-select' ---
import Select from 'react-select';
import Async from 'react-select/async';


// Componente de dropdown com pesquisa, corrigido para usar Promises.
export default function SearchableSelect({
  value,
  onChange,
  loadOptions, // Espera uma função async que retorna um array de opções
  placeholder = "Selecione...",
  onAdvancedSearchClick,
  ...props
}) {
  
  // Adaptador que garante que loadOptions retorne uma Promise
  // e adiciona a opção de "Pesquisa Avançada"
  const adaptedLoadOptions = (inputValue) =>
    new Promise((resolve) => {
      if (typeof loadOptions !== 'function') {
        console.error("SearchableSelect: 'loadOptions' não é uma função.");
        resolve([]);
        return;
      }
      
      loadOptions(inputValue)
        .then(options => {
          if (onAdvancedSearchClick) {
            const advancedSearchOption = {
              value: '__ADVANCED_SEARCH__',
              label: 'Pesquisar mais...',
              isFixed: true,
            };
            resolve([...options, advancedSearchOption]);
          } else {
            resolve(options);
          }
        })
        .catch(error => {
          console.error("Erro ao carregar opções no SearchableSelect:", error);
          resolve([]);
        });
    });

  const handleChange = (selectedOption) => {
    if (selectedOption && selectedOption.value === '__ADVANCED_SEARCH__') {
      onAdvancedSearchClick();
    } else {
      onChange(selectedOption);
    }
  };

  const customStyles = {
     option: (provided, state) => {
      const commonStyles = { ...provided, paddingTop: '4px', paddingBottom: '4px' };
      if (state.data.value === '__ADVANCED_SEARCH__') {
        return {
          ...commonStyles,
          fontSize: '13px', paddingLeft: '24px', color: '#2563EB',
          backgroundColor: state.isFocused ? '#EFF6FF' : 'white',
          textDecoration: state.isFocused ? 'underline' : 'none',
        };
      }
      return {
        ...commonStyles, fontSize: '15px',
        backgroundColor: state.isSelected ? '#4F46E5' : state.isFocused ? '#E0E7FF' : 'white',
        color: state.isSelected ? 'white' : '#1F2937',
        ':active': { backgroundColor: state.isSelected ? '#4F46E5' : '#E0E7FF' },
      };
    },
     control: (provided, state) => ({
        ...provided, width: '100%', padding: '2px 4px', color: '#111827',
        backgroundColor: 'rgba(255, 255, 255, 0.5)', border: '1px solid #D1D5DB',
        borderRadius: '0.5rem', boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        transition: 'all 0.2s ease-in-out',
        ...(state.isFocused && { 
            outline: '2px solid transparent', outlineOffset: '2px',
            '--tw-ring-color': '#6366F1', boxShadow: '0 0 0 2px var(--tw-ring-color)',
            borderColor: 'transparent',
        }),
    }),
    input: (provided) => ({ ...provided, color: '#111827' }),
    placeholder: (provided) => ({ ...provided, color: '#9CA3AF' }),
    singleValue: (provided) => ({ ...provided, color: '#111827' }),
    menu: (provided) => ({
        ...provided, marginTop: '4px', padding: '8px', backgroundColor: 'white',
        border: '1px solid #E5E7EB', borderRadius: '0.5rem',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    }),
    dropdownIndicator: (provided) => ({ ...provided, color: '#9CA3AF', ':hover': { color: '#4B5563' } }),
    clearIndicator: (provided) => ({ ...provided, color: '#9CA3AF', ':hover': { color: '#EF4444' } }),
    indicatorSeparator: (provided) => ({ ...provided, backgroundColor: '#E5E7EB' }),
  };

  return (
    // --- CORREÇÃO: Alterado para usar o componente <Select> base ---
    // A biblioteca 'react-select' deteta automaticamente a prop 'loadOptions'
    // e ativa o modo assíncrono.
    <Async
      value={value}
      onChange={handleChange}
      loadOptions={adaptedLoadOptions}
      placeholder={placeholder}
      cacheOptions
      defaultOptions
      isClearable
      loadingMessage={() => "A pesquisar..."}
      noOptionsMessage={({ inputValue }) =>
        inputValue ? "Nenhum resultado encontrado" : "Digite para pesquisar"
      }
      styles={customStyles}
      {...props}
    />
  );
}

