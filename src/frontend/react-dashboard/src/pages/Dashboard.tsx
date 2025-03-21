import { useState, useEffect } from 'react'
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/solid'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  BarElement
} from 'chart.js'
import 'chartjs-chart-financial'
import { Chart } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

// Mock data for different time periods
const portfolioTimeData = {
  '1S': {
    labels: Array.from({ length: 60 }, (_, i) => `${i}s`),
    data: Array.from({ length: 60 }, (_, i) => 164802 + Math.random() * 50 - 25),
    candles: Array.from({ length: 60 }, (_, i) => ({
      x: i,
      o: 164802 + Math.random() * 20 - 10,
      h: 164802 + Math.random() * 30,
      l: 164802 - Math.random() * 30,
      c: 164802 + Math.random() * 20 - 10
    }))
  },
  '1M': {
    labels: Array.from({ length: 60 }, (_, i) => `${i}m`),
    data: Array.from({ length: 60 }, (_, i) => 164500 + Math.random() * 500 - 250),
    candles: Array.from({ length: 60 }, (_, i) => ({
      x: i,
      o: 164500 + Math.random() * 200 - 100,
      h: 164800 + Math.random() * 100,
      l: 164200 - Math.random() * 100,
      c: 164500 + Math.random() * 200 - 100
    }))
  },
  '15M': {
    labels: Array.from({ length: 12 }, (_, i) => `${i*15}m`),
    data: Array.from({ length: 12 }, (_, i) => 164000 + i * 100 + Math.random() * 200 - 100),
    candles: Array.from({ length: 12 }, (_, i) => ({
      x: i,
      o: 164000 + i * 90 + Math.random() * 50 - 25,
      h: 164000 + i * 110 + Math.random() * 100,
      l: 164000 + i * 70 - Math.random() * 100,
      c: 164000 + i * 100 + Math.random() * 50 - 25
    }))
  },
  '1H': {
    labels: ['9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM'],
    data: [163800, 164100, 163900, 164200, 164500, 164300, 164600, 164802],
    candles: [
      { x: 0, o: 163700, h: 163900, l: 163600, c: 163800 },
      { x: 1, o: 163800, h: 164200, l: 163800, c: 164100 },
      { x: 2, o: 164100, h: 164150, l: 163850, c: 163900 },
      { x: 3, o: 163900, h: 164300, l: 163900, c: 164200 },
      { x: 4, o: 164200, h: 164600, l: 164200, c: 164500 },
      { x: 5, o: 164500, h: 164550, l: 164250, c: 164300 },
      { x: 6, o: 164300, h: 164700, l: 164300, c: 164600 },
      { x: 7, o: 164600, h: 164900, l: 164600, c: 164802 }
    ]
  },
  daily: {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    data: [161400, 162300, 161800, 163100, 163700, 164300, 164802],
    candles: [
      { x: 0, o: 161200, h: 161700, l: 161000, c: 161400 },
      { x: 1, o: 161400, h: 162500, l: 161300, c: 162300 },
      { x: 2, o: 162300, h: 162500, l: 161600, c: 161800 },
      { x: 3, o: 161800, h: 163300, l: 161700, c: 163100 },
      { x: 4, o: 163100, h: 163900, l: 162900, c: 163700 },
      { x: 5, o: 163700, h: 164500, l: 163600, c: 164300 },
      { x: 6, o: 164300, h: 165000, l: 164100, c: 164802 }
    ]
  },
  weekly: {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    data: [158700, 160900, 162500, 164802],
    candles: [
      { x: 0, o: 158100, h: 159200, l: 157800, c: 158700 },
      { x: 1, o: 158700, h: 161300, l: 158500, c: 160900 },
      { x: 2, o: 160900, h: 162900, l: 160700, c: 162500 },
      { x: 3, o: 162500, h: 165100, l: 162300, c: 164802 }
    ]
  },
  monthly: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    data: [125400, 134200, 141300, 152400, 157700, 161900, 164802],
    candles: [
      { x: 0, o: 124000, h: 126500, l: 123500, c: 125400 },
      { x: 1, o: 125400, h: 135600, l: 125000, c: 134200 },
      { x: 2, o: 134200, h: 142800, l: 133900, c: 141300 },
      { x: 3, o: 141300, h: 153900, l: 140800, c: 152400 },
      { x: 4, o: 152400, h: 158900, l: 151900, c: 157700 },
      { x: 5, o: 157700, h: 162800, l: 157200, c: 161900 },
      { x: 6, o: 161900, h: 165900, l: 161500, c: 164802 }
    ]
  },
  yearly: {
    labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024'],
    data: [82400, 94200, 103300, 118400, 142700, 156900, 164802],
    candles: [
      { x: 0, o: 81000, h: 84000, l: 79000, c: 82400 },
      { x: 1, o: 82400, h: 96000, l: 81500, c: 94200 },
      { x: 2, o: 94200, h: 105000, l: 92500, c: 103300 },
      { x: 3, o: 103300, h: 120000, l: 102000, c: 118400 },
      { x: 4, o: 118400, h: 144500, l: 117000, c: 142700 },
      { x: 5, o: 142700, h: 158500, l: 141500, c: 156900 },
      { x: 6, o: 156900, h: 166000, l: 155800, c: 164802 }
    ]
  }
}

