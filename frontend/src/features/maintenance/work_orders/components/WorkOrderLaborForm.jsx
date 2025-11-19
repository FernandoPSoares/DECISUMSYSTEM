// File: frontend/src/features/maintenance/work_orders/components/WorkOrderLaborForm.jsx

import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import apiClient from '../../../../api/apiClient';
import { createWorkOrderLaborLog } from '../workOrdersApi';
import Spinner from '../../../../components/ui/Spinner';
import SearchableSelect from '../../../../components/ui/SearchableSelect';

const WorkOrderLaborForm = ({ workOrderId, onSuccess, onCancel }) => {
  const [technicians, setTechnicians] = useState([]);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  // Estado do formulário
  const [formData, setFormData] = useState({
    technician_id: null,
    start_time: '', // datetime-local string
    hours: ''
  });

  // Carregar técnicos ao montar
  useEffect(() => {
    const loadTechnicians = async () => {
      setIsLoadingData(true);
      try {
        const res = await apiClient.get('/maintenance/technicians');
        setTechnicians(res.data || []);
      } catch (err) {
        console.error("Erro ao carregar técnicos:", err);
        setError("Não foi possível carregar a lista de técnicos.");
      } finally {
        setIsLoadingData(false);
      }
    };
    loadTechnicians();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.technician_id || !formData.start_time || !formData.hours) {
        setError("Preencha todos os campos obrigatórios.");
        return;
    }

    setIsSaving(true);
    setError(null);

    try {
      // Converter data para ISO se necessário, mas o backend aceita ISO strings
      await createWorkOrderLaborLog(workOrderId, {
        technician_id: formData.technician_id,
        start_time: new Date(formData.start_time).toISOString(),
        hours: parseFloat(formData.hours)
      });
      onSuccess();
    } catch (err) {
      console.error("Erro ao registar horas:", err);
      setError(err.response?.data?.detail || "Erro ao registar apontamento.");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoadingData) return <div className="p-4 flex justify-center"><Spinner /></div>;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Seleção de Técnico */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Técnico *</label>
        <SearchableSelect
            options={technicians.map(t => ({ value: t.id, label: t.name }))}
            // CORREÇÃO: Encontra o objeto completo para exibir o label
            value={technicians.map(t => ({ value: t.id, label: t.name })).find(t => t.value === formData.technician_id)}
            onChange={(val) => setFormData(prev => ({ ...prev, technician_id: val ? val.value : null }))}
            placeholder="Selecione o técnico..."
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Data/Hora Início */}
        <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Início do Trabalho *</label>
            <input
            type="datetime-local"
            required
            value={formData.start_time}
            onChange={(e) => setFormData(prev => ({ ...prev, start_time: e.target.value }))}
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
            />
        </div>

        {/* Quantidade de Horas */}
        <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Horas Trabalhadas *</label>
            <input
            type="number"
            step="0.5"
            min="0.1"
            required
            value={formData.hours}
            onChange={(e) => setFormData(prev => ({ ...prev, hours: e.target.value }))}
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
            placeholder="Ex: 1.5"
            />
        </div>
      </div>

      {error && <p className="text-sm text-red-600 bg-red-50 p-2 rounded">{error}</p>}

      <div className="flex justify-end space-x-2 pt-4 border-t">
        <button
          type="button"
          onClick={onCancel}
          className="px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded"
          disabled={isSaving}
        >
          Cancelar
        </button>
        <button
          type="submit"
          className="px-3 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded flex items-center"
          disabled={isSaving}
        >
          {isSaving && <Spinner size="sm" className="mr-2" />}
          Registar
        </button>
      </div>
    </form>
  );
};

WorkOrderLaborForm.propTypes = {
  workOrderId: PropTypes.string.isRequired,
  onSuccess: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};

export default WorkOrderLaborForm;