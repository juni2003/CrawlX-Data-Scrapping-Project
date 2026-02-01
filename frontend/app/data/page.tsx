'use client';

import { useState, useEffect } from 'react';
import { Search, Download, ExternalLink } from 'lucide-react';
import { apiClient } from '@/lib/api';
import type { ScrapedItem } from '@/types';
import { formatDistanceToNow } from 'date-fns';

export default function DataExplorerPage() {
  const [items, setItems] = useState<ScrapedItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTag, setSelectedTag] = useState('');
  const [fuzzy, setFuzzy] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadItems();
  }, [selectedTag]);

  const loadItems = async () => {
    try {
      setIsLoading(true);
      const data = await apiClient.getItems({
        limit: 100,
        tag: selectedTag || undefined,
      });
      setItems(data);
    } catch (error) {
      console.error('Failed to load items:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery) {
      loadItems();
      return;
    }

    try {
      setIsLoading(true);
      const data = await apiClient.searchItems({
        q: searchQuery,
        tag: selectedTag || undefined,
        fuzzy,
        limit: 100,
      });
      setItems(data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async (format: 'csv' | 'pdf') => {
    try {
      let blob;
      let filename;

      if (format === 'csv') {
        blob = await apiClient.exportCSV();
        filename = 'scraped_data.csv';
      } else {
        blob = await apiClient.exportPDF({ style: 'detailed', limit: 100 });
        filename = 'scraped_data.pdf';
      }

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
    } catch (error) {
      alert('Export failed');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-dark-bg dark:to-gray-900 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-primary-500 to-purple-500 bg-clip-text text-transparent">
            Data Explorer
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Browse, search, and export your scraped content
          </p>
        </div>

        {/* Search & Filters */}
        <div className="card p-6 mb-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {/* Search */}
            <div className="lg:col-span-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  placeholder="Search titles and content..."
                  className="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-primary-500 outline-none"
                />
              </div>
              <div className="flex items-center gap-2 mt-2">
                <input
                  type="checkbox"
                  id="fuzzy"
                  checked={fuzzy}
                  onChange={(e) => setFuzzy(e.target.checked)}
                  className="rounded"
                />
                <label htmlFor="fuzzy" className="text-sm text-gray-600 dark:text-gray-400">
                  Fuzzy search
                </label>
              </div>
            </div>

            {/* Tag Filter */}
            <div>
              <select
                value={selectedTag}
                onChange={(e) => setSelectedTag(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-primary-500 outline-none"
              >
                <option value="">All Tags</option>
                <option value="news">News</option>
                <option value="tech">Tech</option>
                <option value="jobs">Jobs</option>
                <option value="remote">Remote</option>
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2 mt-4">
            <button onClick={handleSearch} className="btn-primary">
              Search
            </button>
            <button onClick={() => { setSearchQuery(''); setSelectedTag(''); loadItems(); }} className="btn-secondary">
              Reset
            </button>
            <button onClick={() => handleExport('csv')} className="btn-secondary ml-auto">
              <Download className="w-4 h-4 mr-1" />
              Export CSV
            </button>
            <button onClick={() => handleExport('pdf')} className="btn-secondary">
              <Download className="w-4 h-4 mr-1" />
              Export PDF
            </button>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-4 text-sm text-gray-600 dark:text-gray-400">
          {isLoading ? 'Loading...' : `${items.length} items found`}
        </div>

        {/* Data Table */}
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tags
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Scraped
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Link
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {items.map((item) => (
                  <tr
                    key={item.id}
                    className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                  >
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {item.title}
                      </div>
                      {item.summary && (
                        <div className="text-sm text-gray-500 mt-1 line-clamp-2">
                          {item.summary}
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900 dark:text-gray-100">
                        {item.source}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {item.tags?.map((tag, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 text-xs bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDistanceToNow(new Date(item.scraped_at), { addSuffix: true })}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-500 hover:text-primary-600"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {items.length === 0 && !isLoading && (
            <div className="text-center py-12 text-gray-500">
              No items found. Try running the scrapers first!
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
