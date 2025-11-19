// File: frontend/src/features/maintenance/assets/AssetManagementPage.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Edit2, Trash2, Eye } from 'lucide-react';
import { getAssets, deleteAsset } from './assetsApi';

// Componentes UI
import DataTable from '../../../components/ui/table/DataTable';
import Modal from '../../../components/ui/Modal';
import ConfirmationModal from '../../../components/ui/ConfirmationModal';
import AssetForm from './components/AssetForm';
import useDebounce from '../../../hooks/useDebounce';

const AssetManagementPage = () => {
  const navigate = useNavigate();

  // --- Estados ---
  const [assets, setAssets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Modais
  const [isFormModalOpen, setIsFormModalOpen] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState(null);
  
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [assetToDelete, setAssetToDelete] = useState(null);

  const debouncedSearch = useDebounce(searchTerm, 500);

  // --- Carregamento ---
  const fetchAssets = async () => {
    setIsLoading(true);
    try {
      const params = {};
      if (debouncedSearch) params.search = debouncedSearch;
      const data = await getAssets(params);
      setAssets(data);
    } catch (error) {
      console.error("Erro ao carregar ativos:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAssets();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedSearch]);

  // --- Ações ---
  
  const handleViewDetails = (asset) => {
    navigate(`/maintenance/assets/${asset.id}`);
  };

  const handleCreate = () => {
    setSelectedAsset(null);
    setIsFormModalOpen(true);
  };

  const handleEdit = (asset) => {
    setSelectedAsset(asset);
    setIsFormModalOpen(true);
  };

  const handleDeleteClick = (asset) => {
    setAssetToDelete(asset);
    setIsDeleteModalOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!assetToDelete) return;
    try {
      await deleteAsset(assetToDelete.id);
      await fetchAssets();
      setIsDeleteModalOpen(false);
      setAssetToDelete(null);
    } catch (error) {
      console.error("Erro ao eliminar ativo:", error);
      alert("Não foi possível eliminar o ativo.");
    }
  };

  const handleFormSuccess = async () => {
    await fetchAssets();
    setIsFormModalOpen(false);
    setSelectedAsset(null);
  };

  // --- Colunas ---
  const columns = [
    { 
      header: 'Nome', 
      accessor: 'name',
      cell: (row) => (
        <div 
          onClick={() => handleViewDetails(row)}
          className="cursor-pointer group"
        >
            <div className="font-medium text-gray-900 group-hover:text-blue-600 transition-colors">
                {row.name}
            </div>
            <div className="text-xs text-gray-500">{row.internal_tag}</div>
        </div>
      )
    },
    { 
        header: 'Categoria', 
        accessor: 'category.name',
        cell: (row) => row.category?.name || '-'
    },
    { 
        header: 'Ativo Pai', 
        accessor: 'parent_asset.name',
        cell: (row) => row.parent_asset?.name || '-'
    },
    { 
        header: 'Local', 
        accessor: 'location.nome',
        cell: (row) => row.location?.nome || '-'
    },
    { 
      header: 'Status', 
      accessor: 'status',
      cell: (row) => {
        const statusColors = {
          OPERATIONAL: 'bg-green-100 text-green-800',
          NON_OPERATIONAL: 'bg-red-100 text-red-800',
          MAINTENANCE: 'bg-yellow-100 text-yellow-800',
          DECOMMISSIONED: 'bg-gray-100 text-gray-800'
        };
        const labels = {
          OPERATIONAL: 'Operacional',
          NON_OPERATIONAL: 'Parado',
          MAINTENANCE: 'Em Manutenção',
          DECOMMISSIONED: 'Desativado'
        };
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${statusColors[row.status] || 'bg-gray-100'}`}>
            {labels[row.status] || row.status}
          </span>
        );
      }
    },
    {
      header: 'Ações',
      accessor: 'actions',
      cell: (row) => (
        <div className="flex space-x-2 justify-end">
          <button 
            onClick={(e) => { e.stopPropagation(); handleViewDetails(row); }}
            className="text-gray-500 hover:text-blue-600 p-1 transition-colors"
            title="Ver Detalhes (Hub)"
          >
             <Eye className="w-5 h-5" /> 
          </button>
          <button 
            onClick={(e) => { e.stopPropagation(); handleEdit(row); }}
            className="text-blue-600 hover:text-blue-800 p-1 transition-colors"
            title="Editar"
          >
            <Edit2 className="w-5 h-5" />
          </button>
          <button 
            onClick={(e) => { e.stopPropagation(); handleDeleteClick(row); }}
            className="text-red-600 hover:text-red-800 p-1 transition-colors"
            title="Eliminar"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>
      )
    }
  ];

  return (
    <div className="container mx-auto">
      <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Gestão de Ativos</h1>
          <p className="text-sm text-gray-600">Gerir equipamentos e máquinas</p>
        </div>
        <button
          onClick={handleCreate}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors shadow-sm"
        >
          <Plus className="w-4 h-4" />
          Novo Ativo
        </button>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Pesquisar por nome, tag ou serial..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
        {/* IMPORTANTE: Não passamos onEdit nem onDelete aqui para não ativar a coluna automática do DataTable */}
        <DataTable
          columns={columns}
          data={assets}
          isLoading={isLoading}
          emptyMessage="Nenhum ativo encontrado."
        />
      </div>

      <Modal
        isOpen={isFormModalOpen}
        onClose={() => setIsFormModalOpen(false)}
        title={selectedAsset ? `Editar Ativo: ${selectedAsset.internal_tag}` : "Novo Ativo"}
        maxWidth="2xl"
      >
        <AssetForm
          assetToEdit={selectedAsset}
          onSuccess={handleFormSuccess}
          onCancel={() => setIsFormModalOpen(false)}
        />
      </Modal>

      <ConfirmationModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={handleConfirmDelete}
        title="Eliminar Ativo"
        message={`Tem a certeza que deseja eliminar o ativo?`}
        confirmText="Eliminar"
        cancelText="Cancelar"
        variant="danger"
      />
    </div>
  );
};

export default AssetManagementPage;