// File: frontend/src/features/maintenance/assets/tabs/AssetStructureTab.jsx
import React from 'react';
import { ArrowUpRight, CornerDownRight, Box, Layers } from 'lucide-react';

const AssetStructureTab = ({ asset, onNavigate }) => {
  
  const hasParent = !!asset.parent_asset;
  const hasChildren = asset.child_assets && asset.child_assets.length > 0;

  if (!hasParent && !hasChildren) {
    return (
      <div className="p-12 text-center flex flex-col items-center text-gray-400">
        <Layers className="w-12 h-12 mb-3 opacity-20" />
        <p>Este ativo não possui hierarquia associada (nem pai, nem sub-componentes).</p>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl">
      <h3 className="text-lg font-semibold text-gray-800 mb-6 flex items-center gap-2">
        <GitMerge className="w-5 h-5 text-blue-500" /> Árvore de Ativos
      </h3>

      <div className="relative pl-4 border-l-2 border-gray-100 space-y-8">
        
        {/* 1. Ativo PAI (Se existir) */}
        {hasParent && (
          <div className="relative">
            <span className="absolute -left-[25px] top-1/2 -translate-y-1/2 bg-gray-100 text-gray-500 p-1 rounded-full">
               <ArrowUpRight className="w-4 h-4" />
            </span>
            <p className="text-xs uppercase font-bold text-gray-400 mb-2 pl-4">Ativo Pai (Superior)</p>
            
            <div 
              onClick={() => onNavigate(asset.parent_asset.id)}
              className="ml-4 p-4 border border-gray-200 rounded-lg bg-gray-50 hover:bg-white hover:border-blue-300 hover:shadow-md cursor-pointer transition-all group"
            >
              <div className="flex justify-between items-center">
                <div>
                  <h4 className="font-bold text-gray-800 group-hover:text-blue-600 transition-colors">
                    {asset.parent_asset.name}
                  </h4>
                  <p className="text-sm text-gray-500">{asset.parent_asset.internal_tag}</p>
                </div>
                <span className="text-xs px-2 py-1 bg-white rounded border border-gray-200 text-gray-500">
                  {asset.parent_asset.status}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* 2. Ativo ATUAL (O Foco) */}
        <div className="relative my-8">
           <span className="absolute -left-[21px] top-1/2 -translate-y-1/2 w-3 h-3 bg-blue-500 rounded-full ring-4 ring-white"></span>
           <div className="ml-4 p-5 bg-blue-50 border-2 border-blue-100 rounded-xl shadow-sm">
              <div className="flex items-center gap-3">
                 <Box className="w-6 h-6 text-blue-600" />
                 <div>
                    <h4 className="font-bold text-blue-900 text-lg">{asset.name}</h4>
                    <p className="text-sm text-blue-600">Ativo Atual</p>
                 </div>
              </div>
           </div>
        </div>

        {/* 3. Ativos FILHOS (Lista) */}
        {hasChildren && (
          <div className="relative">
            <span className="absolute -left-[25px] top-4 bg-gray-100 text-gray-500 p-1 rounded-full">
               <CornerDownRight className="w-4 h-4" />
            </span>
            <p className="text-xs uppercase font-bold text-gray-400 mb-3 pl-4">Sub-Ativos / Componentes ({asset.child_assets.length})</p>
            
            <div className="ml-4 grid grid-cols-1 md:grid-cols-2 gap-3">
              {asset.child_assets.map((child) => (
                <div 
                  key={child.id}
                  onClick={() => onNavigate(child.id)}
                  className="p-3 border border-gray-200 rounded-lg hover:border-blue-400 hover:shadow-sm cursor-pointer bg-white transition-all group flex items-center justify-between"
                >
                  <div>
                    <h5 className="font-medium text-gray-700 group-hover:text-blue-600">
                      {child.name}
                    </h5>
                    <p className="text-xs text-gray-400">{child.internal_tag}</p>
                  </div>
                  {/* Mini badge de status */}
                  <div className={`w-2 h-2 rounded-full ${
                    child.status === 'OPERATIONAL' ? 'bg-green-500' : 'bg-red-500'
                  }`} title={child.status}></div>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
};

export default AssetStructureTab;