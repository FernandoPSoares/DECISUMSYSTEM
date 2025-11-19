// frontend/src/api/apiClient.js

import axios from 'axios';

// Cria uma instância do Axios pré-configurada para a nossa API.
// Isto evita que tenhamos de escrever a URL completa em todos os pedidos.
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // A URL base da nossa API FastAPI
});

export default apiClient;

