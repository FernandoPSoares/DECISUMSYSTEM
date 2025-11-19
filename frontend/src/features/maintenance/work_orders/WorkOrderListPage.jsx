// File: frontend/src/features/maintenance/work_orders/WorkOrderListPage.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Edit2, Trash2, Eye } from 'lucide-react';
import { getWorkOrders, deleteWorkOrder } from './workOrdersApi';

// Componentes UI
import DataTable from '../../../components/ui/table/DataTable';
import Modal from '../../../components/ui/Modal';
import ConfirmationModal from '../../../components/ui/ConfirmationModal';
import WorkOrderForm from './components/WorkOrderForm';
import useDebounce from '../../../hooks/useDebounce';

/**
 * Página de Listagem de Ordens de Serviço.
 * Permite listar, filtrar, criar e navegar para os detalhes das OSs.
 */
const WorkOrderListPage = () => {
  const navigate = useNavigate();

  // --- Estados ---
  const [workOrders, setWorkOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Estados para Modais
  const [isFormModalOpen, setIsFormModalOpen] = useState(false);
  const [selectedWorkOrder, setSelectedWorkOrder] = useState(null);
  
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [woToDelete, setWoToDelete] = useState(null);

  const debouncedSearch = useDebounce(searchTerm, 500);

  // --- Carregamento de Dados ---
  const fetchWorkOrders = async () => {
    setIsLoading(true);
    try {
      const params = {};
      if (debouncedSearch) params.search = debouncedSearch;
      
      // Ordenar por padrão pelas mais recentes
      params.sort_by = 'created_at';
      params.sort_order = 'desc';

      const data = await getWorkOrders(params);
      setWorkOrders(data);
    } catch (error) {
      console.error("Erro ao carregar OSs:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkOrders();
  }, [debouncedSearch]);

  // --- Handlers ---

  const handleCreate = () => {
    setSelectedWorkOrder(null);
    setIsFormModalOpen(true);
  };

  const handleEdit = (wo) => {
    setSelectedWorkOrder(wo);
    setIsFormModalOpen(true);
  };

  // Navega para a página de detalhes (Fase 3.4)
  const handleViewDetails = (wo) => {
    navigate(`/maintenance/work-orders/${wo.id}`);
  };

  const handleDeleteClick = (wo) => {
    setWoToDelete(wo);
    setIsDeleteModalOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!woToDelete) return;
    try {
      await deleteWorkOrder(woToDelete.id);
      await fetchWorkOrders();
      setIsDeleteModalOpen(false);
      setWoToDelete(null);
    } catch (error) {
      console.error("Erro ao eliminar OS:", error);
      const msg = error.response?.data?.detail || "Não foi possível eliminar a OS.";
      alert(msg);
    }
  };

  const handleFormSuccess = async () => {
    await fetchWorkOrders();
    setIsFormModalOpen(false);
    setSelectedWorkOrder(null);
  };

  // --- Renderização de Colunas ---
  
  const renderPriorityBadge = (priority) => {
    const styles = {
      LOW: 'bg-gray-100 text-gray-700',
      MEDIUM: 'bg-blue-100 text-blue-700',
      HIGH: 'bg-orange-100 text-orange-700',
      URGENT: 'bg-red-100 text-red-700 font-bold',
    };
    const labels = { LOW: 'Baixa', MEDIUM: 'Média', HIGH: 'Alta', URGENT: 'Urgente' };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs ${styles[priority] || 'bg-gray-100'}`}>
        {labels[priority] || priority}
      </span>
    );
  };

  const renderStatusBadge = (status) => {
    const styles = {
      DRAFT: 'bg-gray-200 text-gray-700 border border-gray-300',
      OPEN: 'bg-blue-100 text-blue-700',
      IN_PROGRESS: 'bg-yellow-100 text-yellow-800',
      ON_HOLD: 'bg-orange-50 text-orange-600',
      COMPLETED: 'bg-green-100 text-green-800',
      CANCELLED: 'bg-red-50 text-red-600 strike-through',
    };
    const labels = {
      DRAFT: 'Rascunho', OPEN: 'Aberta', IN_PROGRESS: 'Em Andamento',
      ON_HOLD: 'Em Espera', COMPLETED: 'Concluída', CANCELLED: 'Cancelada'
    };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${styles[status] || 'bg-gray-100'}`}>
        {labels[status] || status}
      </span>
    );
  };

  const columns = [
    { 
      header: 'Nº OS', 
      accessor: 'wo_number',
      render: (row) => (
        <button 
          onClick={() => handleViewDetails(row)}
          className="font-bold text-blue-600 hover:text-blue-800 hover:underline"
        >
          {row.wo_number}
        </button>
      )
    },
    { 
      header: 'Título', 
      accessor: 'title',
      render: (row) => (
        <div className="max-w-xs truncate" title={row.title}>
          <div className="font-medium text-gray-900">{row.title}</div>
          <div className="text-xs text-gray-500">{row.wo_type}</div>
        </div>
      )
    },
    { 
      header: 'Prioridade', 
      accessor: 'priority',
      render: (row) => renderPriorityBadge(row.priority)
    },
    { 
        header: 'Status', 
        accessor: 'status',
        render: (row) => renderStatusBadge(row.status)
    },
    { 
        header: 'Ativo', 
        accessor: 'asset.name',
        render: (row) => (
            <div className="text-sm">
                <div className="font-medium">{row.asset?.name}</div>
                <div className="text-xs text-gray-400">{row.asset?.internal_tag}</div>
            </div>
        )
    },
    { 
        header: 'Responsável', 
        accessor: 'assigned_to',
        render: (row) => {
            if (row.assigned_to_technician) return row.assigned_to_technician.name;
            if (row.assigned_to_team) return `Equipa: ${row.assigned_to_team.name}`;
            return <span className="text-gray-400 italic">- Não Atribuído -</span>;
        }
    },
    {
      header: 'Ações',
      accessor: 'actions',
      render: (row) => (
        <div className="flex space-x-2">
          <button 
            onClick={() => handleViewDetails(row)}
            className="text-gray-600 hover:text-blue-600 p-1"
            title="Ver Detalhes"
          >
            <Eye className="w-4 h-4" />
          </button>
          <button 
            onClick={() => handleEdit(row)}
            className="text-blue-600 hover:text-blue-800 p-1"
            title="Editar (Alterar Status/Atribuição)"
          >
            <Edit2 className="w-4 h-4" />
          </button>
          
          {/* Apenas permite eliminar Rascunhos (Regra de Negócio do Frontend) */}
          {row.status === 'DRAFT' && (
            <button 
                onClick={() => handleDeleteClick(row)}
                className="text-red-600 hover:text-red-800 p-1"
                title="Eliminar"
            >
                <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      )
    }
  ];

  return (
    <div className="container mx-auto">
      {/* Cabeçalho */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Ordens de Serviço</h1>
          <p className="text-sm text-gray-600">Gestão de manutenção corretiva e preventiva</p>
        </div>
        <button
          onClick={handleCreate}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 shadow-sm transition-colors"
        >
          <Plus className="w-4 h-4" />
          Nova OS
        </button>
      </div>

      {/* Filtros */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Pesquisar por Nº OS, Título, Ativo..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Tabela */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
        <DataTable
          columns={columns}
          data={workOrders}
          isLoading={isLoading}
          emptyMessage="Nenhuma Ordem de Serviço encontrada."
        />
      </div>

      {/* Modal Formulário */}
      <Modal
        isOpen={isFormModalOpen}
        onClose={() => setIsFormModalOpen(false)}
        title={selectedWorkOrder ? `Editar OS: ${selectedWorkOrder.wo_number}` : "Nova Ordem de Serviço"}
        maxWidth="2xl"
      >
        <WorkOrderForm
          workOrderToEdit={selectedWorkOrder}
          onSuccess={handleFormSuccess}
          onCancel={() => setIsFormModalOpen(false)}
        />
      </Modal>

      {/* Modal Eliminação */}
      <ConfirmationModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={handleConfirmDelete}
        title="Eliminar Ordem de Serviço"
        message={`Tem a certeza que deseja eliminar a OS "${woToDelete?.wo_number}"? Apenas rascunhos podem ser eliminados permanentemente.`}
        confirmText="Eliminar"
        variant="danger"
      />
    </div>
  );
};

export default WorkOrderListPage;