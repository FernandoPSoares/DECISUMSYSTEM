// File: frontend/src/features/maintenance/work_orders/components/WorkOrderTaskForm.jsx

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Spinner from '../../../../components/ui/Spinner';
import { createWorkOrderTask } from '../workOrdersApi';

const WorkOrderTaskForm = ({ workOrderId, onSuccess, onCancel }) => {
  const [description, setDescription] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description.trim()) return;

    setIsSaving(true);
    setError(null);

    try {
      await createWorkOrderTask(workOrderId, { description });
      onSuccess();
    } catch (err) {
      console.error("Erro ao criar tarefa:", err);
      setError("Erro ao adicionar tarefa.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Descrição da Tarefa</label>
        <input
          type="text"
          required
          autoFocus
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
          placeholder="Ex: Verificar nível de óleo..."
        />
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <div className="flex justify-end space-x-2 pt-2">
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
          Adicionar
        </button>
      </div>
    </form>
  );
};

WorkOrderTaskForm.propTypes = {
  workOrderId: PropTypes.string.isRequired,
  onSuccess: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};

export default WorkOrderTaskForm;