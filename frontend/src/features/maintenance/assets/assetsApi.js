// File: frontend/src/features/maintenance/assets/assetsApi.js

import apiClient from '../../../api/apiClient';

/**
 * Módulo de API para a gestão de Ativos (Assets).
 * Interage com os endpoints definidos em:
 * backend/app/modules/maintenance/assets/assets_router.py
 */

const ENDPOINT = '/maintenance/assets';

// --- CRUD Principal ---

/**
 * Obtém a lista de ativos com filtros opcionais.
 * @param {Object} params - Filtros: { skip, limit, search, sort_by, sort_order }
 */
export const getAssets = async (params = {}) => {
  const response = await apiClient.get(ENDPOINT, { params });
  return response.data;
};

/**
 * Obtém um ativo específico pelo ID.
 * @param {string} id - O UUID do ativo.
 */
export const getAsset = async (id) => {
  const response = await apiClient.get(`${ENDPOINT}/${id}`);
  return response.data;
};

/**
 * Cria um novo ativo.
 * @param {Object} data - O objeto AssetCreate (name, internal_tag, etc.)
 */
export const createAsset = async (data) => {
  const response = await apiClient.post(ENDPOINT, data);
  return response.data;
};

/**
 * Atualiza um ativo existente.
 * @param {string} id - O UUID do ativo.
 * @param {Object} data - O objeto AssetUpdate (campos a alterar).
 */
export const updateAsset = async (id, data) => {
  const response = await apiClient.put(`${ENDPOINT}/${id}`, data);
  return response.data;
};



/**

 * Elimina um ativo.

 * (Nota: O backend impedirá a eliminação se houver histórico associado)

 * @param {string} id - O UUID do ativo.

 */

export const deleteAsset = async (id) => {

  const response = await apiClient.delete(`${ENDPOINT}/${id}`);

  return response.data;

};



// --- Funções Relacionadas (para preencher selects, etc.) ---



/**

 * Obtém a lista de categorias de ativos.

 * @param {Object} params - Filtros opcionais.

 */

export const getAssetCategories = async (params = {}) => {

    const response = await apiClient.get('/maintenance/asset-categories', { params });

    return response.data;

};
