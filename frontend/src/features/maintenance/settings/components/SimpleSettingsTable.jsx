// File: frontend/src/features/maintenance/settings/components/SimpleSettingsTable.jsx

import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Plus, Search, Edit2, Trash2, AlertCircle } from 'lucide-react';
import useDebounce from '../../../../hooks/useDebounce';

// Componentes UI Partilhados
import DataTable from '../../../../components/ui/table/DataTable';
import Modal from '../../../../components/ui/Modal';
import ConfirmationModal from '../../../../components/ui/ConfirmationModal';
import Spinner from '../../../../components/ui/Spinner';

/**
 * Utilitário para formatar telefone (Brasil).
 * Suporta (XX) XXXX-XXXX e (XX) XXXXX-XXXX.
 */
const formatPhoneNumber = (value) => {
  if (!value) return "";
  
  // Remove tudo o que não é dígito
  const v = value.replace(/\D/g, "");
  const limit = v.slice(0, 11); // Limita a 11 números

  // Aplica a máscara progressivamente
  if (limit.length <= 10) {
    // Formato Fixo: (XX) XXXX-XXXX
    return limit
      .replace(/(\d{2})(\d)/, "($1) $2")
      .replace(/(\d{4})(\d)/, "$1-$2");
  } else {
    // Formato Celular: (XX) XXXXX-XXXX
    return limit
      .replace(/(\d{2})(\d)/, "($1) $2")
      .replace(/(\d{5})(\d)/, "$1-$2");
  }
};

