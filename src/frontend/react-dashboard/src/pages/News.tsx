import React, { useState, useEffect } from 'react'
import { NewspaperIcon, ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline'

interface NewsArticle {
  title: string;
  description: string;
  url: string;
  source: string;
  published_at: string;
  is_relevant: boolean;
}

interface NewsData {
  ticker: string;
  total_results: number;
  articles: NewsArticle[];
  sources: string[];
  keywords: string[];
  date_range: {
    from: string;
    to: string;
  };
}

const News = () => {
  const [selectedTicker, setSelectedTicker] = useState('AAPL');
  const [newsData, setNewsData] = useState<NewsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const popularTickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'];
  
  const fetchNews = async (ticker: string) => {
    setLoading(true);
    setError('');
    
    try {
      // In a real implementation, this would call the MCP server
      const response = await fetch(`/api/news?ticker=${ticker}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch news data');
      }
      
      const data = await response.json();
      setNewsData(data);
    } catch (err) {
      console.error('Error fetching news:', err);
      setError('Failed to load news data. Please try again later.');
      
      // Generate mock data for demo purposes
      generateMockNewsData(ticker);
    } finally {
      setLoading(false);
    }
  };
  
  const generateMockNewsData = (ticker: string) => {
    // Mock data generation for demo purposes
    const mockArticles: NewsArticle[] = [
      {
        title: `${ticker} Reports Strong Quarterly Earnings`,
        description: `${ticker} exceeded analyst expectations with a record quarter, showing strength in new product lines.`,
        url: 'https://example.com/news/1',
        source: 'Financial Times',
        published_at: new Date().toISOString(),
        is_relevant: true
      },
      {
        title: `Analysts Upgrade ${ticker} Rating`,
        description: `Several leading analysts have upgraded their outlook for ${ticker}, citing strong growth potential.`,
        url: 'https://example.com/news/2',
        source: 'Bloomberg',
        published_at: new Date(Date.now() - 86400000).toISOString(), // Yesterday
        is_relevant: true
      },
      {
        title: `New Products Boost ${ticker} Market Share`,
        description: `${ticker}'s latest product launches have significantly increased its market share in key segments.`,
        url: 'https://example.com/news/3',
        source: 'CNBC',
        published_at: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
        is_relevant: true
      },
      {
        title: `${ticker} Announces Strategic Partnership`,
        description: `A new strategic partnership is expected to open new markets for ${ticker} in the coming year.`,
        url: 'https://example.com/news/4',
        source: 'Reuters',
        published_at: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
        is_relevant: true
      },
      {
        title: `Industry Outlook: What's Next for ${ticker}?`,
        description: `Industry experts weigh in on the future prospects for ${ticker} amid changing market conditions.`,
        url: 'https://example.com/news/5',
        source: 'Wall Street Journal',
        published_at: new Date(Date.now() - 345600000).toISOString(), // 4 days ago
        is_relevant: true
      }
    ];
    
    setNewsData({
      ticker,
      total_results: mockArticles.length,
      articles: mockArticles,
      sources: ['Financial Times', 'Bloomberg', 'CNBC', 'Reuters', 'Wall Street Journal'],
      keywords: ['earnings', 'growth', 'products', 'partnership', 'analysis'],
      date_range: {
        from: new Date(Date.now() - 604800000).toISOString().split('T')[0], // 7 days ago
        to: new Date().toISOString().split('T')[0] // Today
      }
    });
  };
  
  useEffect(() => {
    fetchNews(selectedTicker);
  }, [selectedTicker]);
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };
  
  return (
    <div className="h-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">News</h1>
          <p className="text-gray-400">Financial news and market insights</p>
        </div>
      </div>
      
      {/* Ticker selection */}
      <div className="bg-secondary-300 rounded-xl p-4 mb-6">
        <h2 className="text-lg font-medium text-white mb-3">Select Ticker</h2>
        <div className="flex flex-wrap gap-2">
          {popularTickers.map(ticker => (
            <button
              key={ticker}
              className={`px-4 py-2 rounded-md ${
                selectedTicker === ticker 
                  ? 'bg-primary-500 text-white' 
                  : 'bg-secondary-200 text-gray-300 hover:bg-secondary-100'
              }`}
              onClick={() => setSelectedTicker(ticker)}
            >
              {ticker}
            </button>
          ))}
        </div>
      </div>
      
      {/* News content */}
      {loading ? (
        <div className="bg-secondary-300 rounded-xl p-8 text-center">
          <div className="animate-pulse">
            <div className="h-4 bg-secondary-200 rounded w-3/4 mx-auto mb-3"></div>
            <div className="h-4 bg-secondary-200 rounded w-1/2 mx-auto"></div>
          </div>
        </div>
      ) : error ? (
        <div className="bg-secondary-300 rounded-xl p-8 text-center">
          <NewspaperIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h2 className="text-xl font-medium text-white mb-2">Couldn't load news</h2>
          <p className="text-gray-400 max-w-md mx-auto">{error}</p>
        </div>
      ) : newsData ? (
        <div>
          <div className="bg-secondary-300 rounded-xl p-6 mb-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-medium text-white">Recent News for {newsData.ticker}</h2>
              <span className="text-sm text-gray-400">
                {newsData.total_results} articles • {newsData.date_range.from} to {newsData.date_range.to}
              </span>
            </div>
            
            {/* Keywords */}
            {newsData.keywords && newsData.keywords.length > 0 && (
              <div className="mb-4">
                <p className="text-sm text-gray-400 mb-2">Trending Keywords:</p>
                <div className="flex flex-wrap gap-2">
                  {newsData.keywords.map((keyword, index) => (
                    <span 
                      key={index} 
                      className="bg-secondary-200 text-gray-300 px-2 py-1 rounded text-xs"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          {/* News articles */}
          <div className="space-y-4">
            {newsData.articles.map((article, index) => (
              <div key={index} className="bg-secondary-300 rounded-xl p-5 hover:bg-secondary-200 transition-colors">
                <div className="flex justify-between">
                  <span className="text-xs text-primary-400 font-medium">{article.source}</span>
                  <span className="text-xs text-gray-400">{formatDate(article.published_at)}</span>
                </div>
                <h3 className="text-lg font-medium text-white mt-2 mb-2">{article.title}</h3>
                <p className="text-gray-400 text-sm mb-3">{article.description}</p>
                <a 
                  href={article.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-primary-500 text-sm hover:underline"
                >
                  Read full article 
                  <ArrowTopRightOnSquareIcon className="h-4 w-4 ml-1" />
                </a>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="bg-secondary-300 rounded-xl p-8 text-center">
          <NewspaperIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h2 className="text-xl font-medium text-white mb-2">No news data available</h2>
          <p className="text-gray-400 max-w-md mx-auto">
            Select a ticker to view the latest news and market insights.
          </p>
        </div>
      )}
    </div>
  )
}

export default News 