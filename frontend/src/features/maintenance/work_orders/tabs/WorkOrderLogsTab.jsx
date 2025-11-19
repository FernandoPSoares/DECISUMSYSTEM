// File: frontend/src/features/maintenance/work_orders/tabs/WorkOrderLogsTab.jsx
import React from 'react';
import { MessageSquare } from 'lucide-react';

const WorkOrderLogsTab = ({ workOrder, onUpdate }) => {
  return (
    <div className="p-4">
      <h3 className="text-lg font-medium text-gray-900 flex items-center mb-4">
        <MessageSquare className="w-5 h-5 mr-2 text-gray-500" />
        Histórico e Comentários
      </h3>

      <div className="space-y-4 mb-6">
        {(!workOrder.activity_logs || workOrder.activity_logs.length === 0) ? (
            <p className="text-gray-500 text-sm italic">Sem atividade registada.</p>
        ) : (
            workOrder.activity_logs.map(log => (
            <div key={log.id} className="flex space-x-3">
                <div className="flex-shrink-0">
                <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-xs font-bold text-gray-600">
                    {log.created_by_user?.full_name?.charAt(0) || '?'}
                </div>
                </div>
                <div className="flex-1 bg-gray-50 p-3 rounded-lg border border-gray-100">
                <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-medium text-gray-900">
                    {log.created_by_user?.full_name || 'Utilizador'}
                    </span>
                    <span className="text-xs text-gray-500">
                    {new Date(log.created_at).toLocaleString()}
                    </span>
                </div>
                <p className="text-sm text-gray-700">{log.log_entry}</p>
                </div>
            </div>
            ))
        )}
      </div>
      
      {/* Input Simples (Placeholder para funcionalidade futura) */}
      <div className="mt-4">
        <textarea 
            className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
            rows="2"
            placeholder="Escreva um comentário..."
        ></textarea>
        <button className="mt-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700">
            Enviar Comentário
        </button>
      </div>
    </div>
  );
};

export default WorkOrderLogsTab;