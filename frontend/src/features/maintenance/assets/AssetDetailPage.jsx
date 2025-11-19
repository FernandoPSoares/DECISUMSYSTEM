// File: frontend/src/features/maintenance/assets/AssetDetailPage.jsx

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Settings, Activity, GitMerge, Wrench, ClipboardList } from 'lucide-react';
import apiClient from '../../../api/apiClient';
import Tabs from '../../../components/ui/Tabs';
import Spinner from '../../../components/ui/Spinner';

// Importação das Abas (Vamos criar a seguir)
import AssetOverviewTab from './tabs/AssetOverviewTab';
import AssetStructureTab from './tabs/AssetStructureTab'; // Foco na hierarquia
import AssetHistoryTab from './tabs/AssetHistoryTab';

const AssetDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [asset, setAsset] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchAsset = async () => {
    setIsLoading(true);
    try {
      // Assume que o backend retorna as relações (child_assets, parent_asset, etc.)
      const response = await apiClient.get(`/maintenance/assets/${id}`);
      setAsset(response.data);
    } catch (error) {
      console.error("Erro ao carregar ativo:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAsset();
  }, [id]); // Recarrega se o ID mudar (navegação entre pai/filho)

  if (isLoading) return <div className="h-screen flex items-center justify-center"><Spinner /></div>;
  if (!asset) return <div className="p-6">Ativo não encontrado.</div>;

  // Helpers de UI
  const getStatusColor = (status) => {
    const map = {
      OPERATIONAL: 'bg-green-50 text-green-700 border-green-200',
      NON_OPERATIONAL: 'bg-red-50 text-red-700 border-red-200',
      MAINTENANCE: 'bg-yellow-50 text-yellow-700 border-yellow-200',
      DECOMMISSIONED: 'bg-gray-50 text-gray-600 border-gray-200',
    };
    return map[status] || 'bg-gray-50 text-gray-600';
  };

  // Definição das Abas com Ícones para melhor UX
  const tabs = [
    {
      id: 'overview',
      label: (
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4" /> Visão Geral
        </div>
      ),
      content: <AssetOverviewTab asset={asset} />
    },
    {
      id: 'structure',
      label: (
        <div className="flex items-center gap-2">
          <GitMerge className="w-4 h-4" /> Estrutura & Hierarquia
        </div>
      ),
      content: <AssetStructureTab asset={asset} onNavigate={(newId) => navigate(`/maintenance/assets/${newId}`)} />
    },
    {
      id: 'history',
      label: (
        <div className="flex items-center gap-2">
          <ClipboardList className="w-4 h-4" /> Histórico OS
        </div>
      ),
      content: <AssetHistoryTab workOrders={asset.work_orders || []} />
    }
  ];

  return (
    <div className="container mx-auto pb-10">
      {/* 1. Top Bar de Navegação */}
      <button 
        onClick={() => navigate('/maintenance/assets')}
        className="flex items-center text-gray-500 hover:text-gray-800 mb-4 transition-colors text-sm"
      >
        <ArrowLeft className="w-4 h-4 mr-1" /> Voltar à Lista
      </button>

      {/* 2. Header do Ativo (Card Principal) */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex flex-col md:flex-row justify-between items-start">
          
          {/* Identidade Principal */}
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">{asset.name}</h1>
              <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getStatusColor(asset.status)} uppercase tracking-wider`}>
                {asset.status}
              </span>
            </div>
            <div className="flex items-center text-gray-500 text-sm gap-4">
              <span className="flex items-center gap-1">
                <span className="font-semibold">TAG:</span> {asset.internal_tag}
              </span>
              {asset.serial_number && (
                <span className="flex items-center gap-1 border-l pl-4 border-gray-300">
                  <span className="font-semibold">S/N:</span> {asset.serial_number}
                </span>
              )}
            </div>
          </div>

          {/* Botões de Ação Rápida */}
          <div className="mt-4 md:mt-0 flex gap-2">
             <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium flex items-center gap-2 shadow-sm transition-all">
                <Wrench className="w-4 h-4" /> Abrir Ordem de Serviço
             </button>
             <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg border border-transparent hover:border-gray-200 transition-all">
                <Settings className="w-5 h-5" />
             </button>
          </div>
        </div>
      </div>

      {/* 3. Sistema de Abas */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden min-h-[400px]">
        <Tabs tabs={tabs} />
      </div>
    </div>
  );
};

export default AssetDetailPage;