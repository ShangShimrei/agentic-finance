import React, { useState } from 'react'
import { ArrowUpIcon, ArrowDownIcon, ArrowsRightLeftIcon, BanknotesIcon } from '@heroicons/react/24/solid'
import { MagnifyingGlassIcon, FunnelIcon, CalendarIcon } from '@heroicons/react/24/outline'

// Transaction types
type TransactionType = 'buy' | 'sell' | 'transfer' | 'deposit' | 'withdrawal' | 'all';
type AssetType = 'crypto' | 'stock' | 'etf' | 'cash' | 'all';

// Transaction status
type TransactionStatus = 'completed' | 'pending' | 'failed';

// Transaction data interface
interface Transaction {
  id: string;
  type: TransactionType;
  assetType: AssetType;
  assetName: string;
  assetSymbol: string;
  amount: number;
  price: number | null;
  total: number;
  date: string;
  status: TransactionStatus;
}

// Filter type
interface TransactionFilters {
  type: TransactionType;
  assetType: AssetType;
  dateRange: 'all' | '7d' | '30d' | '90d' | 'ytd';
  search: string;
}

const Transactions = () => {
  // State for filters
  const [filters, setFilters] = useState<TransactionFilters>({
    type: 'all',
    assetType: 'all',
    dateRange: 'all',
    search: ''
  });

  // Mock transaction data
  const transactions: Transaction[] = [
    {
      id: '1',
      type: 'buy',
      assetType: 'crypto',
      assetName: 'Bitcoin',
      assetSymbol: 'BTC',
      amount: 0.05,
      price: 54200.42,
      total: 2710.02,
      date: '2025-03-22T10:32:14',
      status: 'completed'
    },
    {
      id: '2',
      type: 'sell',
      assetType: 'crypto',
      assetName: 'Ethereum',
      assetSymbol: 'ETH',
      amount: 2.5,
      price: 2940.33,
      total: 7350.83,
      date: '2025-03-18T15:21:46',
      status: 'completed'
    },
    {
      id: '3',
      type: 'buy',
      assetType: 'stock',
      assetName: 'Apple Inc.',
      assetSymbol: 'AAPL',
      amount: 15,
      price: 178.32,
      total: 2674.80,
      date: '2025-03-15T09:45:12',
      status: 'completed'
    },
    {
      id: '4',
      type: 'deposit',
      assetType: 'cash',
      assetName: 'US Dollar',
      assetSymbol: 'USD',
      amount: 10000,
      price: null,
      total: 10000,
      date: '2025-03-10T14:20:45',
      status: 'completed'
    },
    {
      id: '5',
      type: 'transfer',
      assetType: 'crypto',
      assetName: 'Bitcoin',
      assetSymbol: 'BTC',
      amount: 0.1,
      price: 51230.67,
      total: 5123.07,
      date: '2025-03-05T17:12:33',
      status: 'completed'
    },
    {
      id: '6',
      type: 'buy',
      assetType: 'stock',
      assetName: 'Tesla',
      assetSymbol: 'TSLA',
      amount: 10,
      price: 178.52,
      total: 1785.20,
      date: '2025-03-01T11:34:56',
      status: 'completed'
    },
    {
      id: '7',
      type: 'buy',
      assetType: 'crypto',
      assetName: 'Solana',
      assetSymbol: 'SOL',
      amount: 20,
      price: 102.33,
      total: 2046.60,
      date: '2025-02-28T10:08:32',
      status: 'completed'
    },
    {
      id: '8',
      type: 'withdrawal',
      assetType: 'cash',
      assetName: 'US Dollar',
      assetSymbol: 'USD',
      amount: 5000,
      price: null,
      total: 5000,
      date: '2025-02-25T16:45:02',
      status: 'completed'
    },
    {
      id: '9',
      type: 'buy',
      assetType: 'etf',
      assetName: 'Vanguard S&P 500 ETF',
      assetSymbol: 'VOO',
      amount: 5,
      price: 412.35,
      total: 2061.75,
      date: '2025-02-20T13:22:41',
      status: 'completed'
    },
    {
      id: '10',
      type: 'sell',
      assetType: 'stock',
      assetName: 'Microsoft',
      assetSymbol: 'MSFT',
      amount: 8,
      price: 330.45,
      total: 2643.60,
      date: '2025-02-15T09:15:33',
      status: 'completed'
    },
    {
      id: '11',
      type: 'buy',
      assetType: 'crypto',
      assetName: 'Cardano',
      assetSymbol: 'ADA',
      amount: 3000,
      price: 0.45,
      total: 1350.00,
      date: '2025-02-10T14:52:17',
      status: 'completed'
    },
    {
      id: '12',
      type: 'deposit',
      assetType: 'cash',
      assetName: 'US Dollar',
      assetSymbol: 'USD',
      amount: 15000,
      price: null,
      total: 15000,
      date: '2025-02-05T11:10:23',
      status: 'completed'
    },
    {
      id: '13',
      type: 'buy',
      assetType: 'crypto',
      assetName: 'Ethereum',
      assetSymbol: 'ETH',
      amount: 1.2,
      price: 2895.32,
      total: 3474.38,
      date: '2025-03-23T08:15:00',
      status: 'pending'
    },
    {
      id: '14',
      type: 'withdrawal',
      assetType: 'cash',
      assetName: 'US Dollar',
      assetSymbol: 'USD',
      amount: 2500,
      price: null,
      total: 2500,
      date: '2025-03-22T09:30:45',
      status: 'pending'
    },
    {
      id: '15',
      type: 'sell',
      assetType: 'stock',
      assetName: 'Amazon',
      assetSymbol: 'AMZN',
      amount: 5,
      price: 178.92,
      total: 894.60,
      date: '2025-03-15T16:42:22',
      status: 'failed'
    }
  ];
  
  // Apply filters to transactions
  const filteredTransactions = transactions.filter(transaction => {
    // Filter by transaction type
    if (filters.type !== 'all' && transaction.type !== filters.type) {
      return false;
    }
    
    // Filter by asset type
    if (filters.assetType !== 'all' && transaction.assetType !== filters.assetType) {
      return false;
    }
    
    // Filter by date range
    if (filters.dateRange !== 'all') {
      const txDate = new Date(transaction.date);
      const now = new Date();
      
      if (filters.dateRange === '7d') {
        const sevenDaysAgo = new Date(now.setDate(now.getDate() - 7));
        if (txDate < sevenDaysAgo) return false;
      } else if (filters.dateRange === '30d') {
        const thirtyDaysAgo = new Date(now.setDate(now.getDate() - 30));
        if (txDate < thirtyDaysAgo) return false;
      } else if (filters.dateRange === '90d') {
        const ninetyDaysAgo = new Date(now.setDate(now.getDate() - 90));
        if (txDate < ninetyDaysAgo) return false;
      } else if (filters.dateRange === 'ytd') {
        const startOfYear = new Date(now.getFullYear(), 0, 1);
        if (txDate < startOfYear) return false;
      }
    }
    
    // Filter by search term
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      return (
        transaction.assetName.toLowerCase().includes(searchLower) ||
        transaction.assetSymbol.toLowerCase().includes(searchLower) ||
        transaction.id.toLowerCase().includes(searchLower)
      );
    }
    
    return true;
  });
  
  // Get transaction icon based on type
  const getTransactionIcon = (type: TransactionType) => {
    switch (type) {
      case 'buy':
        return <ArrowDownIcon className="w-4 h-4 text-green-500" />;
      case 'sell':
        return <ArrowUpIcon className="w-4 h-4 text-red-500" />;
      case 'transfer':
        return <ArrowsRightLeftIcon className="w-4 h-4 text-blue-500" />;
      case 'deposit':
        return <ArrowDownIcon className="w-4 h-4 text-green-500" />;
      case 'withdrawal':
        return <ArrowUpIcon className="w-4 h-4 text-red-500" />;
      default:
        return <BanknotesIcon className="w-4 h-4 text-gray-500" />;
    }
  };
  
  // Get transaction status style
  const getStatusStyle = (status: TransactionStatus) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500/20 text-green-500';
      case 'pending':
        return 'bg-yellow-500/20 text-yellow-500';
      case 'failed':
        return 'bg-red-500/20 text-red-500';
      default:
        return 'bg-gray-500/20 text-gray-500';
    }
  };
  
  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };
  
  // Format time for display
  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit'
    });
  };
  
  // Update filter handler
  const handleFilterChange = (filterName: keyof TransactionFilters, value: string) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }));
  };
  
  // Get transaction type display name
  const getTransactionTypeDisplay = (type: TransactionType) => {
    switch (type) {
      case 'buy':
        return 'Buy';
      case 'sell':
        return 'Sell';
      case 'transfer':
        return 'Transfer';
      case 'deposit':
        return 'Deposit';
      case 'withdrawal':
        return 'Withdrawal';
      default:
        return 'Unknown';
    }
  };
  
  return (
    <div className="h-full">
      {/* Transactions header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Transactions</h1>
          <p className="text-gray-400">View and filter your transaction history</p>
        </div>
      </div>
      
      {/* Filters */}
      <div className="bg-secondary-300 rounded-xl p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {/* Search filter */}
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search transactions..."
              className="w-full bg-secondary-200 rounded-md pl-10 pr-4 py-2 text-gray-300 outline-none"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
            />
          </div>
          
          {/* Transaction type filter */}
          <div className="relative">
            <FunnelIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <select
              className="w-full bg-secondary-200 rounded-md pl-10 pr-4 py-2 text-gray-300 outline-none appearance-none"
              value={filters.type}
              onChange={(e) => handleFilterChange('type', e.target.value as TransactionType)}
            >
              <option value="all">All Transaction Types</option>
              <option value="buy">Buy</option>
              <option value="sell">Sell</option>
              <option value="transfer">Transfer</option>
              <option value="deposit">Deposit</option>
              <option value="withdrawal">Withdrawal</option>
            </select>
          </div>
          
          {/* Asset type filter */}
          <div className="relative">
            <FunnelIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <select
              className="w-full bg-secondary-200 rounded-md pl-10 pr-4 py-2 text-gray-300 outline-none appearance-none"
              value={filters.assetType}
              onChange={(e) => handleFilterChange('assetType', e.target.value as AssetType)}
            >
              <option value="all">All Asset Types</option>
              <option value="crypto">Crypto</option>
              <option value="stock">Stocks</option>
              <option value="etf">ETFs</option>
              <option value="cash">Cash</option>
            </select>
          </div>
          
          {/* Date range filter */}
          <div className="relative">
            <CalendarIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <select
              className="w-full bg-secondary-200 rounded-md pl-10 pr-4 py-2 text-gray-300 outline-none appearance-none"
              value={filters.dateRange}
              onChange={(e) => handleFilterChange('dateRange', e.target.value as TransactionFilters['dateRange'])}
            >
              <option value="all">All Time</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
              <option value="ytd">Year to Date</option>
            </select>
          </div>
        </div>
      </div>
      
      {/* Transactions list */}
      <div className="bg-secondary-300 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-secondary-200">
                <th className="text-left py-4 px-6 text-gray-400 font-medium">Type</th>
                <th className="text-left py-4 px-6 text-gray-400 font-medium">Asset</th>
                <th className="text-right py-4 px-6 text-gray-400 font-medium">Amount</th>
                <th className="text-right py-4 px-6 text-gray-400 font-medium">Price</th>
                <th className="text-right py-4 px-6 text-gray-400 font-medium">Total</th>
                <th className="text-center py-4 px-6 text-gray-400 font-medium">Status</th>
                <th className="text-right py-4 px-6 text-gray-400 font-medium">Date</th>
              </tr>
            </thead>
            <tbody>
              {filteredTransactions.map(transaction => (
                <tr key={transaction.id} className="border-b border-secondary-200 hover:bg-secondary-200 transition-colors">
                  <td className="py-4 px-6">
                    <div className="flex items-center">
                      <div className="w-8 h-8 rounded-full bg-secondary-200 flex items-center justify-center mr-3">
                        {getTransactionIcon(transaction.type)}
                      </div>
                      <span className="text-white">{getTransactionTypeDisplay(transaction.type)}</span>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <div>
                      <div className="font-medium text-white">{transaction.assetName}</div>
                      <div className="text-gray-400 text-sm">{transaction.assetSymbol}</div>
                    </div>
                  </td>
                  <td className="py-4 px-6 text-right font-medium text-white">
                    {transaction.assetType === 'cash' 
                      ? `$${transaction.amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
                      : transaction.amount.toLocaleString('en-US', {
                          minimumFractionDigits: transaction.assetType === 'crypto' ? 6 : 2,
                          maximumFractionDigits: transaction.assetType === 'crypto' ? 6 : 2
                        })}
                  </td>
                  <td className="py-4 px-6 text-right font-medium text-white">
                    {transaction.price 
                      ? `$${transaction.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
                      : '-'}
                  </td>
                  <td className="py-4 px-6 text-right font-medium text-white">
                    ${transaction.total.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>
                  <td className="py-4 px-6">
                    <div className="flex justify-center">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusStyle(transaction.status)}`}>
                        {transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
                      </span>
                    </div>
                  </td>
                  <td className="py-4 px-6 text-right">
                    <div className="text-white">{formatDate(transaction.date)}</div>
                    <div className="text-gray-400 text-sm">{formatTime(transaction.date)}</div>
                  </td>
                </tr>
              ))}
              
              {filteredTransactions.length === 0 && (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-gray-400">
                    No transactions found matching your filters
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Transactions 