// Mock data
const portfolioData = {
  balance: 164802.43,
  change: 10.08,
  assets: [
    {
      name: 'Bitcoin',
      symbol: 'BTC',
      price: 47521.89,
      change: 2.34,
      holdings: 0.872,
      value: 41428.36,
      chartData: [41000, 42100, 41400, 42300, 45100, 44300, 47500]
    },
    {
      name: 'Ethereum',
      symbol: 'ETH',
      price: 3521.47,
      change: -0.87,
      holdings: 12.45,
      value: 43842.30,
      chartData: [3400, 3200, 3250, 3400, 3500, 3400, 3520]
    },
    {
      name: 'Solana',
      symbol: 'SOL',
      price: 102.34,
      change: 4.83,
      holdings: 214.56,
      value: 21958.69,
      chartData: [88, 92, 96, 93, 97, 99, 102]
    }
  ],
  recentTransactions: [
    { id: 1, type: 'buy', asset: 'Bitcoin', amount: 0.12, price: 47521.89, total: 5702.63, date: '2023-11-15' },
    { id: 2, type: 'sell', asset: 'Ethereum', amount: 2.5, price: 3495.27, total: 8738.18, date: '2023-11-14' },
    { id: 3, type: 'buy', asset: 'Solana', amount: 45.0, price: 99.82, total: 4491.90, date: '2023-11-12' },
  ]
}

type TimePeriod = '1S' | '1M' | '15M' | '1H' | 'daily' | 'weekly' | 'monthly' | 'yearly';
type ChartType = 'line' | 'candle';

