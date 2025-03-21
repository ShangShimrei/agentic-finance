import React, { useState } from 'react'
import { ArrowUpIcon, ArrowDownIcon, StarIcon as StarIconSolid } from '@heroicons/react/24/solid'
import { StarIcon as StarIconOutline, MagnifyingGlassIcon } from '@heroicons/react/24/outline'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

// Market asset types and interfaces
type AssetType = 'crypto' | 'stock' | 'etf';
type TrendDirection = 'up' | 'down' | 'neutral';

interface MarketAsset {
  id: string;
  name: string;
  symbol: string;
  type: AssetType;
  price: number;
  change24h: number;
  volume24h: number;
  marketCap: number;
  sparklineData: {time: string, price: number}[];
  trend: TrendDirection;
}

interface MarketSection {
  id: string;
  title: string;
  assets: MarketAsset[];
}

interface MarketTrend {
  id: string;
  title: string;
  changePercentage: number;
  direction: TrendDirection;
  description: string;
}

const Market = () => {
  // State for market data
  const [searchQuery, setSearchQuery] = useState('');
  const [watchlist, setWatchlist] = useState<string[]>(['BTC', 'ETH', 'AAPL']);
  
  // Mock market trends data
  const marketTrends: MarketTrend[] = [
    {
      id: '1',
      title: 'Crypto Markets',
      changePercentage: 2.8,
      direction: 'up',
      description: 'Bitcoin leads market recovery as institutional interest grows'
    },
    {
      id: '2',
      title: 'Tech Stocks',
      changePercentage: -1.2,
      direction: 'down',
      description: 'Tech sector under pressure amid rising interest rates'
    },
    {
      id: '3',
      title: 'Energy Sector',
      changePercentage: 3.5,
      direction: 'up',
      description: 'Oil and gas companies rally on supply constraints'
    },
    {
      id: '4',
      title: 'Global Markets',
      changePercentage: 0.4,
      direction: 'up',
      description: 'Mixed signals in global markets amid geopolitical tensions'
    }
  ];
  
  // Mock market assets data
  const generateSparklineData = (trend: TrendDirection, volatility: number = 1) => {
    const data = [];
    let price = 100;
    for (let i = 0; i < 24; i++) {
      const hour = i.toString().padStart(2, '0') + ':00';
      
      // Generate price movement based on trend
      const randomChange = (Math.random() - (trend === 'down' ? 0.6 : trend === 'up' ? 0.4 : 0.5)) * volatility;
      price = price * (1 + randomChange / 100);
      
      data.push({
        time: hour,
        price: Math.max(1, price)
      });
    }
    return data;
  };
  
  const marketAssets: MarketAsset[] = [
    {
      id: '1',
      name: 'Bitcoin',
      symbol: 'BTC',
      type: 'crypto',
      price: 53248.42,
      change24h: 2.34,
      volume24h: 28500000000,
      marketCap: 1040000000000,
      sparklineData: generateSparklineData('up', 2),
      trend: 'up'
    },
    {
      id: '2',
      name: 'Ethereum',
      symbol: 'ETH',
      type: 'crypto',
      price: 2937.81,
      change24h: -1.21,
      volume24h: 15700000000,
      marketCap: 352000000000,
      sparklineData: generateSparklineData('down', 2.5),
      trend: 'down'
    },
    {
      id: '3',
      name: 'Apple Inc.',
      symbol: 'AAPL',
      type: 'stock',
      price: 178.72,
      change24h: 0.53,
      volume24h: 68900000,
      marketCap: 2800000000000,
      sparklineData: generateSparklineData('up', 0.8),
      trend: 'up'
    },
    {
      id: '4',
      name: 'Microsoft',
      symbol: 'MSFT',
      type: 'stock',
      price: 331.21,
      change24h: 1.05,
      volume24h: 24600000,
      marketCap: 2450000000000,
      sparklineData: generateSparklineData('up', 0.7),
      trend: 'up'
    },
    {
      id: '5',
      name: 'Tesla',
      symbol: 'TSLA',
      type: 'stock',
      price: 177.94,
      change24h: -2.67,
      volume24h: 137500000,
      marketCap: 560000000000,
      sparklineData: generateSparklineData('down', 3),
      trend: 'down'
    },
    {
      id: '6',
      name: 'Solana',
      symbol: 'SOL',
      type: 'crypto',
      price: 101.54,
      change24h: 5.76,
      volume24h: 2350000000,
      marketCap: 43700000000,
      sparklineData: generateSparklineData('up', 4),
      trend: 'up'
    },
    {
      id: '7',
      name: 'Amazon',
      symbol: 'AMZN',
      type: 'stock',
      price: 178.15,
      change24h: 0.21,
      volume24h: 41300000,
      marketCap: 1850000000000,
      sparklineData: generateSparklineData('neutral', 0.5),
      trend: 'neutral'
    },
    {
      id: '8',
      name: 'Cardano',
      symbol: 'ADA',
      type: 'crypto',
      price: 0.45,
      change24h: -0.89,
      volume24h: 410000000,
      marketCap: 15800000000,
      sparklineData: generateSparklineData('down', 1.8),
      trend: 'down'
    },
    {
      id: '9',
      name: 'Google',
      symbol: 'GOOGL',
      type: 'stock',
      price: 130.25,
      change24h: 0.78,
      volume24h: 26500000,
      marketCap: 1640000000000,
      sparklineData: generateSparklineData('up', 0.6),
      trend: 'up'
    },
    {
      id: '10',
      name: 'Polygon',
      symbol: 'MATIC',
      type: 'crypto',
      price: 0.56,
      change24h: -1.42,
      volume24h: 275000000,
      marketCap: 5300000000,
      sparklineData: generateSparklineData('down', 2.2),
      trend: 'down'
    },
    {
      id: '11',
      name: 'Ripple',
      symbol: 'XRP',
      type: 'crypto',
      price: 0.49,
      change24h: 1.24,
      volume24h: 960000000,
      marketCap: 26500000000,
      sparklineData: generateSparklineData('up', 1.9),
      trend: 'up'
    },
    {
      id: '12',
      name: 'Meta',
      symbol: 'META',
      type: 'stock',
      price: 472.85,
      change24h: -1.05,
      volume24h: 18700000,
      marketCap: 1210000000000,
      sparklineData: generateSparklineData('down', 1.1),
      trend: 'down'
    }
  ];
  
  // Group assets into market sections
  const marketSections: MarketSection[] = [
    {
      id: 'trending',
      title: 'Trending Assets',
      assets: marketAssets.slice(0, 6)
    },
    {
      id: 'gainers',
      title: 'Top Gainers',
      assets: [...marketAssets].sort((a, b) => b.change24h - a.change24h).slice(0, 5)
    },
    {
      id: 'losers',
      title: 'Top Losers',
      assets: [...marketAssets].sort((a, b) => a.change24h - b.change24h).slice(0, 5)
    }
  ];
  
  // Filtered market assets based on search
  const filteredAssets = marketAssets.filter(asset => 
    asset.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    asset.symbol.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  // Toggle asset in watchlist
  const toggleWatchlist = (symbol: string) => {
    if (watchlist.includes(symbol)) {
      setWatchlist(watchlist.filter(item => item !== symbol));
    } else {
      setWatchlist([...watchlist, symbol]);
    }
  };
  
  // Format large numbers for display
  const formatLargeNumber = (num: number) => {
    if (num >= 1000000000) {
      return `$${(num / 1000000000).toFixed(1)}B`;
    } else if (num >= 1000000) {
      return `$${(num / 1000000).toFixed(1)}M`;
    } else {
      return `$${num.toLocaleString()}`;
    }
  };
  
  // Custom tooltip for sparkline chart
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-secondary-200 p-2 rounded shadow-md text-xs">
          <p className="text-white">{`Time: ${payload[0].payload.time}`}</p>
          <p className="text-white">{`Price: $${payload[0].value.toFixed(2)}`}</p>
        </div>
      );
    }
    return null;
  };
  
  return (
    <div className="h-full">
      {/* Market header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Market</h1>
          <p className="text-gray-400">Real-time market data and trends</p>
        </div>
        
        {/* Search bar */}
        <div className="mt-4 md:mt-0 w-full md:w-auto md:min-w-[300px]">
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input 
              type="text" 
              placeholder="Search assets..." 
              className="w-full bg-secondary-300 rounded-md pl-10 pr-4 py-2 text-gray-300 outline-none"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>
      </div>
      
      {/* Market Trends */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">Market Trends</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {marketTrends.map(trend => (
            <div key={trend.id} className="bg-secondary-300 rounded-xl p-5">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-medium text-white">{trend.title}</h3>
                <div className={`flex items-center ${trend.direction === 'up' ? 'text-green-500' : trend.direction === 'down' ? 'text-red-500' : 'text-gray-400'}`}>
                  {trend.direction === 'up' ? (
                    <ArrowUpIcon className="w-4 h-4 mr-1" />
                  ) : trend.direction === 'down' ? (
                    <ArrowDownIcon className="w-4 h-4 mr-1" />
                  ) : null}
                  <span className="font-medium">{Math.abs(trend.changePercentage)}%</span>
                </div>
              </div>
              <p className="text-gray-400 text-sm">{trend.description}</p>
            </div>
          ))}
        </div>
      </div>
      
      {/* Search Results */}
      {searchQuery && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">Search Results</h2>
          {filteredAssets.length > 0 ? (
            <div className="bg-secondary-300 rounded-xl overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-secondary-200">
                    <th className="text-left py-4 px-6 text-gray-400 font-medium">Asset</th>
                    <th className="text-right py-4 px-6 text-gray-400 font-medium">Price</th>
                    <th className="text-right py-4 px-6 text-gray-400 font-medium">24h Change</th>
                    <th className="text-right py-4 px-6 text-gray-400 font-medium">24h Volume</th>
                    <th className="text-right py-4 px-6 text-gray-400 font-medium">Market Cap</th>
                    <th className="text-right py-4 px-6 text-gray-400 font-medium">Chart</th>
                    <th className="text-center py-4 px-6 text-gray-400 font-medium">Watch</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredAssets.map(asset => (
                    <tr key={asset.id} className="border-b border-secondary-200 hover:bg-secondary-200 transition-colors">
                      <td className="py-4 px-6">
                        <div className="flex items-center">
                          <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center mr-3 text-sm">
                            {asset.symbol.substring(0, 1)}
                          </div>
                          <div>
                            <div className="font-medium text-white">{asset.name}</div>
                            <div className="text-gray-400 text-sm">{asset.symbol}</div>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-6 text-right font-medium text-white">
                        ${asset.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </td>
                      <td className={`py-4 px-6 text-right font-medium ${asset.change24h >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                        <div className="flex items-center justify-end">
                          {asset.change24h >= 0 ? <ArrowUpIcon className="w-3 h-3 mr-1" /> : <ArrowDownIcon className="w-3 h-3 mr-1" />}
                          {Math.abs(asset.change24h)}%
                        </div>
                      </td>
                      <td className="py-4 px-6 text-right font-medium text-white">
                        {formatLargeNumber(asset.volume24h)}
                      </td>
                      <td className="py-4 px-6 text-right font-medium text-white">
                        {formatLargeNumber(asset.marketCap)}
                      </td>
                      <td className="py-4 px-6">
                        <div className="w-24 h-12">
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={asset.sparklineData}>
                              <Line 
                                type="monotone" 
                                dataKey="price" 
                                stroke={asset.trend === 'up' ? '#10B981' : asset.trend === 'down' ? '#EF4444' : '#6B7280'} 
                                dot={false}
                                strokeWidth={2}
                              />
                              <Tooltip content={<CustomTooltip />} />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      </td>
                      <td className="py-4 px-6 text-center">
                        <button 
                          onClick={() => toggleWatchlist(asset.symbol)}
                          className="focus:outline-none"
                        >
                          {watchlist.includes(asset.symbol) ? (
                            <StarIconSolid className="w-6 h-6 text-yellow-500" />
                          ) : (
                            <StarIconOutline className="w-6 h-6 text-gray-400 hover:text-yellow-500" />
                          )}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="bg-secondary-300 rounded-xl p-8 text-center">
              <p className="text-gray-400">No assets found matching "{searchQuery}"</p>
            </div>
          )}
        </div>
      )}
      
      {/* Market Sections */}
      {!searchQuery && marketSections.map(section => (
        <div key={section.id} className="mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">{section.title}</h2>
          <div className="bg-secondary-300 rounded-xl overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-secondary-200">
                  <th className="text-left py-4 px-6 text-gray-400 font-medium">Asset</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium">Price</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium">24h Change</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium hidden md:table-cell">24h Volume</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium hidden lg:table-cell">Market Cap</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium">Chart</th>
                  <th className="text-center py-4 px-6 text-gray-400 font-medium">Watch</th>
                </tr>
              </thead>
              <tbody>
                {section.assets.map(asset => (
                  <tr key={asset.id} className="border-b border-secondary-200 hover:bg-secondary-200 transition-colors">
                    <td className="py-4 px-6">
                      <div className="flex items-center">
                        <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center mr-3 text-sm">
                          {asset.symbol.substring(0, 1)}
                        </div>
                        <div>
                          <div className="font-medium text-white">{asset.name}</div>
                          <div className="text-gray-400 text-sm">{asset.symbol}</div>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-6 text-right font-medium text-white">
                      ${asset.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className={`py-4 px-6 text-right font-medium ${asset.change24h >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                      <div className="flex items-center justify-end">
                        {asset.change24h >= 0 ? <ArrowUpIcon className="w-3 h-3 mr-1" /> : <ArrowDownIcon className="w-3 h-3 mr-1" />}
                        {Math.abs(asset.change24h)}%
                      </div>
                    </td>
                    <td className="py-4 px-6 text-right font-medium text-white hidden md:table-cell">
                      {formatLargeNumber(asset.volume24h)}
                    </td>
                    <td className="py-4 px-6 text-right font-medium text-white hidden lg:table-cell">
                      {formatLargeNumber(asset.marketCap)}
                    </td>
                    <td className="py-4 px-6">
                      <div className="w-24 h-12">
                        <ResponsiveContainer width="100%" height="100%">
                          <LineChart data={asset.sparklineData}>
                            <Line 
                              type="monotone" 
                              dataKey="price" 
                              stroke={asset.trend === 'up' ? '#10B981' : asset.trend === 'down' ? '#EF4444' : '#6B7280'} 
                              dot={false}
                              strokeWidth={2}
                            />
                            <Tooltip content={<CustomTooltip />} />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                    </td>
                    <td className="py-4 px-6 text-center">
                      <button 
                        onClick={() => toggleWatchlist(asset.symbol)}
                        className="focus:outline-none"
                      >
                        {watchlist.includes(asset.symbol) ? (
                          <StarIconSolid className="w-6 h-6 text-yellow-500" />
                        ) : (
                          <StarIconOutline className="w-6 h-6 text-gray-400 hover:text-yellow-500" />
                        )}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
      
      {/* Watchlist */}
      {!searchQuery && watchlist.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">Your Watchlist</h2>
          <div className="bg-secondary-300 rounded-xl overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-secondary-200">
                  <th className="text-left py-4 px-6 text-gray-400 font-medium">Asset</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium">Price</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium">24h Change</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium hidden md:table-cell">24h Volume</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium hidden lg:table-cell">Market Cap</th>
                  <th className="text-right py-4 px-6 text-gray-400 font-medium">Chart</th>
                  <th className="text-center py-4 px-6 text-gray-400 font-medium">Watch</th>
                </tr>
              </thead>
              <tbody>
                {marketAssets
                  .filter(asset => watchlist.includes(asset.symbol))
                  .map(asset => (
                    <tr key={asset.id} className="border-b border-secondary-200 hover:bg-secondary-200 transition-colors">
                      <td className="py-4 px-6">
                        <div className="flex items-center">
                          <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center mr-3 text-sm">
                            {asset.symbol.substring(0, 1)}
                          </div>
                          <div>
                            <div className="font-medium text-white">{asset.name}</div>
                            <div className="text-gray-400 text-sm">{asset.symbol}</div>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-6 text-right font-medium text-white">
                        ${asset.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </td>
                      <td className={`py-4 px-6 text-right font-medium ${asset.change24h >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                        <div className="flex items-center justify-end">
                          {asset.change24h >= 0 ? <ArrowUpIcon className="w-3 h-3 mr-1" /> : <ArrowDownIcon className="w-3 h-3 mr-1" />}
                          {Math.abs(asset.change24h)}%
                        </div>
                      </td>
                      <td className="py-4 px-6 text-right font-medium text-white hidden md:table-cell">
                        {formatLargeNumber(asset.volume24h)}
                      </td>
                      <td className="py-4 px-6 text-right font-medium text-white hidden lg:table-cell">
                        {formatLargeNumber(asset.marketCap)}
                      </td>
                      <td className="py-4 px-6">
                        <div className="w-24 h-12">
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={asset.sparklineData}>
                              <Line 
                                type="monotone" 
                                dataKey="price" 
                                stroke={asset.trend === 'up' ? '#10B981' : asset.trend === 'down' ? '#EF4444' : '#6B7280'} 
                                dot={false}
                                strokeWidth={2}
                              />
                              <Tooltip content={<CustomTooltip />} />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      </td>
                      <td className="py-4 px-6 text-center">
                        <button 
                          onClick={() => toggleWatchlist(asset.symbol)}
                          className="focus:outline-none"
                        >
                          <StarIconSolid className="w-6 h-6 text-yellow-500" />
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default Market 