'use client';

import { useState, useEffect } from 'react';
import { Play, Database, FileText, Briefcase, TrendingUp } from 'lucide-react';
import { apiClient } from '@/lib/api';
import Link from 'next/link';

export default function DashboardPage() {
  const [stats, setStats] = useState({
    total: 0,
    news: 0,
    jobs: 0,
    today: 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isScraping, setIsScraping] = useState(false);

  useEffect(() => {
    loadStats();
    const interval = setInterval(loadStats, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, []);

  const loadStats = async () => {
    try {
      setIsLoading(true);
      const items = await apiClient.getItems({ limit: 1000 });
      
      const today = new Date().toDateString();
      const todayItems = items.filter(
        item => new Date(item.scraped_at).toDateString() === today
      );

      setStats({
        total: items.length,
        news: items.filter(i => i.tags?.includes('news')).length,
        jobs: items.filter(i => i.tags?.includes('jobs')).length,
        today: todayItems.length,
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const runScrapers = async () => {
    try {
      setIsScraping(true);
      await apiClient.runScrapers({});
      alert('Scrapers started successfully!');
      setTimeout(loadStats, 3000);
    } catch (error) {
      alert('Failed to start scrapers');
    } finally {
      setIsScraping(false);
    }
  };

  const StatCard = ({ icon: Icon, label, value, color }: any) => (
    <div className="card p-6 hover:scale-105 transform transition-all duration-300 animate-float">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 dark:text-gray-400 text-sm">{label}</p>
          <p className={`text-3xl font-bold mt-2 ${color}`}>{value}</p>
        </div>
        <div className={`p-4 rounded-full ${color} bg-opacity-10`}>
          <Icon className="w-8 h-8" />
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-dark-bg dark:to-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-primary-500 to-purple-500 bg-clip-text text-transparent">
            Welcome to CrawlX
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            Advanced web scraping with AI-powered content extraction
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center gap-4 mb-12">
          <button
            onClick={runScrapers}
            disabled={isScraping}
            className="btn-primary flex items-center gap-2 px-6 py-3 text-lg"
          >
            <Play className="w-5 h-5" />
            {isScraping ? 'Scraping...' : 'Run Pre-configured Scrapers'}
          </button>
          <Link href="/scraper" className="btn-secondary flex items-center gap-2 px-6 py-3 text-lg">
            <Database className="w-5 h-5" />
            Scrape Custom URL
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <StatCard
            icon={Database}
            label="Total Items"
            value={stats.total}
            color="text-blue-500"
          />
          <StatCard
            icon={TrendingUp}
            label="Scraped Today"
            value={stats.today}
            color="text-green-500"
          />
          <StatCard
            icon={FileText}
            label="News Articles"
            value={stats.news}
            color="text-purple-500"
          />
          <StatCard
            icon={Briefcase}
            label="Job Listings"
            value={stats.jobs}
            color="text-orange-500"
          />
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <FeatureCard
            title="Custom URL Scraper"
            description="Scrape any website with intelligent content extraction"
            link="/scraper"
          />
          <FeatureCard
            title="Data Explorer"
            description="Browse, search, and export your scraped data"
            link="/data"
          />
          <FeatureCard
            title="AI-Powered"
            description="Smart content detection and extraction"
            link="/"
          />
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ title, description, link }: { title: string; description: string; link: string }) {
  return (
    <Link href={link} className="card p-6 hover:shadow-xl transition-all duration-300 group">
      <h3 className="text-xl font-semibold mb-2 group-hover:text-primary-500 transition-colors">
        {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-400">{description}</p>
    </Link>
  );
}
