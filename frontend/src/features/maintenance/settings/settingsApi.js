// File: frontend/src/features/maintenance/settings/settingsApi.js
import apiClient from '../../../api/apiClient';

/**
 * API Centralizada para Configurações e Tabelas Auxiliares de Manutenção.
 */

// ==========================================
// 1. FABRICANTES (MANUFACTURERS)
// ==========================================
const MANUFACTURERS_ENDPOINT = '/maintenance/manufacturers';

export const getManufacturers = async (params = {}) => {
  const response = await apiClient.get(MANUFACTURERS_ENDPOINT, { params });
  return response.data;
};

export const createManufacturer = async (data) => {
  const response = await apiClient.post(MANUFACTURERS_ENDPOINT, data);
  return response.data;
};

export const updateManufacturer = async (id, data) => {
  const response = await apiClient.put(`${MANUFACTURERS_ENDPOINT}${id}`, data);
  return response.data;
};

export const deleteManufacturer = async (id) => {
  const response = await apiClient.delete(`${MANUFACTURERS_ENDPOINT}/${id}`);
  return response.data;
};


// ==========================================
// 2. EQUIPAS DE MANUTENÇÃO (TEAMS)
// ==========================================
const TEAMS_ENDPOINT = '/maintenance/teams';

export const getMaintenanceTeams = async (params = {}) => {
  const response = await apiClient.get(TEAMS_ENDPOINT, { params });
  return response.data;
};

export const createMaintenanceTeam = async (data) => {
  const response = await apiClient.post(TEAMS_ENDPOINT, data);
  return response.data;
};

export const updateMaintenanceTeam = async (id, data) => {
  const response = await apiClient.put(`${TEAMS_ENDPOINT}/${id}`, data);
  return response.data;
};

export const deleteMaintenanceTeam = async (id) => {
  const response = await apiClient.delete(`${TEAMS_ENDPOINT}/${id}`);
  return response.data;
};


// ==========================================
// 3. ANÁLISE DE FALHAS (RCA - Root Cause Analysis)
// Nota: Certifique-se que estas rotas existem no backend (failure_modes_router.py)
// ==========================================

// 3.1 SINTOMAS DE FALHA (Failure Symptoms)
const SYMPTOMS_ENDPOINT = '/maintenance/failure-symptoms';

export const getFailureSymptoms = async (params = {}) => {
  const response = await apiClient.get(SYMPTOMS_ENDPOINT, { params });
  return response.data;
};

export const createFailureSymptom = async (data) => {
  const response = await apiClient.post(SYMPTOMS_ENDPOINT, data);
  return response.data;
};

export const updateFailureSymptom = async (id, data) => {
  const response = await apiClient.put(`${SYMPTOMS_ENDPOINT}/${id}`, data);
  return response.data;
};

export const deleteFailureSymptom = async (id) => {
  const response = await apiClient.delete(`${SYMPTOMS_ENDPOINT}/${id}`);
  return response.data;
};

// 3.2 MODOS DE FALHA (Failure Modes)
const MODES_ENDPOINT = '/maintenance/failure-modes';

export const getFailureModes = async (params = {}) => {
  const response = await apiClient.get(MODES_ENDPOINT, { params });
  return response.data;
};

export const createFailureMode = async (data) => {
  const response = await apiClient.post(MODES_ENDPOINT, data);
  return response.data;
};

export const updateFailureMode = async (id, data) => {
  const response = await apiClient.put(`${MODES_ENDPOINT}/${id}`, data);
  return response.data;
};

export const deleteFailureMode = async (id) => {
  const response = await apiClient.delete(`${MODES_ENDPOINT}/${id}`);
  return response.data;
};

// 3.3 CAUSAS DE FALHA (Failure Causes)
const CAUSES_ENDPOINT = '/maintenance/failure-causes';

export const getFailureCauses = async (params = {}) => {
  const response = await apiClient.get(CAUSES_ENDPOINT, { params });
  return response.data;
};

export const createFailureCause = async (data) => {
  const response = await apiClient.post(CAUSES_ENDPOINT, data);
  return response.data;
};

export const updateFailureCause = async (id, data) => {
  const response = await apiClient.put(`${CAUSES_ENDPOINT}/${id}`, data);
  return response.data;
};

export const deleteFailureCause = async (id) => {
  const response = await apiClient.delete(`${CAUSES_ENDPOINT}/${id}`);
  return response.data;
};