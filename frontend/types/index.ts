// API Types matching backend schemas

export interface ScrapedItem {
  id: number;
  source: string;
  title: string;
  url: string;
  summary: string | null;
  tags: string[] | null;
  published_at: string | null;
  scraped_at: string;
}

export interface UrlScrapeRequest {
  url: string;
  extract_type: 'auto' | 'article' | 'text' | 'structured';
  wait_for?: number;
}

export interface UrlScrapeResponse {
  success: boolean;
  url: string;
  title?: string;
  content?: string;
  author?: string;
  published_date?: string;
  description?: string;
  tags?: string[];
  tables?: string[][][];
  lists?: string[][];
  extracted_at: string;
  extraction_method?: string;
  error?: string;
}

export interface ScrapeJobRequest {
  spiders?: string;
}

export interface ScrapeJobResponse {
  status: string;
  spiders: string[];
  message: string;
}

export type ThemeMode = 'light' | 'dark';
export type ViewMode = 'table' | 'cards';
