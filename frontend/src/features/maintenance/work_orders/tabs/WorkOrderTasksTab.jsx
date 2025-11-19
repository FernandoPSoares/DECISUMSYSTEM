// File: frontend/src/features/maintenance/work_orders/tabs/WorkOrderTasksTab.jsx
import React, { useState } from 'react';
import { CheckSquare, Trash2, Plus } from 'lucide-react';
import { updateWorkOrderTask, deleteWorkOrderTask } from '../workOrdersApi';

// Componentes
import Modal from '../../../../components/ui/Modal';
import WorkOrderTaskForm from '../components/WorkOrderTaskForm';

const WorkOrderTasksTab = ({ workOrder, onUpdate }) => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [processingTaskId, setProcessingTaskId] = useState(null); // Para loading individual

  // --- Handlers ---

  const handleToggleTask = async (task) => {
    setProcessingTaskId(task.id);
    try {
      await updateWorkOrderTask(workOrder.id, task.id, { completed: !task.completed });
      onUpdate(); // Recarrega a OS
    } catch (error) {
      console.error("Erro ao atualizar tarefa:", error);
    } finally {
      setProcessingTaskId(null);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm("Tem a certeza que deseja remover esta tarefa?")) return;
    
    setProcessingTaskId(taskId);
    try {
      await deleteWorkOrderTask(workOrder.id, taskId);
      onUpdate();
    } catch (error) {
      console.error("Erro ao eliminar tarefa:", error);
    } finally {
      setProcessingTaskId(null);
    }
  };

  const handleSuccessCreate = () => {
    setIsAddModalOpen(false);
    onUpdate();
  };

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium text-gray-900 flex items-center">
          <CheckSquare className="w-5 h-5 mr-2 text-gray-500" />
          Checklist de Tarefas
        </h3>
        <button 
          onClick={() => setIsAddModalOpen(true)}
          className="text-sm bg-blue-50 text-blue-600 px-3 py-1 rounded hover:bg-blue-100 transition-colors flex items-center"
        >
          <Plus className="w-4 h-4 mr-1" />
          Adicionar Tarefa
        </button>
      </div>
      
      {(!workOrder.tasks || workOrder.tasks.length === 0) ? (
        <p className="text-gray-500 text-sm italic text-center py-4 border border-dashed rounded">
          Nenhuma tarefa definida para esta OS.
        </p>
      ) : (
        <ul className="space-y-2">
          {workOrder.tasks.map(task => (
            <li 
              key={task.id} 
              className={`flex justify-between items-center p-3 rounded border transition-colors ${
                task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200 hover:border-blue-300'
              }`}
            >
              <div className="flex items-center flex-1">
                <input 
                  type="checkbox" 
                  checked={task.completed}
                  onChange={() => handleToggleTask(task)}
                  disabled={processingTaskId === task.id}
                  className="h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500 cursor-pointer disabled:opacity-50"
                />
                <span className={`ml-3 text-sm ${task.completed ? 'text-gray-500 line-through' : 'text-gray-800 font-medium'}`}>
                  {task.description}
                </span>
              </div>
              
              <button 
                onClick={() => handleDeleteTask(task.id)}
                disabled={processingTaskId === task.id}
                className="text-gray-400 hover:text-red-600 p-1 ml-2"
                title="Remover tarefa"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* Modal para Adicionar Tarefa */}
      <Modal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        title="Nova Tarefa"
        maxWidth="md"
      >
        <WorkOrderTaskForm
          workOrderId={workOrder.id}
          onSuccess={handleSuccessCreate}
          onCancel={() => setIsAddModalOpen(false)}
        />
      </Modal>
    </div>
  );
};

export default WorkOrderTasksTab;