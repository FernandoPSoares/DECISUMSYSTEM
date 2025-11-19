import React from 'react';
import { MapPin, Factory, Calendar, FileText, Tag } from 'lucide-react';

const InfoCard = ({ icon: Icon, title, value, subValue }) => (
  <div className="flex items-start p-4 bg-gray-50 rounded-lg border border-gray-100">
    <div className="p-2 bg-white rounded-md shadow-sm mr-3">
      <Icon className="w-5 h-5 text-gray-500" />
    </div>
    <div>
      <p className="text-xs font-bold text-gray-400 uppercase tracking-wide">{title}</p>
      <p className="text-sm font-medium text-gray-900 mt-1">{value || '-'}</p>
      {subValue && <p className="text-xs text-gray-500 mt-0.5">{subValue}</p>}
    </div>
  </div>
);

const AssetOverviewTab = ({ asset }) => {
  return (
    <div className="p-6 space-y-6">
      
      {/* Seção 1: Localização e Origem */}
      <section>
        <h4 className="text-sm font-bold text-gray-900 mb-3 flex items-center gap-2">
          Localização & Fabricante
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <InfoCard 
            icon={Tag} 
            title="Categoria" 
            value={asset.category?.name || 'N/A'} 
          />
          <InfoCard 
            icon={MapPin} 
            title="Localização" 
            value={asset.location?.nome || 'N/A'} 
            subValue="Módulo de Inventário"
          />
          <InfoCard 
            icon={Factory} 
            title="Fabricante" 
            value={asset.manufacturer?.name || 'N/A'} 
            subValue={asset.manufacturer?.contact_phone}
          />
        </div>
      </section>

      <hr className="border-gray-100" />

      {/* Seção 2: Datas e Garantia */}
      <section>
        <h4 className="text-sm font-bold text-gray-900 mb-3 flex items-center gap-2">
          Ciclo de Vida
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <InfoCard 
            icon={Calendar} 
            title="Data de Instalação" 
            value={asset.installation_date ? new Date(asset.installation_date).toLocaleDateString() : '-'} 
          />
          <InfoCard 
            icon={Calendar} 
            title="Fim da Garantia" 
            value={asset.warranty_expiry_date ? new Date(asset.warranty_expiry_date).toLocaleDateString() : '-'} 
            subValue={new Date(asset.warranty_expiry_date) < new Date() ? 'Expirada' : 'Em Vigor'}
          />
           <InfoCard 
            icon={FileText} 
            title="Modelo / Serial" 
            value={asset.serial_number || 'N/A'}
          />
        </div>
      </section>

      {/* Seção 3: Descrição */}
      {asset.description && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-100 text-blue-900 text-sm">
          <span className="font-bold block mb-1">Observações:</span>
          {asset.description}
        </div>
      )}
    </div>
  );
};

export default AssetOverviewTab;