// File: frontend/src/features/maintenance/work_orders/tabs/WorkOrderPartsTab.jsx
import React from 'react';
import { Box } from 'lucide-react';

const WorkOrderPartsTab = ({ workOrder, onUpdate }) => {
  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium text-gray-900 flex items-center">
          <Box className="w-5 h-5 mr-2 text-gray-500" />
          Peças Utilizadas
        </h3>
        <button className="text-sm text-blue-600 hover:underline">
          + Adicionar Peça
        </button>
      </div>

      {(!workOrder.parts_used || workOrder.parts_used.length === 0) ? (
        <p className="text-gray-500 text-sm italic">Nenhuma peça/material utilizado.</p>
      ) : (
        <ul className="space-y-2">
          {workOrder.parts_used.map(part => (
            <li key={part.id} className="flex justify-between items-center p-3 bg-gray-50 rounded border border-gray-200">
              <span className="text-sm text-gray-700">
                Produto ID: <span className="font-mono text-xs">{part.product_id.substring(0,8)}...</span>
              </span>
              <span className="text-sm font-bold text-gray-900">
                Qtd: {part.quantity_used}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default WorkOrderPartsTab;