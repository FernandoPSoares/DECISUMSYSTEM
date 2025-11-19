// File: frontend/src/features/maintenance/work_orders/components/WorkOrderForm.jsx

import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { X, Save } from 'lucide-react';
import apiClient from '../../../../api/apiClient';
import { createWorkOrder, updateWorkOrder } from '../workOrdersApi';
import SearchableSelect from '../../../../components/ui/SearchableSelect';
import Spinner from '../../../../components/ui/Spinner';

/**
 * Formulário para Criar ou Editar uma Ordem de Serviço (OS).
 * * Carrega dados auxiliares (Ativos, Técnicos, Equipes) para preencher
 * os campos de seleção.
 */
const WorkOrderForm = ({ workOrderToEdit, onSuccess, onCancel }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  // Dados para os dropdowns
  const [assets, setAssets] = useState([]);
  const [technicians, setTechnicians] = useState([]);
  const [teams, setTeams] = useState([]);

  // Estado do Formulário
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    wo_type: 'CORRECTIVE',
    priority: 'MEDIUM',
    status: 'OPEN', // Apenas relevante na edição
    asset_id: null,
    assigned_to_technician_id: null,
    assigned_to_team_id: null,
    due_date: ''
  });

  // --- 1. Carregar Dados Auxiliares ---
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        // Carregar em paralelo: Ativos, Técnicos e Equipes
        const [assetsRes, techsRes, teamsRes] = await Promise.all([
          apiClient.get('/maintenance/assets?limit=500'), // Limite alto para o dropdown
          apiClient.get('/maintenance/technicians'),
          apiClient.get('/maintenance/teams')
        ]);
        
        setAssets(assetsRes.data || []);
        setTechnicians(techsRes.data || []);
        setTeams(teamsRes.data || []);

        // Se estiver em modo de edição, preencher o formulário
        if (workOrderToEdit) {
          setFormData({
            title: workOrderToEdit.title || '',
            description: workOrderToEdit.description || '',
            wo_type: workOrderToEdit.wo_type || 'CORRECTIVE',
            priority: workOrderToEdit.priority || 'MEDIUM',
            status: workOrderToEdit.status || 'OPEN',
            asset_id: workOrderToEdit.asset?.id || workOrderToEdit.asset_id || null,
            assigned_to_technician_id: workOrderToEdit.assigned_to_technician?.id || workOrderToEdit.assigned_to_technician_id || null,
            assigned_to_team_id: workOrderToEdit.assigned_to_team?.id || workOrderToEdit.assigned_to_team_id || null,
            // Formatar data para o input (YYYY-MM-DDTHH:mm ou YYYY-MM-DD)
            due_date: workOrderToEdit.due_date ? workOrderToEdit.due_date.split('T')[0] : ''
          });
        }
      } catch (err) {
        console.error("Erro ao carregar dados:", err);
        setError("Falha ao carregar listas de ativos ou responsáveis.");
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [workOrderToEdit]);

  // --- 2. Handlers ---

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (field, value) => {
    // Extrai apenas o ID (value) do objeto retornado pelo SearchableSelect
    setFormData(prev => ({ ...prev, [field]: value ? value.value : null }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    
    if (!formData.asset_id) {
      setError("É obrigatório selecionar um Ativo.");
      return;
    }

    setIsSaving(true);

    try {
      // Preparar payload
      const payload = {
        ...formData,
        description: formData.description || null,
        due_date: formData.due_date || null,
        // Enviar null se a string estiver vazia ou undefined
        assigned_to_technician_id: formData.assigned_to_technician_id || null,
        assigned_to_team_id: formData.assigned_to_team_id || null,
      };

      if (workOrderToEdit) {
        // Ao editar, enviamos o payload completo, incluindo o status
        await updateWorkOrder(workOrderToEdit.id, payload); 
      } else {
        // Ao criar, o status não é enviado, pois o backend define o padrão.
        // O campo 'status' já não está no payload inicial.
        await createWorkOrder(payload);
      }
      
      onSuccess();
    } catch (err) {
      console.error("Erro ao salvar OS:", err);
      const msg = err.response?.data?.detail || "Erro ao salvar a Ordem de Serviço.";
      setError(msg);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <div className="p-6 flex justify-center"><Spinner /></div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-lg flex flex-col max-h-[90vh]">
      {/* Header */}
      <div className="flex justify-between items-center p-4 border-b">
        <h3 className="text-lg font-semibold text-gray-800">
          {workOrderToEdit ? `Editar OS: ${workOrderToEdit.wo_number}` : 'Nova Ordem de Serviço'}
        </h3>
        <button onClick={onCancel} className="text-gray-500 hover:text-gray-700">
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Body */}
      <div className="p-6 overflow-y-auto">
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded text-sm">
            {error}
          </div>
        )}

        <form id="wo-form" onSubmit={handleSubmit} className="space-y-4">
          
          {/* Título e Tipo */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Título da OS *</label>
              <input
                type="text"
                name="title"
                required
                value={formData.title}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Ex: Troca de Correia do Motor"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
              <select
                name="wo_type"
                value={formData.wo_type}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none bg-white"
              >
                <option value="CORRECTIVE">Corretiva</option>
                <option value="PREVENTIVE">Preventiva</option>
                <option value="PREDICTIVE">Preditiva</option>
                <option value="IMPROVEMENT">Melhoria</option>
                <option value="SAFETY">Segurança</option>
              </select>
            </div>
          </div>

          {/* Ativo e Prioridade */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Ativo (Equipamento) *</label>
              <SearchableSelect
                options={assets.map(a => ({ value: a.id, label: `${a.name} (${a.internal_tag})` }))}
                value={assets.map(a => ({ value: a.id, label: `${a.name} (${a.internal_tag})` })).find(a => a.value === formData.asset_id)}
                onChange={(val) => handleSelectChange('asset_id', val)}
                placeholder="Selecione o ativo..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Prioridade *</label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none bg-white"
              >
                <option value="LOW">Baixa</option>
                <option value="MEDIUM">Média</option>
                <option value="HIGH">Alta</option>
                <option value="URGENT">Urgente</option>
              </select>
            </div>
          </div>

          {/* Atribuição (Técnico e Equipe) */}
          <div className="p-4 bg-gray-50 rounded border border-gray-100">
            <h4 className="text-sm font-semibold text-gray-600 mb-3">Atribuição (Responsáveis)</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Técnico Responsável</label>
                <SearchableSelect
                  options={technicians.map(t => ({ value: t.id, label: t.name }))}
                  value={technicians.map(t => ({ value: t.id, label: t.name })).find(t => t.value === formData.assigned_to_technician_id)}
                  onChange={(val) => handleSelectChange('assigned_to_technician_id', val)}
                  placeholder="Selecione um técnico..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Equipe Responsável</label>
                <SearchableSelect
                  options={teams.map(t => ({ value: t.id, label: t.name }))}
                  value={teams.map(t => ({ value: t.id, label: t.name })).find(t => t.value === formData.assigned_to_team_id)}
                  onChange={(val) => handleSelectChange('assigned_to_team_id', val)}
                  placeholder="Selecione uma equipe..."
                />
              </div>
            </div>
          </div>

          {/* Data Limite e Status (Status só aparece na edição) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Data Limite (Due Date)</label>
              <input
                type="date"
                name="due_date"
                value={formData.due_date}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            
            {workOrderToEdit && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status Atual</label>
                <select
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none bg-white"
                >
                   <option value="DRAFT">Rascunho</option>
                   <option value="OPEN">Aberta</option>
                   <option value="IN_PROGRESS">Em Andamento</option>
                   <option value="ON_HOLD">Em Espera</option>
                   <option value="COMPLETED">Concluída</option>
                   <option value="CANCELLED">Cancelada</option>
                </select>
              </div>
            )}
          </div>

          {/* Descrição */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Descrição do Problema/Serviço</label>
            <textarea
              name="description"
              rows="4"
              value={formData.description}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="Descreva detalhadamente o que precisa ser feito..."
            />
          </div>

        </form>
      </div>

      {/* Footer */}
      <div className="p-4 border-t bg-gray-50 flex justify-end space-x-3 rounded-b-lg">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none"
        >
          Cancelar
        </button>
        <button
          type="submit"
          form="wo-form"
          disabled={isSaving}
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none flex items-center"
        >
          {isSaving && <Spinner size="sm" className="mr-2 text-white" />}
          {isSaving ? 'Salvando...' : 'Salvar Ordem de Serviço'}
        </button>
      </div>
    </div>
  );
};

WorkOrderForm.propTypes = {
  workOrderToEdit: PropTypes.object,
  onSuccess: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};

export default WorkOrderForm;