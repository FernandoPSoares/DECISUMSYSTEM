// File: frontend/src/components/ui/Tabs.jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const Tabs = ({ tabs, defaultTabId, variant = 'default' }) => {
  // Se não houver abas, não renderiza nada
  if (!tabs || tabs.length === 0) return null;

  // Estado da aba ativa
  const [activeTab, setActiveTab] = useState(defaultTabId || tabs[0].id);

  // Garante que se a lista de abas mudar, a ativa se mantém válida
  useEffect(() => {
    if (tabs.length > 0 && !tabs.find(t => t.id === activeTab)) {
      setActiveTab(tabs[0].id);
    }
  }, [tabs, activeTab]);

  // Estilos baseados na variante
  const getTabClasses = (isActive) => {
    if (variant === 'underline') {
      return `px-4 py-2 text-sm font-medium border-b-2 transition-colors duration-200 ${
        isActive
          ? 'border-blue-600 text-blue-600'
          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
      }`;
    }
    // Default (Pills/Cards style)
    return `px-4 py-2 text-sm font-medium rounded-t-lg border-b-2 border-transparent transition-colors duration-200 ${
      isActive
        ? 'bg-white text-blue-700 border-blue-500 shadow-sm' // Ativo
        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50' // Inativo
    }`;
  };

  return (
    <div className="flex flex-col h-full">
      {/* Cabeçalho das Abas */}
      <div className={`flex space-x-1 border-b border-gray-200 ${variant === 'default' ? 'bg-gray-100 p-1 rounded-t-lg' : ''}`}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={getTabClasses(activeTab === tab.id)}
            type="button"
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Conteúdo da Aba Ativa */}
      <div className="flex-1 p-4 bg-white rounded-b-lg shadow-sm border-t-0 border-gray-200">
        {tabs.map((tab) => {
          if (tab.id !== activeTab) return null;
          return (
            <div key={tab.id} className="animate-fadeIn">
              {tab.content}
            </div>
          );
        })}
      </div>
    </div>
  );
};

Tabs.propTypes = {
  tabs: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      label: PropTypes.node.isRequired, // node permite string ou JSX (ícones)
      content: PropTypes.node.isRequired,
    })
  ).isRequired,
  defaultTabId: PropTypes.string,
  variant: PropTypes.oneOf(['default', 'underline'])
};

export default Tabs;