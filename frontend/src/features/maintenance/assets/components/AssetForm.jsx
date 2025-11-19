// File: frontend/src/features/maintenance/assets/components/AssetForm.jsx

import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { X } from 'lucide-react';
import apiClient from '../../../../api/apiClient';
import { createAsset, updateAsset, getAssetCategories, getAssets } from '../assetsApi';
import SearchableSelect from '../../../../components/ui/SearchableSelect';
import Spinner from '../../../../components/ui/Spinner';

const AssetForm = ({ assetToEdit, onSuccess, onCancel }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  const [manufacturers, setManufacturers] = useState([]);
  const [locations, setLocations] = useState([]);
  const [categories, setCategories] = useState([]);
  const [assets, setAssets] = useState([]);

  const [formData, setFormData] = useState({
    name: '',
    internal_tag: '',
    serial_number: '',
    description: '',
    is_critical: false,
    manufacturer_id: null,
    location_id: null,
    category_id: null,
    parent_asset_id: null,
    installation_date: '',
    warranty_expiry_date: ''
  });

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        const [manufRes, locRes, catRes, assetsRes] = await Promise.all([
          apiClient.get('/maintenance/manufacturers'),
          apiClient.get('/locais'),
          getAssetCategories(),
          getAssets({ limit: 1000 }) // Busca uma lista de ativos para o select de pai
        ]);
        
        setManufacturers(manufRes.data || []);
        setLocations(locRes.data || []);
        setCategories(catRes || []);
        // Filtra o próprio ativo da lista de pais potenciais
        setAssets(assetsRes.filter(a => a.id !== assetToEdit?.id) || []);

        if (assetToEdit) {
          setFormData({
            name: assetToEdit.name || '',
            internal_tag: assetToEdit.internal_tag || '',
            serial_number: assetToEdit.serial_number || '',
            description: assetToEdit.description || '',
            is_critical: assetToEdit.is_critical || false,
            manufacturer_id: assetToEdit.manufacturer_id || null,
            location_id: assetToEdit.location_id || null,
            category_id: assetToEdit.category_id || null,
            parent_asset_id: assetToEdit.parent_asset_id || null,
            installation_date: assetToEdit.installation_date ? assetToEdit.installation_date.split('T')[0] : '',
            warranty_expiry_date: assetToEdit.warranty_expiry_date ? assetToEdit.warranty_expiry_date.split('T')[0] : ''
          });
        }
      } catch (err) {
        console.error("Erro ao carregar dados auxiliares:", err);
        setError("Falha ao carregar listas de fabricantes, locais, categorias ou ativos.");
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [assetToEdit]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSelectChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value ? value.value : null }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsSaving(true);

    try {
      const payload = {
        ...formData,
        serial_number: formData.serial_number || null,
        description: formData.description || null,
        manufacturer_id: formData.manufacturer_id,
        location_id: formData.location_id,
        category_id: formData.category_id,
        parent_asset_id: formData.parent_asset_id,
        installation_date: formData.installation_date || null,
        warranty_expiry_date: formData.warranty_expiry_date || null,
      };

      if (assetToEdit) {
        await updateAsset(assetToEdit.id, payload);
      } else {
        await createAsset(payload);
      }
      
      onSuccess();
    } catch (err) {
      console.error("Erro ao salvar ativo:", err);
      const msg = err.response?.data?.detail || "Erro ao salvar o ativo. Verifique os dados.";
      setError(msg);
    } finally {
      setIsSaving(false);
    }
  };

  const loadOptions = (list, labelKey = 'name') => (inputValue) => {
    const filtered = list.filter(item =>
      item[labelKey].toLowerCase().includes(inputValue.toLowerCase())
    );
    return Promise.resolve(filtered.map(item => ({ value: item.id, label: item[labelKey] })));
  };
  
  const loadAssetOptions = (inputValue) => {
    const filtered = assets.filter(asset =>
      asset.name.toLowerCase().includes(inputValue.toLowerCase()) ||
      asset.internal_tag.toLowerCase().includes(inputValue.toLowerCase())
    );
    return Promise.resolve(filtered.map(asset => ({ 
        value: asset.id, 
        label: `${asset.name} (${asset.internal_tag})` 
    })));
  };


  const getStatusLabel = (status) => {
    const labels = {
      OPERATIONAL: 'Operacional',
      NON_OPERATIONAL: 'Parado',
      MAINTENANCE: 'Em Manutenção',
      DECOMMISSIONED: 'Desativado'
    };
    return labels[status] || status;
  };

  if (isLoading) {
    return <div className="p-6 flex justify-center"><Spinner /></div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-lg flex flex-col max-h-[90vh]">
      <div className="flex justify-between items-center p-4 border-b">
        <h3 className="text-lg font-semibold text-gray-800">
          {assetToEdit ? 'Editar Ativo' : 'Novo Ativo'}
        </h3>
        <button onClick={onCancel} className="text-gray-500 hover:text-gray-700">
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="p-6 overflow-y-auto">
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded text-sm">
            {error}
          </div>
        )}

        <form id="asset-form" onSubmit={handleSubmit} className="space-y-4">
          
          {assetToEdit && (
            <div className="bg-gray-50 p-3 rounded border border-gray-200 mb-4">
               <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Status Atual</label>
               <div className="flex items-center">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                    ${assetToEdit.status === 'OPERATIONAL' ? 'bg-green-100 text-green-800' : 
                      assetToEdit.status === 'MAINTENANCE' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}`}>
                    {getStatusLabel(assetToEdit.status)}
                  </span>
                  <span className="ml-2 text-xs text-gray-400 italic">
                    (Gerido automaticamente pelas Ordens de Serviço)
                  </span>
               </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nome do Ativo *</label>
              <input
                type="text"
                name="name"
                required
                value={formData.name}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">TAG Interna *</label>
              <input
                type="text"
                name="internal_tag"
                required
                value={formData.internal_tag}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Número de Série</label>
              <input
                type="text"
                name="serial_number"
                value={formData.serial_number}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
              <SearchableSelect
                loadOptions={loadOptions(categories, 'name')}
                defaultOptions
                value={categories.map(c => ({ value: c.id, label: c.name })).find(c => c.value === formData.category_id)}
                onChange={(val) => handleSelectChange('category_id', val)}
                placeholder="Selecione a categoria..."
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Fabricante</label>
              <SearchableSelect
                loadOptions={loadOptions(manufacturers, 'name')}
                defaultOptions
                value={manufacturers.map(m => ({ value: m.id, label: m.name })).find(m => m.value === formData.manufacturer_id)}
                onChange={(val) => handleSelectChange('manufacturer_id', val)}
                placeholder="Selecione o fabricante..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Localização</label>
              <SearchableSelect
                loadOptions={loadOptions(locations, 'nome')}
                defaultOptions
                value={locations.map(l => ({ value: l.id, label: l.nome })).find(l => l.value === formData.location_id)}
                onChange={(val) => handleSelectChange('location_id', val)}
                placeholder="Selecione o local..."
              />
            </div>
          </div>

          <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Ativo Pai (Opcional)</label>
              <SearchableSelect
                loadOptions={loadAssetOptions}
                defaultOptions
                value={assets.map(a => ({ value: a.id, label: `${a.name} (${a.internal_tag})` })).find(a => a.value === formData.parent_asset_id)}
                onChange={(val) => handleSelectChange('parent_asset_id', val)}
                placeholder="Selecione o ativo pai..."
                isClearable
              />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Data Instalação</label>
              <input
                type="date"
                name="installation_date"
                value={formData.installation_date}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Garantia Até</label>
              <input
                type="date"
                name="warranty_expiry_date"
                value={formData.warranty_expiry_date}
                onChange={handleChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
            <textarea
              name="description"
              rows="3"
              value={formData.description}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <div className="flex items-center">
            <input
              id="is_critical"
              name="is_critical"
              type="checkbox"
              checked={formData.is_critical}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor="is_critical" className="ml-2 block text-sm text-gray-900">
              Ativo Crítico (Prioridade Alta)
            </label>
          </div>

        </form>
      </div>

      <div className="p-4 border-t bg-gray-50 flex justify-end space-x-3 rounded-b-lg">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none"
        >
          Cancelar
        </button>
        <button
          type="submit"
          form="asset-form"
          disabled={isSaving}
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none flex items-center"
        >
          {isSaving && <Spinner size="sm" className="mr-2 text-white" />}
          {isSaving ? 'Salvando...' : 'Salvar Ativo'}
        </button>
      </div>
    </div>
  );
};

AssetForm.propTypes = {
  assetToEdit: PropTypes.object,
  onSuccess: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};

export default AssetForm;