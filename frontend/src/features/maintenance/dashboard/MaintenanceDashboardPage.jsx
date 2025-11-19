// File: frontend/src/features/maintenance/dashboard/MaintenanceDashboardPage.jsx

import React from 'react';

/**
 * Página do Dashboard de Manutenção (Esqueleto).
 * Esta é a página 'index' (inicial) do módulo /maintenance.
 * * (Fase 1.3 do nosso plano - Ficheiro 1 de 4)
 */
const MaintenanceDashboardPage = () => {
  return (
    <div className="container mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Dashboard de Manutenção
      </h1>
      <div className="p-6 bg-white rounded-lg shadow-md">
        <p className="text-gray-700">
          (Página de Dashboard em construção. Esta página irá conter KPIs, 
          gráficos de MTTR/MTBF, e listas de Ordens de Serviço críticas.)
        </p>
      </div>
    </div>
  );
};

export default MaintenanceDashboardPage;