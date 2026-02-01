import axios from 'axios';
import type { ScrapedItem, UrlScrapeRequest, UrlScrapeResponse, ScrapeJobRequest, ScrapeJobResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiClient = {
  // Health check
  health: async () => {
    const { data } = await api.get('/health');
    return data;
  },

  // Get all items
  getItems: async (params?: { skip?: number; limit?: number; tag?: string }) => {
    const { data } = await api.get<ScrapedItem[]>('/items', { params });
    return data;
  },

  // Search items
  searchItems: async (params: { q: string; skip?: number; limit?: number; tag?: string; fuzzy?: boolean }) => {
    const { data } = await api.get<ScrapedItem[]>('/search', { params });
    return data;
  },

  // Run scrapers
  runScrapers: async (payload: ScrapeJobRequest) => {
    const { data } = await api.post<ScrapeJobResponse>('/scrape/run', null, {
      params: {
        spiders: payload.spiders,
      },
      paramsSerializer: {
        indexes: null, // This makes arrays send as ?spiders=news&spiders=jobs
      },
    });
    return data;
  },

  // Scrape custom URL
  scrapeUrl: async (payload: UrlScrapeRequest) => {
    const { data } = await api.post<UrlScrapeResponse>('/scrape/url', payload);
    return data;
  },

  // Export data
  exportJSON: async () => {
    const { data } = await api.get('/items/export');
    return data;
  },

  exportCSV: async () => {
    const response = await api.get('/items/export/csv', { responseType: 'blob' });
    return response.data;
  },

  exportPDF: async (params?: { style?: string; limit?: number; tag?: string }) => {
    const response = await api.get('/items/export/pdf', {
      params,
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api;
