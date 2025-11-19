// File: frontend/src/features/maintenance/work_orders/WorkOrderDetailPage.jsx

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Calendar, User, Briefcase, AlertCircle } from 'lucide-react';
import { getWorkOrder } from './workOrdersApi';

// Componentes UI
import Spinner from '../../../components/ui/Spinner';
import Tabs from '../../../components/ui/Tabs';

// Abas (Sub-componentes)
import WorkOrderTasksTab from './tabs/WorkOrderTasksTab';
import WorkOrderLaborTab from './tabs/WorkOrderLaborTab';
import WorkOrderPartsTab from './tabs/WorkOrderPartsTab';
import WorkOrderLogsTab from './tabs/WorkOrderLogsTab';

const WorkOrderDetailPage = () => {
  const { id } = useParams(); // Obtém o ID da URL
  const navigate = useNavigate();
  
  const [workOrder, setWorkOrder] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- Carregar Dados ---
  const fetchWorkOrderDetails = async () => {
    setIsLoading(true);
    try {
      const data = await getWorkOrder(id);
      setWorkOrder(data);
    } catch (err) {
      console.error("Erro ao carregar detalhes da OS:", err);
      setError("Não foi possível carregar a Ordem de Serviço.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (id) {
      fetchWorkOrderDetails();
    }
  }, [id]);

  // --- Helpers de Renderização ---
  const getStatusColor = (status) => {
    const colors = {
      DRAFT: 'bg-gray-100 text-gray-800',
      OPEN: 'bg-blue-100 text-blue-800',
      IN_PROGRESS: 'bg-yellow-100 text-yellow-800',
      COMPLETED: 'bg-green-100 text-green-800',
      CANCELLED: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  // Definição das Abas
  const tabs = [
    {
      id: 'tasks',
      label: 'Tarefas',
      content: <WorkOrderTasksTab workOrder={workOrder} onUpdate={fetchWorkOrderDetails} />
    },
    {
      id: 'labor',
      label: 'Mão de Obra',
      content: <WorkOrderLaborTab workOrder={workOrder} onUpdate={fetchWorkOrderDetails} />
    },
    {
      id: 'parts',
      label: 'Peças',
      content: <WorkOrderPartsTab workOrder={workOrder} onUpdate={fetchWorkOrderDetails} />
    },
    {
      id: 'logs',
      label: 'Histórico',
      content: <WorkOrderLogsTab workOrder={workOrder} onUpdate={fetchWorkOrderDetails} />
    }
  ];

  if (isLoading) return <div className="h-full flex items-center justify-center"><Spinner /></div>;
  if (error) return <div className="p-8 text-center text-red-600">{error}</div>;
  if (!workOrder) return null;

  return (
    <div className="container mx-auto pb-10">
      {/* Botão Voltar */}
      <button 
        onClick={() => navigate('/maintenance/work-orders')}
        className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition-colors"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Voltar à Lista
      </button>

      {/* Cabeçalho Principal */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
                <h1 className="text-2xl font-bold text-gray-900">{workOrder.wo_number}</h1>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(workOrder.status)}`}>
                    {workOrder.status}
                </span>
            </div>
            <h2 className="text-lg text-gray-700 font-medium">{workOrder.title}</h2>
          </div>
          
          {/* Ações Principais (Ex: Editar, Imprimir) */}
          <div className="flex gap-2 mt-4 md:mt-0">
             {/* (Botões de ação virão aqui futuramente) */}
          </div>
        </div>

        {/* Informações Rápidas (Grid) */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 pt-4 border-t border-gray-100 text-sm">
            <div>
                <span className="block text-gray-500 mb-1">Ativo</span>
                <div className="font-medium text-gray-900 flex items-center">
                    <Briefcase className="w-4 h-4 mr-2 text-gray-400" />
                    {workOrder.asset?.name} 
                    <span className="text-gray-400 ml-1 text-xs">({workOrder.asset?.internal_tag})</span>
                </div>
            </div>
            <div>
                <span className="block text-gray-500 mb-1">Prioridade</span>
                <div className="font-medium text-gray-900 flex items-center">
                    <AlertCircle className="w-4 h-4 mr-2 text-gray-400" />
                    {workOrder.priority}
                </div>
            </div>
            <div>
                <span className="block text-gray-500 mb-1">Responsável</span>
                <div className="font-medium text-gray-900 flex items-center">
                    <User className="w-4 h-4 mr-2 text-gray-400" />
                    {workOrder.assigned_to_technician?.name || workOrder.assigned_to_team?.name || 'Não atribuído'}
                </div>
            </div>
            <div>
                <span className="block text-gray-500 mb-1">Data Limite</span>
                <div className="font-medium text-gray-900 flex items-center">
                    <Calendar className="w-4 h-4 mr-2 text-gray-400" />
                    {workOrder.due_date ? new Date(workOrder.due_date).toLocaleDateString() : '-'}
                </div>
            </div>
        </div>
        
        {/* Descrição Completa */}
        {workOrder.description && (
            <div className="mt-4 pt-4 border-t border-gray-100">
                <span className="block text-gray-500 text-xs uppercase font-bold mb-1">Descrição</span>
                <p className="text-gray-700 bg-gray-50 p-3 rounded-md">{workOrder.description}</p>
            </div>
        )}
      </div>

      {/* Área de Conteúdo (Abas) */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <Tabs tabs={tabs} />
      </div>
    </div>
  );
};

export default WorkOrderDetailPage;