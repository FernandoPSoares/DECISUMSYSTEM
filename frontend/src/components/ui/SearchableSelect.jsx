// frontend/src/components/ui/SearchableSelect.jsx

import React from 'react';
import AsyncSelect from 'react-select/async';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

// O nosso componente de dropdown, agora com a opção de pesquisa avançada.
export default function SearchableSelect({
  value,
  onChange,
  loadOptions,
  placeholder = "Selecione...",
  onAdvancedSearchClick, // <-- 1. NOVA PROPRIEDADE PARA ABRIR O MODAL
  ...props
}) {
  // Função que envolve a 'loadOptions' para adicionar a opção de pesquisa avançada
  const loadOptionsWithAdvancedSearch = (inputValue, callback) => {
    loadOptions(inputValue, (options) => {
      if (onAdvancedSearchClick) {
        // --- 2. ADIÇÃO DA OPÇÃO ESPECIAL ---
        const advancedSearchOption = {
          value: '__ADVANCED_SEARCH__', // Um valor especial para identificar o clique
          label: 'Pesquisar mais...',
          isFixed: true, // Garante que esta opção não é filtrada
        };
        callback([...options, advancedSearchOption]);
      } else {
        callback(options);
      }
    });
  };

  // --- 3. LÓGICA DE MANIPULAÇÃO DO CLIQUE ---
  // A função onChange agora verifica se a opção especial foi clicada
  const handleChange = (selectedOption) => {
    if (selectedOption && selectedOption.value === '__ADVANCED_SEARCH__') {
      onAdvancedSearchClick();
    } else {
      onChange(selectedOption);
    }
  };

    // --- 1. NOVA ABORDAGEM: Objeto de estilos customizados ---
  // Estes estilos são injetados diretamente e têm prioridade máxima.
  const customStyles = {
    option: (provided, state) => {
      // Estilos base que serão aplicados a TODAS as opções para diminuir a altura.
      // py-1 no Tailwind.
      const commonStyles = {
        ...provided, // Herda os estilos base da biblioteca
        paddingTop: '4px',
        paddingBottom: '4px',
      };

      // Se for a nossa opção especial de "Pesquisar mais..."
      if (state.data.value === '__ADVANCED_SEARCH__') {
        return {
          ...commonStyles, // Aplica os estilos comuns de altura
          fontSize: '13px',
          paddingLeft: '24px',
          color: '#2563EB',
          backgroundColor: state.isFocused ? '#EFF6FF' : 'white',
          textDecoration: state.isFocused ? 'underline' : 'none',
        };
      }

      // Para todas as outras opções normais
      return {
        ...commonStyles, // Aplica apenas os estilos comuns de altura
        fontSize: '15px',
        backgroundColor: state.isSelected 
            ? '#4F46E5' // Cor de fundo quando selecionado (indigo-600)
            : state.isFocused 
            ? '#E0E7FF' // Cor de fundo no hover/focus (indigo-100)
            : 'white',
        color: state.isSelected 
            ? 'white' 
            : '#1F2937', // Cor do texto (gray-800)
        ':active': { // Garante que a cor de fundo não mude no clique
          backgroundColor: state.isSelected ? '#4F46E5' : '#E0E7FF',
        },
      };
    },
  };

  return (
    <AsyncSelect
      value={value}
      onChange={handleChange}
      loadOptions={loadOptionsWithAdvancedSearch}
      placeholder={placeholder}
      cacheOptions
      defaultOptions
      isClearable
      loadingMessage={() => "A pesquisar..."}
      noOptionsMessage={({ inputValue }) =>
        inputValue ? "Nenhum resultado encontrado" : "Digite para pesquisar"
      }
      
      // --- 2. ADICIONA A NOVA PROP DE ESTILOS AQUI ---
      styles={customStyles}

      // Mantenha as outras classNames, mas REMOVA a chave "option" daqui.
      classNames={{
        control: (state) => `
          w-full px-2 py-1 text-gray-900 bg-white/50 border border-gray-300 rounded-lg shadow-sm
          transition-colors duration-200
          ${state.isFocused ? 'ring-2 ring-indigo-500 border-transparent' : ''}
        `,
        input: () => 'text-gray-900',
        placeholder: () => 'text-gray-400',
        singleValue: () => 'text-gray-900',
        menu: () => 'mt-1 p-2 bg-white border border-gray-200 rounded-lg shadow-lg',
        dropdownIndicator: () => 'text-gray-400 hover:text-gray-600',
        clearIndicator: () => 'text-gray-400 hover:text-red-600',
        indicatorSeparator: () => 'bg-gray-200',
      }}
      {...props}
    />
  );
}