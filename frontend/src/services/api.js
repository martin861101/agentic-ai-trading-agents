import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8007';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error('API Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Health check
  async checkHealth() {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Get agents
  async getAgents() {
    const response = await this.client.get('/agents');
    return response.data;
  }

  // Get recent signals
  async getRecentSignals(limit = 50) {
    const response = await this.client.get(`/signals?limit=${limit}`);
    return response.data;
  }

  // Create manual signal
  async createManualSignal(signalData) {
    const response = await this.client.post('/manual_signal', signalData);
    return response.data;
  }
}

export default new ApiService();
