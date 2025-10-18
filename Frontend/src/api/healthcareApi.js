import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const healthcareApi = {
  analyzeSymptoms: async (symptoms) => {
    const response = await api.post('/analyze', { symptoms });
    return response.data;
  },

  analyzeSymptomsWithCrew: async (symptoms) => {
    const response = await api.post('/analyze-crew', { symptoms });
    return response.data;
  },

  getHospitals: async () => {
    const response = await api.get('/hospitals');
    return response.data;
  },

  queryRAG: async (symptoms) => {
    const response = await api.post('/rag-query', { symptoms });
    return response.data;
  },

  getHealthStatus: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default healthcareApi;