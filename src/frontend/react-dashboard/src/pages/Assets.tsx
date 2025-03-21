import React, { useState } from 'react'
import { CurrencyDollarIcon, ArrowUpIcon, ArrowDownIcon, PlusIcon } from '@heroicons/react/24/solid'
import { MagnifyingGlassIcon, FunnelIcon, ArrowsUpDownIcon } from '@heroicons/react/24/outline'

// Asset types
type AssetType = 'crypto' | 'stock' | 'etf' | 'all';

// Asset category for filtering
type AssetCategory = {
  id: AssetType;
  name: string;
  count: number;
}

// Asset data structure
interface Asset {
  id: string;
  name: string;
  symbol: string;
  type: AssetType;
  price: number;
  change24h: number;
  holdings: number;
  value: number;
  allTimeReturn: number;
  icon: string;
}

const Assets = () => {
  // State for search and filtering
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<AssetType>('all');
  const [sortField, setSortField] = useState<keyof Asset>('value');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  // Asset categories for filtering
  const categories: AssetCategory[] = [
    { id: 'all', name: 'All Assets', count: 12 },
    { id: 'crypto', name: 'Crypto', count: 5 },
    { id: 'stock', name: 'Stocks', count: 5 },
    { id: 'etf', name: 'ETFs', count: 2 },
  ];

  // Mock assets data
  const assets: Asset[] = [
    {
      id: '1',
      name: 'Bitcoin',
      symbol: 'BTC',
      type: 'crypto',
      price: 53248.42,
      change24h: 2.34,
      holdings: 0.45,
      value: 23961.79,
      allTimeReturn: 112.5,
      icon: '₿'
    },
    {
      id: '2',
      name: 'Ethereum',
      symbol: 'ETH',
      type: 'crypto',
      price: 2937.81,
      change24h: -1.21,
      holdings: 3.2,
      value: 9401.00,
      allTimeReturn: 85.3,
      icon: 'Ξ'
    },
    {
      id: '3',
      name: 'Apple Inc.',
      symbol: 'AAPL',
      type: 'stock',
      price: 178.72,
      change24h: 0.53,
      holdings: 25,
      value: 4468.00,
      allTimeReturn: 32.1,
      icon: ''
    },
    {
      id: '4',
      name: 'Microsoft',
      symbol: 'MSFT',
      type: 'stock',
      price: 331.21,
      change24h: 1.05,
      holdings: 10,
      value: 3312.10,
      allTimeReturn: 45.7,
      icon: ''
    },
    {
      id: '5',
      name: 'Tesla',
      symbol: 'TSLA',
      type: 'stock',
      price: 177.94,
      change24h: -2.67,
      holdings: 15,
      value: 2669.10,
      allTimeReturn: -5.2,
      icon: ''
    },
    {
      id: '6',
      name: 'Solana',
      symbol: 'SOL',
      type: 'crypto',
      price: 101.54,
      change24h: 5.76,
      holdings: 25,
      value: 2538.50,
      allTimeReturn: 132.8,
      icon: 'SOL'
    },
    {
      id: '7',
      name: 'Amazon',
      symbol: 'AMZN',
      type: 'stock',
      price: 178.15,
      change24h: 0.21,
      holdings: 12,
      value: 2137.80,
      allTimeReturn: 28.6,
      icon: ''
    },
    {
      id: '8',
      name: 'Cardano',
      symbol: 'ADA',
      type: 'crypto',
      price: 0.45,
      change24h: -0.89,
      holdings: 4500,
      value: 2025.00,
      allTimeReturn: 12.4,
      icon: 'ADA'
    },
    {
      id: '9',
      name: 'Google',
      symbol: 'GOOGL',
      type: 'stock',
      price: 130.25,
      change24h: 0.78,
      holdings: 15,
      value: 1953.75,
      allTimeReturn: 21.9,
      icon: ''
    },
    {
      id: '10',
      name: 'Polygon',
      symbol: 'MATIC',
      type: 'crypto',
      price: 0.56,
      change24h: -1.42,
      holdings: 3200,
      value: 1792.00,
      allTimeReturn: 45.2,
      icon: 'MATIC'
    },
    {
      id: '11',
      name: 'Vanguard S&P 500 ETF',
      symbol: 'VOO',
      type: 'etf',
      price: 412.75,
      change24h: 0.65,
      holdings: 4,
      value: 1651.00,
      allTimeReturn: 18.5,
      icon: ''
    },
    {
      id: '12',
      name: 'Invesco QQQ Trust',
      symbol: 'QQQ',
      type: 'etf',
      price: 386.92,
      change24h: 0.72,
      holdings: 3,
      value: 1160.76,
      allTimeReturn: 22.1,
      icon: ''
    },
  ];

  // Filter assets based on selected category and search query
  const filteredAssets = assets.filter(asset => {
    const matchesCategory = selectedCategory === 'all' || asset.type === selectedCategory;
    const matchesSearch = asset.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         asset.symbol.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  // Sort assets based on sort field and direction
  const sortedAssets = [...filteredAssets].sort((a, b) => {
    if (sortDirection === 'asc') {
      return a[sortField] > b[sortField] ? 1 : -1;
    } else {
      return a[sortField] < b[sortField] ? 1 : -1;
    }
  });

  // Calculate total portfolio value
  const totalValue = assets.reduce((sum, asset) => sum + asset.value, 0);

  // Handle sort button click
  const handleSort = (field: keyof Asset) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  return (
    <div className="h-full">
      {/* Assets Overview */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Assets</h1>
          <p className="text-gray-400">Manage and track your crypto and stock holdings</p>
        </div>
        <button className="btn-primary flex items-center gap-2">
          <PlusIcon className="w-5 h-5" />
          Add Asset
        </button>
      </div>
      
      {/* Asset Value Summary */}
      <div className="bg-secondary-300 rounded-xl p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h2 className="text-lg font-medium text-gray-400">Total Value</h2>
            <div className="flex items-end gap-2 mt-1">
              <span className="text-3xl font-bold text-white">${totalValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              <span className="text-green-500 font-medium text-sm flex items-center mb-1">
                <ArrowUpIcon className="w-3 h-3 mr-1" />
                24.5%
              </span>
            </div>
          </div>
          
          <div className="flex gap-4 justify-end">
            <div className="text-center">
              <div className="text-gray-400 text-sm">Crypto</div>
              <div className="text-xl font-bold text-white mt-1">${sortedAssets.filter(a => a.type === 'crypto').reduce((sum, asset) => sum + asset.value, 0).toLocaleString('en-US', { maximumFractionDigits: 0 })}</div>
            </div>
            <div className="text-center">
              <div className="text-gray-400 text-sm">Stocks</div>
              <div className="text-xl font-bold text-white mt-1">${sortedAssets.filter(a => a.type === 'stock').reduce((sum, asset) => sum + asset.value, 0).toLocaleString('en-US', { maximumFractionDigits: 0 })}</div>
            </div>
            <div className="text-center">
              <div className="text-gray-400 text-sm">ETFs</div>
              <div className="text-xl font-bold text-white mt-1">${sortedAssets.filter(a => a.type === 'etf').reduce((sum, asset) => sum + asset.value, 0).toLocaleString('en-US', { maximumFractionDigits: 0 })}</div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Filters and Search */}
      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <div className="flex bg-secondary-300 rounded-md px-3 py-2 flex-1">
          <MagnifyingGlassIcon className="w-5 h-5 text-gray-400 mr-2" />
          <input 
            type="text" 
            placeholder="Search assets by name or symbol" 
            className="bg-transparent border-none outline-none text-gray-300 w-full"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        <div className="flex items-center bg-secondary-300 rounded-md px-3 py-2">
          <FunnelIcon className="w-5 h-5 text-gray-400 mr-2" />
          <select 
            className="bg-transparent border-none outline-none text-gray-300 pr-8"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value as AssetType)}
          >
            {categories.map(category => (
              <option key={category.id} value={category.id} className="bg-secondary-300">
                {category.name} ({category.count})
              </option>
            ))}
          </select>
        </div>
      </div>
      
      {/* Assets Table */}
      <div className="bg-secondary-300 rounded-xl overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-secondary-200">
              <th className="text-left py-4 px-6 text-gray-400 font-medium">Asset</th>
              <th 
                className="text-right py-4 px-6 text-gray-400 font-medium cursor-pointer"
                onClick={() => handleSort('price')}
              >
                <div className="flex items-center justify-end">
                  Price
                  {sortField === 'price' && (
                    <ArrowsUpDownIcon className={`w-4 h-4 ml-1 ${sortDirection === 'asc' ? 'rotate-180' : ''}`} />
                  )}
                </div>
              </th>
              <th 
                className="text-right py-4 px-6 text-gray-400 font-medium cursor-pointer"
                onClick={() => handleSort('change24h')}
              >
                <div className="flex items-center justify-end">
                  24h Change
                  {sortField === 'change24h' && (
                    <ArrowsUpDownIcon className={`w-4 h-4 ml-1 ${sortDirection === 'asc' ? 'rotate-180' : ''}`} />
                  )}
                </div>
              </th>
              <th 
                className="text-right py-4 px-6 text-gray-400 font-medium cursor-pointer"
                onClick={() => handleSort('holdings')}
              >
                <div className="flex items-center justify-end">
                  Holdings
                  {sortField === 'holdings' && (
                    <ArrowsUpDownIcon className={`w-4 h-4 ml-1 ${sortDirection === 'asc' ? 'rotate-180' : ''}`} />
                  )}
                </div>
              </th>
              <th 
                className="text-right py-4 px-6 text-gray-400 font-medium cursor-pointer"
                onClick={() => handleSort('value')}
              >
                <div className="flex items-center justify-end">
                  Value
                  {sortField === 'value' && (
                    <ArrowsUpDownIcon className={`w-4 h-4 ml-1 ${sortDirection === 'asc' ? 'rotate-180' : ''}`} />
                  )}
                </div>
              </th>
              <th 
                className="text-right py-4 px-6 text-gray-400 font-medium cursor-pointer"
                onClick={() => handleSort('allTimeReturn')}
              >
                <div className="flex items-center justify-end">
                  All-Time Return
                  {sortField === 'allTimeReturn' && (
                    <ArrowsUpDownIcon className={`w-4 h-4 ml-1 ${sortDirection === 'asc' ? 'rotate-180' : ''}`} />
                  )}
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedAssets.map(asset => (
              <tr key={asset.id} className="border-b border-secondary-200 hover:bg-secondary-200 transition-colors">
                <td className="py-4 px-6">
                  <div className="flex items-center">
                    <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center mr-3 text-sm">
                      {asset.icon || asset.symbol.substring(0, 1)}
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
                  {asset.holdings.toLocaleString('en-US', { maximumFractionDigits: asset.type === 'crypto' ? 8 : 2 })} {asset.symbol}
                </td>
                <td className="py-4 px-6 text-right font-medium text-white">
                  ${asset.value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </td>
                <td className={`py-4 px-6 text-right font-medium ${asset.allTimeReturn >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  <div className="flex items-center justify-end">
                    {asset.allTimeReturn >= 0 ? <ArrowUpIcon className="w-3 h-3 mr-1" /> : <ArrowDownIcon className="w-3 h-3 mr-1" />}
                    {Math.abs(asset.allTimeReturn)}%
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Assets 