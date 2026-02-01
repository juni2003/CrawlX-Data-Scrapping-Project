'use client';

import { useState } from 'react';
import { Globe, Loader2, CheckCircle, XCircle, Copy, Download } from 'lucide-react';
import { apiClient } from '@/lib/api';
import type { UrlScrapeResponse } from '@/types';

export default function CustomScraperPage() {
  const [url, setUrl] = useState('');
  const [extractType, setExtractType] = useState<'auto' | 'article' | 'text' | 'structured'>('auto');
  const [waitFor, setWaitFor] = useState(2);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<UrlScrapeResponse | null>(null);
  const [error, setError] = useState('');

  const handleScrape = async () => {
    if (!url) {
      setError('Please enter a URL');
      return;
    }

    try {
      setIsLoading(true);
      setError('');
      setResult(null);

      const data = await apiClient.scrapeUrl({
        url,
        extract_type: extractType,
        wait_for: waitFor,
      });

      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to scrape URL');
    } finally {
      setIsLoading(false);
    }
  };

  const copyContent = () => {
    if (result?.content) {
      navigator.clipboard.writeText(result.content);
      alert('Content copied to clipboard!');
    }
  };

  const downloadAsText = () => {
    if (result?.content) {
      const blob = new Blob([result.content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${result.title || 'scraped-content'}.txt`;
      a.click();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-dark-bg dark:to-gray-900 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-primary-500 to-purple-500 bg-clip-text text-transparent">
            Custom URL Scraper
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Extract content from any website with AI-powered intelligence
          </p>
        </div>

        {/* Input Form */}
        <div className="card p-8 mb-8">
          <div className="space-y-6">
            {/* URL Input */}
            <div>
              <label className="block text-sm font-medium mb-2">Website URL</label>
              <div className="relative">
                <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com/article"
                  className="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-primary-500 outline-none"
                />
              </div>
            </div>

            {/* Extract Type */}
            <div>
              <label className="block text-sm font-medium mb-2">Extraction Mode</label>
              <select
                value={extractType}
                onChange={(e) => setExtractType(e.target.value as any)}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-primary-500 outline-none"
              >
                <option value="auto">Auto (Recommended)</option>
                <option value="article">Article - Optimized for news/blogs</option>
                <option value="text">Text - Extract all text content</option>
                <option value="structured">Structured - Tables and lists</option>
              </select>
            </div>

            {/* Wait Time */}
            <div>
              <label className="block text-sm font-medium mb-2">
                Wait Time: {waitFor}s
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={waitFor}
                onChange={(e) => setWaitFor(parseInt(e.target.value))}
                className="w-full"
              />
              <p className="text-xs text-gray-500 mt-1">
                Time to wait for page content to load
              </p>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleScrape}
              disabled={isLoading}
              className="w-full btn-primary py-4 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Scraping...
                </>
              ) : (
                <>
                  <Globe className="w-5 h-5" />
                  Scrape Website
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="card p-4 mb-8 bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
            <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
              <XCircle className="w-5 h-5" />
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Result Display */}
        {result && result.success && (
          <div className="card p-8 space-y-6">
            {/* Success Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                <CheckCircle className="w-6 h-6" />
                <span className="font-semibold">Successfully Scraped!</span>
              </div>
              <div className="flex gap-2">
                <button onClick={copyContent} className="btn-secondary flex items-center gap-1">
                  <Copy className="w-4 h-4" />
                  Copy
                </button>
                <button onClick={downloadAsText} className="btn-secondary flex items-center gap-1">
                  <Download className="w-4 h-4" />
                  Download
                </button>
              </div>
            </div>

            {/* Metadata */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-sm text-gray-500">Title:</span>
                <p className="font-medium">{result.title || 'N/A'}</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Author:</span>
                <p className="font-medium">{result.author || 'N/A'}</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Published:</span>
                <p className="font-medium">{result.published_date || 'N/A'}</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Method:</span>
                <p className="font-medium capitalize">{result.extraction_method}</p>
              </div>
            </div>

            {/* Description */}
            {result.description && (
              <div>
                <span className="text-sm text-gray-500 block mb-1">Description:</span>
                <p className="text-gray-700 dark:text-gray-300">{result.description}</p>
              </div>
            )}

            {/* Tags */}
            {result.tags && result.tags.length > 0 && (
              <div>
                <span className="text-sm text-gray-500 block mb-2">Tags:</span>
                <div className="flex flex-wrap gap-2">
                  {result.tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-full text-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Content */}
            {result.content && (
              <div>
                <span className="text-sm text-gray-500 block mb-2">Extracted Content:</span>
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 max-h-96 overflow-y-auto">
                  <pre className="whitespace-pre-wrap text-sm">{result.content}</pre>
                </div>
              </div>
            )}

            {/* Tables */}
            {result.tables && result.tables.length > 0 && (
              <div>
                <span className="text-sm text-gray-500 block mb-2">Tables Found: {result.tables.length}</span>
                {result.tables.slice(0, 3).map((table, idx) => (
                  <div key={idx} className="overflow-x-auto mb-4">
                    <table className="min-w-full border border-gray-300 dark:border-gray-600">
                      <tbody>
                        {table.map((row, rowIdx) => (
                          <tr key={rowIdx}>
                            {row.map((cell, cellIdx) => (
                              <td
                                key={cellIdx}
                                className="border border-gray-300 dark:border-gray-600 px-4 py-2 text-sm"
                              >
                                {cell}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ))}
              </div>
            )}

            {/* Lists */}
            {result.lists && result.lists.length > 0 && (
              <div>
                <span className="text-sm text-gray-500 block mb-2">Lists Found: {result.lists.length}</span>
                {result.lists.slice(0, 3).map((list, idx) => (
                  <ul key={idx} className="list-disc list-inside space-y-1 mb-4">
                    {list.map((item, itemIdx) => (
                      <li key={itemIdx} className="text-sm">{item}</li>
                    ))}
                  </ul>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