const Dashboard = () => {
  const [isLoading, setIsLoading] = useState(true)
  const [selectedTimePeriod, setSelectedTimePeriod] = useState<TimePeriod>('1H')
  const [chartType, setChartType] = useState<ChartType>('line')
  
  useEffect(() => {
    // Simulate data loading
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 500)
    
    return () => clearTimeout(timer)
  }, [])
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
          drawBorder: false,
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.5)',
        },
      },
      y: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
          drawBorder: false,
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.5)',
          callback: function(value: any) {
            return '$' + value.toLocaleString();
          }
        },
      },
    },
    elements: {
      line: {
        tension: 0.4,
      },
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
      },
    },
  }
  
  const lineChartData = {
    labels: portfolioTimeData[selectedTimePeriod].labels,
    datasets: [
      {
        label: 'Portfolio Value',
        data: portfolioTimeData[selectedTimePeriod].data,
        borderColor: '#3761F2',
        backgroundColor: 'rgba(55, 97, 242, 0.1)',
        fill: true,
      },
    ],
  }
  
  const candleChartData = {
    labels: portfolioTimeData[selectedTimePeriod].labels,
    datasets: [
      {
        label: 'Portfolio Value',
        data: portfolioTimeData[selectedTimePeriod].candles,
        borderColor: (ctx: any) => {
          const item = ctx.raw || {};
          return item.o > item.c ? '#ef4444' : '#10b981';
        },
        backgroundColor: (ctx: any) => {
          const item = ctx.raw || {};
          return item.o > item.c ? 'rgba(239, 68, 68, 0.5)' : 'rgba(16, 185, 129, 0.5)';
        }
      }
    ]
  }
  
  const renderAssetChart = (data: number[]) => {
    const miniChartData = {
      labels: new Array(data.length).fill(''),
      datasets: [
        {
          data,
          borderColor: data[0] < data[data.length - 1] ? '#10B981' : '#EF4444',
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 0,
        },
      ],
    }
    
    const miniChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { 
        legend: { display: false },
        tooltip: { enabled: false }
      },
      scales: {
        x: { display: false },
        y: { display: false }
      },
    }
    
    return (
      <div className="h-12">
        <Line data={miniChartData} options={miniChartOptions} />
      </div>
    )
  }
  
  const handleTimePeriodChange = (period: TimePeriod) => {
    setSelectedTimePeriod(period);
  };
  
  const handleChartTypeChange = (type: ChartType) => {
    setChartType(type);
  };
  
  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    )
  }
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <div className="flex space-x-2">
          <button className="px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-600 transition-colors">
            Deposit
          </button>
          <button className="px-4 py-2 bg-secondary-200 text-white rounded-md hover:bg-secondary-100 transition-colors">
            Withdraw
          </button>
        </div>
      </div>
      
      {/* Portfolio Overview */}
      <div className="grid grid-cols-3 gap-6">
        <div className="card col-span-2 p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h2 className="text-lg font-medium text-gray-400">Portfolio Value</h2>
              <div className="flex items-center mt-1">
                <span className="text-3xl font-bold text-white">${portfolioData.balance.toLocaleString()}</span>
                <div className="ml-3 flex items-center text-green-500">
                  <ArrowUpIcon className="h-4 w-4 mr-1" />
                  <span>{portfolioData.change}%</span>
                </div>
              </div>
            </div>
            <div className="flex flex-col items-end space-y-3">
              <div className="flex items-center space-x-3">
                <div className="flex bg-secondary-200 rounded-md p-1">
                  <button 
                    className={`px-3 py-1 text-sm rounded-md ${chartType === 'line' ? 'bg-primary-500 text-white' : 'text-gray-400'}`}
                    onClick={() => handleChartTypeChange('line')}
                  >
                    Line
                  </button>
                  <button 
                    className={`px-3 py-1 text-sm rounded-md ${chartType === 'candle' ? 'bg-primary-500 text-white' : 'text-gray-400'}`}
                    onClick={() => handleChartTypeChange('candle')}
                  >
                    Candle
                  </button>
                </div>
              </div>
              <div className="flex space-x-1">
                <button 
                  className={`px-2 py-1 text-xs ${selectedTimePeriod === '1S' ? 'bg-primary-500 text-white' : 'bg-secondary-200 text-white'} rounded-md`}
                  onClick={() => handleTimePeriodChange('1S')}
                >
                  1S
                </button>
                <button 
                  className={`px-2 py-1 text-xs ${selectedTimePeriod === '1M' ? 'bg-primary-500 text-white' : 'bg-secondary-200 text-white'} rounded-md`}
                  onClick={() => handleTimePeriodChange('1M')}
                >
                  1M
                </button>
                <button 
                  className={`px-2 py-1 text-xs ${selectedTimePeriod === '15M' ? 'bg-primary-500 text-white' : 'bg-secondary-200 text-white'} rounded-md`}
                  onClick={() => handleTimePeriodChange('15M')}
                >
                  15M
                </button>
                <button 
                  className={`px-2 py-1 text-xs ${selectedTimePeriod === '1H' ? 'bg-primary-500 text-white' : 'bg-secondary-200 text-white'} rounded-md`}
                  onClick={() => handleTimePeriodChange('1H')}
                >
                  1H
                </button>
                <button 
                  className={`px-2 py-1 text-xs ${selectedTimePeriod === 'daily' ? 'bg-primary-500 text-white' : 'bg-secondary-200 text-white'} rounded-md`}
                  onClick={() => handleTimePeriodChange('daily')}
                >
                  1D
                </button>
                <button 
                  className={`px-2 py-1 text-xs ${selectedTimePeriod === 'weekly' ? 'bg-primary-500 text-white' : 'bg-secondary-200 text-white'} rounded-md`}
                  onClick={() => handleTimePeriodChange('weekly')}
                >
                  1W
                </button>
                <button 
                  className={`px-2 py-1 text-xs ${selectedTimePeriod === 'monthly' ? 'bg-primary-500 text-white' : 'bg-secondary-200 text-white'} rounded-md`}
                  onClick={() => handleTimePeriodChange('monthly')}
                >
                  1M
                </button>
                <button 
                  className={`px-2 py-1 text-xs ${selectedTimePeriod === 'yearly' ? 'bg-primary-500 text-white' : 'bg-secondary-200 text-white'} rounded-md`}
                  onClick={() => handleTimePeriodChange('yearly')}
                >
                  1Y
                </button>
              </div>
            </div>
          </div>
          <div className="h-64">
            {chartType === 'line' ? (
              <Line data={lineChartData} options={chartOptions} />
            ) : (
              // Using a simple line chart for candlestick since the financial chart is having compatibility issues
              <Line 
                data={{
                  labels: portfolioTimeData[selectedTimePeriod].labels,
                  datasets: [
                    {
                      label: 'High',
                      data: portfolioTimeData[selectedTimePeriod].candles.map(c => c.h),
                      borderColor: 'rgba(16, 185, 129, 0.7)',
                      borderWidth: 1,
                      pointRadius: 1,
                      fill: false
                    },
                    {
                      label: 'Low',
                      data: portfolioTimeData[selectedTimePeriod].candles.map(c => c.l),
                      borderColor: 'rgba(239, 68, 68, 0.7)',
                      borderWidth: 1,
                      pointRadius: 1,
                      fill: false
                    },
                    {
                      label: 'Open',
                      data: portfolioTimeData[selectedTimePeriod].candles.map(c => c.o),
                      borderColor: 'rgba(96, 165, 250, 0.7)',
                      borderWidth: 1,
                      pointRadius: 2,
                      pointStyle: 'triangle',
                      fill: false
                    },
                    {
                      label: 'Close',
                      data: portfolioTimeData[selectedTimePeriod].candles.map(c => c.c),
                      borderColor: 'rgba(249, 168, 37, 0.7)',
                      borderWidth: 1,
                      pointRadius: 2,
                      pointStyle: 'rect',
                      fill: false
                    }
                  ]
                }} 
                options={chartOptions} 
              />
            )}
          </div>
        </div>
        
        <div className="space-y-6">
          <div className="card p-5">
            <h2 className="text-lg font-medium text-gray-400 mb-3">Asset Allocation</h2>
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <div className="h-4 w-4 rounded-full bg-primary-500"></div>
                <span className="text-white">Bitcoin</span>
              </div>
              <span className="text-white">25.1%</span>
            </div>
            <div className="w-full bg-secondary-200 h-2 rounded-full mt-2 mb-3">
              <div className="bg-primary-500 h-2 rounded-full" style={{ width: '25.1%' }}></div>
            </div>
            
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <div className="h-4 w-4 rounded-full bg-indigo-500"></div>
                <span className="text-white">Ethereum</span>
              </div>
              <span className="text-white">26.6%</span>
            </div>
            <div className="w-full bg-secondary-200 h-2 rounded-full mt-2 mb-3">
              <div className="bg-indigo-500 h-2 rounded-full" style={{ width: '26.6%' }}></div>
            </div>
            
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <div className="h-4 w-4 rounded-full bg-purple-500"></div>
                <span className="text-white">Solana</span>
              </div>
              <span className="text-white">13.3%</span>
            </div>
            <div className="w-full bg-secondary-200 h-2 rounded-full mt-2 mb-3">
              <div className="bg-purple-500 h-2 rounded-full" style={{ width: '13.3%' }}></div>
            </div>
            
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <div className="h-4 w-4 rounded-full bg-gray-500"></div>
                <span className="text-white">Others</span>
              </div>
              <span className="text-white">35.0%</span>
            </div>
            <div className="w-full bg-secondary-200 h-2 rounded-full mt-2">
              <div className="bg-gray-500 h-2 rounded-full" style={{ width: '35.0%' }}></div>
            </div>
          </div>
          
          <div className="card p-5">
            <h2 className="text-lg font-medium text-gray-400 mb-3">Quick Actions</h2>
            <div className="grid grid-cols-2 gap-2">
              <button className="py-3 bg-secondary-200 hover:bg-secondary-100 text-white rounded-md transition-colors">
                Buy/Sell
              </button>
              <button className="py-3 bg-secondary-200 hover:bg-secondary-100 text-white rounded-md transition-colors">
                Send/Receive
              </button>
              <button className="py-3 bg-secondary-200 hover:bg-secondary-100 text-white rounded-md transition-colors">
                Convert
              </button>
              <button className="py-3 bg-secondary-200 hover:bg-secondary-100 text-white rounded-md transition-colors">
                Stake
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Assets */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-white">Your Assets</h2>
          <button className="text-primary-400 hover:text-primary-500">View All</button>
        </div>
        
        <div className="grid grid-cols-3 gap-6">
          {portfolioData.assets.map((asset) => (
            <div key={asset.symbol} className="card p-5">
              <div className="flex justify-between items-start">
                <div className="flex items-center">
                  <div className="h-10 w-10 rounded-full bg-primary-500/20 flex items-center justify-center mr-3">
                    <span className="text-primary-500 font-bold">{asset.symbol.substring(0, 1)}</span>
                  </div>
                  <div>
                    <h3 className="font-medium text-white">{asset.name}</h3>
                    <p className="text-sm text-gray-400">{asset.symbol}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-1">
                  {asset.change >= 0 ? (
                    <ArrowUpIcon className="h-3 w-3 text-green-500" />
                  ) : (
                    <ArrowDownIcon className="h-3 w-3 text-red-500" />
                  )}
                  <span className={`text-sm ${asset.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                    {Math.abs(asset.change)}%
                  </span>
                </div>
              </div>
              
              {renderAssetChart(asset.chartData)}
              
              <div className="flex justify-between items-end mt-2">
                <div>
                  <p className="text-sm text-gray-400">Holdings</p>
                  <p className="text-white font-medium">
                    {asset.holdings} {asset.symbol}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-400">Value</p>
                  <p className="text-white font-medium">${asset.value.toLocaleString()}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Markets and Recent Transactions */}
      <div className="grid grid-cols-2 gap-6">
        <div className="card p-5">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-white">Markets</h2>
            <button className="text-primary-400 hover:text-primary-500">View All</button>
          </div>
          
          <table className="w-full">
            <thead>
              <tr className="text-gray-400 text-sm">
                <th className="text-left pb-3 font-medium">Name</th>
                <th className="text-right pb-3 font-medium">Price</th>
                <th className="text-right pb-3 font-medium">Change</th>
                <th className="text-right pb-3 font-medium">Action</th>
              </tr>
            </thead>
            <tbody>
              {portfolioData.assets.map((asset) => (
                <tr key={asset.symbol} className="border-t border-secondary-200">
                  <td className="py-3">
                    <div className="flex items-center">
                      <div className="h-8 w-8 rounded-full bg-primary-500/20 flex items-center justify-center mr-2">
                        <span className="text-primary-500 font-bold">{asset.symbol.substring(0, 1)}</span>
                      </div>
                      <div>
                        <p className="text-white">{asset.name}</p>
                        <p className="text-xs text-gray-400">{asset.symbol}</p>
                      </div>
                    </div>
                  </td>
                  <td className="text-right text-white">${asset.price.toLocaleString()}</td>
                  <td className="text-right">
                    <div className="flex items-center justify-end">
                      {asset.change >= 0 ? (
                        <ArrowUpIcon className="h-3 w-3 text-green-500 mr-1" />
                      ) : (
                        <ArrowDownIcon className="h-3 w-3 text-red-500 mr-1" />
                      )}
                      <span className={`${asset.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                        {Math.abs(asset.change)}%
                      </span>
                    </div>
                  </td>
                  <td className="text-right">
                    <div className="flex space-x-1 justify-end">
                      <button className="px-2 py-1 text-xs bg-primary-500 text-white rounded">Buy</button>
                      <button className="px-2 py-1 text-xs bg-secondary-100 text-white rounded">Sell</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="card p-5">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-white">Recent Transactions</h2>
            <button className="text-primary-400 hover:text-primary-500">View All</button>
          </div>
          
          <table className="w-full">
            <thead>
              <tr className="text-gray-400 text-sm">
                <th className="text-left pb-3 font-medium">Asset</th>
                <th className="text-right pb-3 font-medium">Amount</th>
                <th className="text-right pb-3 font-medium">Price</th>
                <th className="text-right pb-3 font-medium">Total</th>
              </tr>
            </thead>
            <tbody>
              {portfolioData.recentTransactions.map((tx) => (
                <tr key={tx.id} className="border-t border-secondary-200">
                  <td className="py-3">
                    <div className="flex items-center">
                      <div className={`h-8 w-8 rounded-full ${tx.type === 'buy' ? 'bg-green-500/20' : 'bg-red-500/20'} flex items-center justify-center mr-2`}>
                        <span className={tx.type === 'buy' ? 'text-green-500' : 'text-red-500'}>
                          {tx.type === 'buy' ? '+' : '-'}
                        </span>
                      </div>
                      <div>
                        <p className="text-white">{tx.type === 'buy' ? 'Bought' : 'Sold'} {tx.asset}</p>
                        <p className="text-xs text-gray-400">{new Date(tx.date).toLocaleDateString()}</p>
                      </div>
                    </div>
                  </td>
                  <td className="text-right text-white">{tx.amount}</td>
                  <td className="text-right text-white">${tx.price.toLocaleString()}</td>
                  <td className="text-right text-white">${tx.total.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Dashboard 