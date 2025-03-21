import React, { useState } from 'react'
import { 
  ArrowUpIcon, 
  ArrowDownIcon, 
  PlusIcon, 
  AdjustmentsHorizontalIcon,
  ArrowPathIcon
} from '@heroicons/react/24/solid'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'

// Asset types
type AssetType = 'crypto' | 'stock' | 'etf' | 'cash';

// Portfolio asset structure
interface PortfolioAsset {
  id: string;
  name: string;
  symbol: string;
  type: AssetType;
  allocation: number;  // percentage of portfolio
  value: number;       // actual value in $
  returnsYTD: number;  // percentage
  returnsAllTime: number; // percentage
  color: string;
}

// Performance metric structure
interface PerformanceMetric {
  id: string;
  name: string;
  value: string;
  change: number;
  description: string;
}

const Portfolio = () => {
  // State
  const [timeFrame, setTimeFrame] = useState<'1W' | '1M' | '3M' | 'YTD' | '1Y' | 'ALL'>('1M');
  
  // Mock portfolio data
  const portfolioAssets: PortfolioAsset[] = [
    {
      id: '1',
      name: 'Bitcoin',
      symbol: 'BTC',
      type: 'crypto',
      allocation: 32.5,
      value: 23961.79,
      returnsYTD: 21.5,
      returnsAllTime: 112.5,
      color: '#F7931A'
    },
    {
      id: '2',
      name: 'Ethereum',
      symbol: 'ETH',
      type: 'crypto',
      allocation: 12.8,
      value: 9401.00,
      returnsYTD: 15.8,
      returnsAllTime: 85.3,
      color: '#627EEA'
    },
    {
      id: '3',
      name: 'Apple Inc.',
      symbol: 'AAPL',
      type: 'stock',
      allocation: 6.1,
      value: 4468.00,
      returnsYTD: 8.3,
      returnsAllTime: 32.1,
      color: '#A3AAAE'
    },
    {
      id: '4',
      name: 'Microsoft',
      symbol: 'MSFT',
      type: 'stock',
      allocation: 4.5,
      value: 3312.10,
      returnsYTD: 11.2,
      returnsAllTime: 45.7,
      color: '#00A4EF'
    },
    {
      id: '5',
      name: 'Tesla',
      symbol: 'TSLA',
      type: 'stock',
      allocation: 3.6,
      value: 2669.10,
      returnsYTD: -12.4,
      returnsAllTime: -5.2,
      color: '#E31937'
    },
    {
      id: '6',
      name: 'Solana',
      symbol: 'SOL',
      type: 'crypto',
      allocation: 3.5,
      value: 2538.50,
      returnsYTD: 67.2,
      returnsAllTime: 132.8,
      color: '#00FFA3'
    },
    {
      id: '7',
      name: 'Other Assets',
      symbol: 'OTHER',
      type: 'stock',
      allocation: 31.3,
      value: 23113.09,
      returnsYTD: 7.8,
      returnsAllTime: 42.5,
      color: '#6B7280'
    },
    {
      id: '8',
      name: 'Cash',
      symbol: 'USD',
      type: 'cash',
      allocation: 5.7,
      value: 4200.00,
      returnsYTD: 0,
      returnsAllTime: 0,
      color: '#22C55E'
    },
  ];

  // Calculate total portfolio value
  const totalPortfolioValue = portfolioAssets.reduce((sum, asset) => sum + asset.value, 0);
  
  // Group assets by type
  const assetsByType = portfolioAssets.reduce((acc, asset) => {
    if (!acc[asset.type]) {
      acc[asset.type] = {
        value: 0,
        allocation: 0,
        color: asset.type === 'crypto' ? '#F7931A' : 
               asset.type === 'stock' ? '#00A4EF' : 
               asset.type === 'etf' ? '#E31937' : '#22C55E'
      };
    }
    acc[asset.type].value += asset.value;
    acc[asset.type].allocation += asset.allocation;
    return acc;
  }, {} as Record<AssetType, { value: number, allocation: number, color: string }>);
  
  // Format allocation data for pie chart
  const assetAllocationData = Object.entries(assetsByType).map(([type, data]) => ({
    name: type.charAt(0).toUpperCase() + type.slice(1),
    value: data.value,
    allocation: data.allocation,
    color: data.color
  }));
  
  // Performance metrics
  const performanceMetrics: PerformanceMetric[] = [
    {
      id: '1',
      name: 'Total Value',
      value: `$${totalPortfolioValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      change: 18.3,
      description: 'Current portfolio market value'
    },
    {
      id: '2',
      name: 'Total Returns',
      value: `$${(totalPortfolioValue * 0.42).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      change: 42.0,
      description: 'All-time profit/loss'
    },
    {
      id: '3',
      name: 'YTD Returns',
      value: `$${(totalPortfolioValue * 0.167).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      change: 16.7,
      description: 'Year-to-date profit/loss'
    },
    {
      id: '4',
      name: 'Annualized Return',
      value: '21.3%',
      change: 21.3,
      description: 'Average yearly return'
    }
  ];
  
  // Custom tooltip for pie chart
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-secondary-200 p-3 rounded-md shadow-md">
          <p className="text-white font-medium">{payload[0].name}</p>
          <p className="text-gray-300">
            ${payload[0].value.toLocaleString('en-US', { maximumFractionDigits: 0 })}
          </p>
          <p className="text-gray-300">
            {payload[0].payload.allocation.toFixed(1)}% of portfolio
          </p>
        </div>
      );
    }
    return null;
  };
  
  // Time frame buttons
  const timeFrameOptions = [
    { id: '1W', label: '1W' },
    { id: '1M', label: '1M' },
    { id: '3M', label: '3M' },
    { id: 'YTD', label: 'YTD' },
    { id: '1Y', label: '1Y' },
    { id: 'ALL', label: 'ALL' },
  ];
  
  return (
    <div className="h-full">
      {/* Portfolio header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Portfolio</h1>
          <p className="text-gray-400">Manage and track your investment portfolio</p>
        </div>
        <div className="flex gap-3">
          <button className="btn-secondary flex items-center gap-2">
            <ArrowPathIcon className="w-5 h-5" />
            Rebalance
          </button>
          <button className="btn-primary flex items-center gap-2">
            <PlusIcon className="w-5 h-5" />
            Add Funds
          </button>
        </div>
      </div>
      
      {/* Performance metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {performanceMetrics.map(metric => (
          <div key={metric.id} className="bg-secondary-300 rounded-xl p-5">
            <div className="flex justify-between items-start">
              <h3 className="text-gray-400 font-medium">{metric.name}</h3>
              <div className={`flex items-center ${metric.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                {metric.change >= 0 ? (
                  <ArrowUpIcon className="w-4 h-4 mr-1" />
                ) : (
                  <ArrowDownIcon className="w-4 h-4 mr-1" />
                )}
                <span className="font-medium">{Math.abs(metric.change)}%</span>
              </div>
            </div>
            <div className="mt-2">
              <div className="text-2xl font-bold text-white">{metric.value}</div>
              <div className="text-xs text-gray-400 mt-1">{metric.description}</div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Portfolio overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Asset allocation */}
        <div className="bg-secondary-300 rounded-xl p-6 lg:col-span-1">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-white">Asset Allocation</h2>
            <button className="text-gray-400 hover:text-white">
              <AdjustmentsHorizontalIcon className="w-5 h-5" />
            </button>
          </div>
          
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={assetAllocationData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  innerRadius={40}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {assetAllocationData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          
          <div className="grid grid-cols-2 gap-2 mt-4">
            {assetAllocationData.map((type, index) => (
              <div key={index} className="flex items-center">
                <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: type.color }}></div>
                <div className="text-sm text-gray-300">{type.name} ({type.allocation.toFixed(1)}%)</div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Performance chart */}
        <div className="bg-secondary-300 rounded-xl p-6 lg:col-span-2">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-white">Portfolio Performance</h2>
            <div className="flex bg-secondary-200 rounded-md">
              {timeFrameOptions.map(option => (
                <button
                  key={option.id}
                  className={`px-3 py-1 text-sm ${timeFrame === option.id ? 'bg-primary-500 text-white rounded-md' : 'text-gray-400'}`}
                  onClick={() => setTimeFrame(option.id as any)}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
          
          <div className="h-64 flex items-center justify-center">
            <p className="text-gray-400">Performance chart for {timeFrame} time frame</p>
            {/* Replace with actual chart component */}
          </div>
        </div>
      </div>
      
      {/* Portfolio assets */}
      <div className="bg-secondary-300 rounded-xl overflow-hidden">
        <div className="flex justify-between items-center px-6 py-4 border-b border-secondary-200">
          <h2 className="text-lg font-medium text-white">Your Assets</h2>
          <div className="flex gap-2">
            <select className="bg-secondary-200 text-gray-300 px-3 py-1 rounded-md border-none outline-none">
              <option value="allocation">Sort by Allocation</option>
              <option value="value">Sort by Value</option>
              <option value="performance">Sort by Performance</option>
            </select>
          </div>
        </div>
        
        <table className="w-full">
          <thead>
            <tr className="border-b border-secondary-200">
              <th className="text-left py-4 px-6 text-gray-400 font-medium">Asset</th>
              <th className="text-right py-4 px-6 text-gray-400 font-medium">Price</th>
              <th className="text-right py-4 px-6 text-gray-400 font-medium">Holdings</th>
              <th className="text-right py-4 px-6 text-gray-400 font-medium">Value</th>
              <th className="text-right py-4 px-6 text-gray-400 font-medium">Allocation</th>
              <th className="text-right py-4 px-6 text-gray-400 font-medium">YTD Return</th>
              <th className="text-right py-4 px-6 text-gray-400 font-medium">All-Time Return</th>
            </tr>
          </thead>
          <tbody>
            {portfolioAssets.map(asset => (
              <tr key={asset.id} className="border-b border-secondary-200 hover:bg-secondary-200 transition-colors">
                <td className="py-4 px-6">
                  <div className="flex items-center">
                    <div className="w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm" style={{ backgroundColor: asset.color }}>
                      {asset.symbol.substring(0, 1)}
                    </div>
                    <div>
                      <div className="font-medium text-white">{asset.name}</div>
                      <div className="text-gray-400 text-sm">{asset.symbol}</div>
                    </div>
                  </div>
                </td>
                <td className="py-4 px-6 text-right font-medium text-white">
                  {asset.type === 'cash' ? '-' : `$${(asset.value / (asset.type === 'crypto' ? 0.45 : 25)).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
                </td>
                <td className="py-4 px-6 text-right font-medium text-white">
                  {asset.type === 'cash' ? `$${asset.value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : (asset.type === 'crypto' ? '0.45' : '25')}
                </td>
                <td className="py-4 px-6 text-right font-medium text-white">
                  ${asset.value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </td>
                <td className="py-4 px-6 text-right">
                  <div className="w-full bg-secondary-200 rounded-full h-2.5 mb-1">
                    <div className="h-2.5 rounded-full" style={{ width: `${asset.allocation}%`, backgroundColor: asset.color }}></div>
                  </div>
                  <div className="text-sm text-gray-300 text-right">{asset.allocation.toFixed(1)}%</div>
                </td>
                <td className={`py-4 px-6 text-right font-medium ${asset.returnsYTD >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  <div className="flex items-center justify-end">
                    {asset.returnsYTD !== 0 && (
                      <>
                        {asset.returnsYTD > 0 ? <ArrowUpIcon className="w-3 h-3 mr-1" /> : <ArrowDownIcon className="w-3 h-3 mr-1" />}
                        {Math.abs(asset.returnsYTD)}%
                      </>
                    )}
                    {asset.returnsYTD === 0 && '-'}
                  </div>
                </td>
                <td className={`py-4 px-6 text-right font-medium ${asset.returnsAllTime >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  <div className="flex items-center justify-end">
                    {asset.returnsAllTime !== 0 && (
                      <>
                        {asset.returnsAllTime > 0 ? <ArrowUpIcon className="w-3 h-3 mr-1" /> : <ArrowDownIcon className="w-3 h-3 mr-1" />}
                        {Math.abs(asset.returnsAllTime)}%
                      </>
                    )}
                    {asset.returnsAllTime === 0 && '-'}
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

export default Portfolio 