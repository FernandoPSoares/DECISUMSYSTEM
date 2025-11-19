// File: frontend/src/features/maintenance/work_orders/workOrdersApi.js

import apiClient from '../../../api/apiClient';

/**
 * Módulo de API para a gestão de Ordens de Serviço (Work Orders).
 * Interage com os endpoints definidos em:
 * backend/app/modules/maintenance/work_orders/work_orders_router.py
 */

const ENDPOINT = '/maintenance/work-orders';

// ==========================================
// 1. CRUD PRINCIPAL (WORK ORDERS)
// ==========================================

/**
 * Obtém a lista de Ordens de Serviço com filtros.
 * @param {Object} params - { skip, limit, search, sort_by, sort_order }
 */
export const getWorkOrders = async (params = {}) => {
  const response = await apiClient.get(ENDPOINT, { params });
  return response.data;
};

/**
 * Obtém os detalhes completos de uma OS específica.
 * Inclui tarefas, logs, peças e mão de obra.
 * @param {string} id - UUID da Work Order.
 */
export const getWorkOrder = async (id) => {
  const response = await apiClient.get(`${ENDPOINT}/${id}`);
  return response.data;
};

/**
 * Cria uma nova Ordem de Serviço.
 * @param {Object} data - WorkOrderCreate { title, asset_id, ... }
 */
export const createWorkOrder = async (data) => {
  const response = await apiClient.post(ENDPOINT, data);
  return response.data;
};

/**
 * Atualiza uma OS existente.
 * @param {string} id - UUID da Work Order.
 * @param {Object} data - WorkOrderUpdate { status, priority, ... }
 */
export const updateWorkOrder = async (id, data) => {
  const response = await apiClient.put(`${ENDPOINT}/${id}`, data);
  return response.data;
};

/**
 * Elimina uma OS (Apenas se status for DRAFT).
 * @param {string} id - UUID da Work Order.
 */
export const deleteWorkOrder = async (id) => {
  const response = await apiClient.delete(`${ENDPOINT}/${id}`);
  return response.data;
};


// ==========================================
// 2. SUB-API: LOGS (COMENTÁRIOS)
// ==========================================

export const getWorkOrderLogs = async (woId) => {
  const response = await apiClient.get(`${ENDPOINT}/${woId}/logs`);
  return response.data;
};

export const createWorkOrderLog = async (woId, data) => {
  // data: { log_entry: "texto" }
  const response = await apiClient.post(`${ENDPOINT}/${woId}/logs`, data);
  return response.data;
};

export const deleteWorkOrderLog = async (woId, logId) => {
  const response = await apiClient.delete(`${ENDPOINT}/${woId}/logs/${logId}`);
  return response.data;
};


// ==========================================
// 3. SUB-API: TAREFAS (CHECKLIST)
// ==========================================

export const getWorkOrderTasks = async (woId) => {
  const response = await apiClient.get(`${ENDPOINT}/${woId}/tasks`);
  return response.data;
};

export const createWorkOrderTask = async (woId, data) => {
  // data: { description: "Verificar óleo" }
  const response = await apiClient.post(`${ENDPOINT}/${woId}/tasks`, data);
  return response.data;
};

export const updateWorkOrderTask = async (woId, taskId, data) => {
  // data: { completed: true } ou { description: "..." }
  const response = await apiClient.put(`${ENDPOINT}/${woId}/tasks/${taskId}`, data);
  return response.data;
};

export const deleteWorkOrderTask = async (woId, taskId) => {
  const response = await apiClient.delete(`${ENDPOINT}/${woId}/tasks/${taskId}`);
  return response.data;
};


// ==========================================
// 4. SUB-API: MÃO DE OBRA (LABOR LOGS)
// ==========================================

export const getWorkOrderLaborLogs = async (woId) => {
  const response = await apiClient.get(`${ENDPOINT}/${woId}/labor-logs`);
  return response.data;
};

export const createWorkOrderLaborLog = async (woId, data) => {
  // data: { technician_id, start_time, hours }
  const response = await apiClient.post(`${ENDPOINT}/${woId}/labor-logs`, data);
  return response.data;
};

export const updateWorkOrderLaborLog = async (woId, laborId, data) => {
  const response = await apiClient.put(`${ENDPOINT}/${woId}/labor-logs/${laborId}`, data);
  return response.data;
};

export const deleteWorkOrderLaborLog = async (woId, laborId) => {
  const response = await apiClient.delete(`${ENDPOINT}/${woId}/labor-logs/${laborId}`);
  return response.data;
};


// ==========================================
// 5. SUB-API: PEÇAS (PARTS)
// ==========================================

export const getWorkOrderParts = async (woId) => {
  const response = await apiClient.get(`${ENDPOINT}/${woId}/parts`);
  return response.data;
};

export const createWorkOrderPartUsage = async (woId, data) => {
  // data: { product_id, quantity_used }
  const response = await apiClient.post(`${ENDPOINT}/${woId}/parts`, data);
  return response.data;
};

export const updateWorkOrderPartUsage = async (woId, partUsageId, data) => {
  // data: { quantity_used: 5 }
  const response = await apiClient.put(`${ENDPOINT}/${woId}/parts/${partUsageId}`, data);
  return response.data;
};

export const deleteWorkOrderPartUsage = async (woId, partUsageId) => {
  const response = await apiClient.delete(`${ENDPOINT}/${woId}/parts/${partUsageId}`);
  return response.data;
};