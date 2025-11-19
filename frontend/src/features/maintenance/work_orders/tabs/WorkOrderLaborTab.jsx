// File: frontend/src/features/maintenance/work_orders/tabs/WorkOrderLaborTab.jsx
import React, { useState } from 'react';
import { Clock, Trash2, Plus } from 'lucide-react';
import { deleteWorkOrderLaborLog } from '../workOrdersApi';

// Componentes
import Modal from '../../../../components/ui/Modal';
import WorkOrderLaborForm from '../components/WorkOrderLaborForm';

const WorkOrderLaborTab = ({ workOrder, onUpdate }) => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  
  const handleDelete = async (logId) => {
    if (!window.confirm("Tem a certeza que deseja remover este apontamento?")) return;
    
    try {
      await deleteWorkOrderLaborLog(workOrder.id, logId);
      onUpdate();
    } catch (error) {
      console.error("Erro ao eliminar apontamento:", error);
      alert("Erro ao eliminar apontamento.");
    }
  };

  const handleSuccessCreate = () => {
    setIsAddModalOpen(false);
    onUpdate();
  };

  // Calcular total de horas
  const totalHours = workOrder.labor_logs?.reduce((acc, log) => acc + (log.hours || 0), 0) || 0;

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium text-gray-900 flex items-center">
          <Clock className="w-5 h-5 mr-2 text-gray-500" />
          Apontamento de Horas
        </h3>
        <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-gray-600">Total: {totalHours}h</span>
            <button 
            onClick={() => setIsAddModalOpen(true)}
            className="text-sm bg-blue-50 text-blue-600 px-3 py-1 rounded hover:bg-blue-100 transition-colors flex items-center"
            >
            <Plus className="w-4 h-4 mr-1" />
            Registar Horas
            </button>
        </div>
      </div>

      {(!workOrder.labor_logs || workOrder.labor_logs.length === 0) ? (
        <p className="text-gray-500 text-sm italic text-center py-8 border border-dashed rounded bg-gray-50">
          Nenhum apontamento de mão de obra registado.
        </p>
      ) : (
        <div className="overflow-x-auto border rounded-lg">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Técnico</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Início</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Horas</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {workOrder.labor_logs.map(log => (
                <tr key={log.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">
                    {log.technician?.name || <span className="text-red-500 italic">Desconhecido</span>}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {new Date(log.start_time).toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900 font-bold">
                    {log.hours}h
                  </td>
                  <td className="px-4 py-3 text-right text-sm">
                    <button 
                        onClick={() => handleDelete(log.id)}
                        className="text-gray-400 hover:text-red-600 transition-colors"
                        title="Remover apontamento"
                    >
                        <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal para Registar Horas */}
      <Modal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        title="Registar Mão de Obra"
        maxWidth="md"
      >
        <WorkOrderLaborForm
          workOrderId={workOrder.id}
          onSuccess={handleSuccessCreate}
          onCancel={() => setIsAddModalOpen(false)}
        />
      </Modal>
    </div>
  );
};

export default WorkOrderLaborTab;