const SimpleSettingsTable = ({ 
  title, 
  api, 
  columns, 
  formFields = [{ name: 'name', label: 'Nome', type: 'text', required: true }] 
}) => {
  // --- Estados ---
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Modal Criar/Editar
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState({});
  const [formError, setFormError] = useState(null);

  // Modal Eliminar
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState(null);

  const debouncedSearch = useDebounce(searchTerm, 500);

  // --- Fetch Data ---
  const fetchData = async () => {
    setIsLoading(true);
    try {
      const params = {};
      if (debouncedSearch) params.search = debouncedSearch;
      const result = await api.list(params);
      setData(result);
    } catch (error) {
      console.error(`Erro ao carregar ${title}:`, error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [debouncedSearch, api]);

  // --- Helpers de Formulário ---

  const preparePayload = (data) => {
    const payload = { ...data };
    Object.keys(payload).forEach(key => {
      const value = payload[key];
      if (typeof value === 'string') {
        const trimmed = value.trim();
        payload[key] = trimmed === '' ? null : trimmed;
      }
    });
    return payload;
  };

  const handleOpenCreate = () => {
    setEditingItem(null);
    setFormData({});
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (item) => {
    setEditingItem(item);
    const safeData = { ...item };
    Object.keys(safeData).forEach(key => {
      if (safeData[key] === null) safeData[key] = '';
    });
    setFormData(safeData);
    setFormError(null);
    setIsModalOpen(true);
  };

  // --- CORREÇÃO: handleInputChange "inteligente" ---
  const handleInputChange = (e, fieldConfig) => {
    const { name, value, type, checked } = e.target;
    let newValue = type === 'checkbox' ? checked : value;

    // Aplica máscara de telefone se o tipo do campo for 'tel'
    if (fieldConfig.type === 'tel') {
      newValue = formatPhoneNumber(newValue);
    }

    setFormData(prev => ({
      ...prev,
      [name]: newValue
    }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setFormError(null);

    try {
      const payload = preparePayload(formData);
      if (editingItem) {
        await api.update(editingItem.id, payload);
      } else {
        await api.create(payload);
      }
      await fetchData();
      setIsModalOpen(false);
    } catch (err) {
      console.error("Erro ao guardar:", err);
      const msg = err.response?.data?.detail || "Erro ao processar o pedido.";
      if (Array.isArray(msg)) {
         setFormError(`Erro no campo: ${msg[0]?.loc?.[1]} - ${msg[0]?.msg}`);
      } else {
         setFormError(msg);
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleOpenDelete = (item) => {
    setItemToDelete(item);
    setIsDeleteModalOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!itemToDelete) return;
    try {
      await api.remove(itemToDelete.id);
      await fetchData();
      setIsDeleteModalOpen(false);
      setItemToDelete(null);
    } catch (err) {
      console.error("Erro ao eliminar:", err);
      alert("Não foi possível eliminar o registo.");
    }
  };

  const tableColumns = [
    ...columns,
    {
      header: 'Ações',
      accessor: 'actions',
      cell: (row) => (
        <div className="flex justify-end space-x-2">
          <button 
            onClick={(e) => { e.stopPropagation(); handleOpenEdit(row); }}
            className="text-blue-600 hover:text-blue-800 p-1"
            title="Editar"
          >
            <Edit2 className="w-4 h-4" />
          </button>
          <button 
            onClick={(e) => { e.stopPropagation(); handleOpenDelete(row); }}
            className="text-red-600 hover:text-red-800 p-1"
            title="Eliminar"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      )
    }
  ];

  return (
    <div className="space-y-4">
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-lg font-bold text-gray-800">{title}</h2>
        
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative flex-grow md:flex-grow-0">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Pesquisar..."
              className="pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none w-full"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button
            onClick={handleOpenCreate}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm shadow-sm whitespace-nowrap"
          >
            <Plus className="w-4 h-4" />
            Adicionar
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 min-h-[300px]">
        <DataTable
          columns={tableColumns}
          data={data}
          isLoading={isLoading}
          emptyMessage="Nenhum registo encontrado."
        />
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingItem ? `Editar ${title.slice(0, -1)}` : `Novo ${title.slice(0, -1)}`}
        maxWidth="md"
      >
        <form onSubmit={handleSave} className="p-6 space-y-4">
          {formError && (
            <div className="p-3 bg-red-50 text-red-700 rounded-md text-sm border border-red-200 flex items-start gap-2">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <span>{formError}</span>
            </div>
          )}

          {formFields.map((field) => (
            <div key={field.name}>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {field.label} {field.required && <span className="text-red-500">*</span>}
              </label>
              
              {field.type === 'textarea' ? (
                <textarea
                  name={field.name}
                  required={field.required}
                  rows={3}
                  value={formData[field.name] || ''}
                  onChange={(e) => handleInputChange(e, field)}
                  className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                />
              ) : (
                <input
                  type={field.type || 'text'} // Pode ser 'text', 'email', 'tel', etc.
                  name={field.name}
                  required={field.required}
                  value={formData[field.name] || ''}
                  // Passamos o objeto 'field' inteiro para saber se type='tel'
                  onChange={(e) => handleInputChange(e, field)}
                  maxLength={field.type === 'tel' ? 15 : undefined} // Limite de segurança para a máscara
                  className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none"
                />
              )}
              {field.hint && <p className="text-xs text-gray-400 mt-1">{field.hint}</p>}
            </div>
          ))}

          <div className="flex justify-end gap-3 pt-4 border-t border-gray-100 mt-6">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              disabled={isSaving}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 flex items-center"
              disabled={isSaving}
            >
              {isSaving && <Spinner size="sm" className="mr-2 text-white" />}
              {isSaving ? 'A guardar...' : 'Guardar'}
            </button>
          </div>
        </form>
      </Modal>

      <ConfirmationModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={handleConfirmDelete}
        title="Eliminar Registo"
        message="Tem a certeza que deseja eliminar este registo?"
        confirmText="Eliminar"
        variant="danger"
      />
    </div>
  );
};

SimpleSettingsTable.propTypes = {
  title: PropTypes.string.isRequired,
  api: PropTypes.object.isRequired,
  columns: PropTypes.array.isRequired,
  formFields: PropTypes.array
};

export default SimpleSettingsTable;