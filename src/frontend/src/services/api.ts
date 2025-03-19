import axios from 'axios';
import { PortfolioMetric, PerformanceData, AgentSignalsData, Activity } from '../types';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getPortfolioMetrics = async (): Promise<PortfolioMetric[]> => {
  const { data } = await api.get('/portfolio/metrics');
  return data;
};

export const getPerformanceData = async (): Promise<PerformanceData> => {
  const { data } = await api.get('/portfolio/performance');
  return data;
};

export const getAgentSignals = async (): Promise<AgentSignalsData> => {
  const { data } = await api.get('/agents/signals');
  return data;
};

export const getRecentActivity = async (): Promise<Activity[]> => {
  const { data } = await api.get('/activity/recent');
  return data;
};

export const executeOrder = async (
  symbol: string,
  action: 'BUY' | 'SELL',
  quantity: number
): Promise<void> => {
  await api.post('/orders', { symbol, action, quantity });
};

// Error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
); 