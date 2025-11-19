// File: frontend/src/features/maintenance/assets/tabs/AssetHistoryTab.jsx

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ClipboardList, ArrowRight, AlertCircle } from 'lucide-react';

const AssetHistoryTab = ({ workOrders = [] }) => {
  const navigate = useNavigate();

  // Estado vazio (sem histórico)
  if (workOrders.length === 0) {
    return (
      <div className="p-12 text-center flex flex-col items-center text-gray-400">
        <ClipboardList className="w-12 h-12 mb-3 opacity-20" />
        <p>Nenhuma Ordem de Serviço registada para este ativo.</p>
      </div>
    );
  }

  const getStatusColor = (status) => {
    const styles = {
      DRAFT: 'bg-gray-100 text-gray-700 border border-gray-200',
      OPEN: 'bg-blue-50 text-blue-700 border border-blue-200',
      IN_PROGRESS: 'bg-yellow-50 text-yellow-800 border border-yellow-200',
      ON_HOLD: 'bg-orange-50 text-orange-800 border border-orange-200',
      COMPLETED: 'bg-green-50 text-green-800 border border-green-200',
      CANCELLED: 'bg-red-50 text-red-800 border border-red-200',
    };
    return styles[status] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
          <ClipboardList className="w-5 h-5 text-blue-500" /> Histórico de Intervenções
        </h3>
        <span className="text-xs font-medium bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
          Total: {workOrders.length}
        </span>
      </div>
      
      <div className="overflow-hidden rounded-lg border border-gray-200 shadow-sm">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Nº OS</th>
              <th className="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Título / Descrição</th>
              <th className="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Ação</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {workOrders.map((wo) => (
              <tr key={wo.id} className="hover:bg-gray-50 transition-colors group">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-700">
                  {wo.wo_number}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  <div className="font-medium text-gray-900">{wo.title}</div>
                  {/* Futuramente: Adicionar data aqui se o backend enviar created_at */}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full border ${getStatusColor(wo.status)}`}>
                    {wo.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button 
                    onClick={() => navigate(`/maintenance/work-orders/${wo.id}`)}
                    className="text-gray-400 hover:text-blue-600 transition-colors p-2 rounded-full hover:bg-blue-50"
                    title="Ver Detalhes da OS"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AssetHistoryTab;