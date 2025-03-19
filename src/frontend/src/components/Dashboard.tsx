import React from 'react';
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/solid';
import Plot from 'react-plotly.js';
import { PortfolioMetric, PerformanceData, AgentSignalsData, Activity } from '../types';

const MetricCard: React.FC<PortfolioMetric> = ({ title, value, change, changeText }) => {
  const isPositive = change >= 0;
  
  return (
    <div className="stat-card">
      <h3 className="text-base font-medium text-gray-400">{title}</h3>
      <div className="mt-2 flex items-baseline">
        <p className="text-3xl font-semibold text-white">{value}</p>
        <span
          className={`ml-2 text-base font-medium flex items-center ${
            isPositive ? 'trend-up' : 'trend-down'
          }`}
        >
          {isPositive ? (
            <ArrowUpIcon className="h-5 w-5 mr-1" />
          ) : (
            <ArrowDownIcon className="h-5 w-5 mr-1" />
          )}
          {changeText}
        </span>
      </div>
    </div>
  );
};

const Dashboard: React.FC = () => {
  // Sample data - replace with real data from your backend
  const metrics: PortfolioMetric[] = [
    {
      title: 'Portfolio Value',
      value: '$1,234,567',
      change: 2.5,
      changeText: '2.5%'
    },
    {
      title: 'Daily P&L',
      value: '$12,345',
      change: 1.8,
      changeText: '+$12,345'
    },
    {
      title: 'Active Positions',
      value: '15',
      change: -2,
      changeText: '-2'
    },
    {
      title: 'Win Rate',
      value: '68%',
      change: 5,
      changeText: '+5%'
    }
  ];

  // Sample portfolio performance data
  const performanceData: PerformanceData = {
    x: Array.from({ length: 30 }, (_, i) => 
      new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    ),
    y: Array.from({ length: 30 }, (_, i) => 
      1000000 * (1 + Math.sin(i / 5) * 0.1 + i / 100)
    )
  };

  // Sample agent signals data
  const agentSignals: AgentSignalsData = {
    agents: ['Buffet', 'Ackman', 'Technical', 'Sentiment', 'Fundamental', 'Research'],
    confidence: [0.85, 0.72, 0.45, 0.65, 0.78, 0.62],
    signals: ['BUY', 'BUY', 'HOLD', 'SELL', 'BUY', 'HOLD']
  };

  // Sample activities
  const activities: Activity[] = [
    {
      action: 'BUY',
      symbol: 'AAPL',
      quantity: 100,
      price: 185.92,
      agent: 'Buffet Agent',
      time: '2 minutes ago'
    },
    {
      action: 'SELL',
      symbol: 'MSFT',
      quantity: 50,
      price: 372.65,
      agent: 'Technical Agent',
      time: '15 minutes ago'
    },
    {
      action: 'BUY',
      symbol: 'GOOGL',
      quantity: 25,
      price: 142.71,
      agent: 'Research Agent',
      time: '1 hour ago'
    }
  ];

  return (
    <div className="h-screen overflow-y-auto pb-8">
      <div className="max-w-[2000px] mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        {/* Metrics Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
          {metrics.map((metric) => (
            <MetricCard key={metric.title} {...metric} />
          ))}
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
          {/* Portfolio Performance Chart */}
          <div className="card min-h-[400px] flex flex-col">
            <div className="card-header">
              <h3 className="text-xl font-medium text-white">
                Portfolio Performance
              </h3>
            </div>
            <div className="card-body flex-1">
              <Plot
                data={[
                  {
                    x: performanceData.x,
                    y: performanceData.y,
                    type: 'scatter',
                    mode: 'lines',
                    line: { color: '#3B82F6', width: 3 }
                  }
                ]}
                layout={{
                  height: 320,
                  autosize: true,
                  margin: { t: 10, r: 10, b: 40, l: 80 },
                  xaxis: { 
                    showgrid: false,
                    tickfont: { color: '#9CA3AF', size: 14 }
                  },
                  yaxis: { 
                    tickformat: '$,.0f',
                    showgrid: true,
                    gridcolor: '#374151',
                    tickfont: { color: '#9CA3AF', size: 16 }
                  },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)',
                  font: { color: '#9CA3AF', size: 14 }
                }}
                config={{ 
                  responsive: true, 
                  displayModeBar: false,
                  displaylogo: false
                }}
                style={{ width: '100%', height: '100%' }}
                useResizeHandler={true}
              />
            </div>
          </div>

          {/* Agent Signals Chart */}
          <div className="card min-h-[400px] flex flex-col">
            <div className="card-header">
              <h3 className="text-xl font-medium text-white">
                Agent Signals
              </h3>
            </div>
            <div className="card-body flex-1">
              <Plot
                data={[
                  {
                    type: 'bar',
                    x: agentSignals.confidence,
                    y: agentSignals.agents,
                    orientation: 'h',
                    marker: {
                      color: agentSignals.signals.map(signal => 
                        signal === 'BUY' ? '#10B981' : 
                        signal === 'SELL' ? '#EF4444' : '#6B7280'
                      )
                    },
                    text: agentSignals.signals,
                    textposition: 'auto',
                    textfont: { size: 14 }
                  }
                ]}
                layout={{
                  height: 320,
                  autosize: true,
                  margin: { t: 10, r: 10, b: 40, l: 160 },
                  xaxis: { 
                    title: 'Confidence',
                    showgrid: true,
                    gridcolor: '#374151',
                    tickfont: { color: '#9CA3AF', size: 14 },
                    range: [0, 1]
                  },
                  yaxis: { 
                    showgrid: false,
                    tickfont: { color: '#9CA3AF', size: 16 },
                    ticksuffix: '     '
                  },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)',
                  font: { color: '#9CA3AF', size: 14 },
                  bargap: 0.4,
                  barmode: 'group'
                }}
                config={{ 
                  responsive: true, 
                  displayModeBar: false,
                  displaylogo: false
                }}
                style={{ width: '100%', height: '100%' }}
                useResizeHandler={true}
              />
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-xl font-medium text-white">Recent Activity</h3>
          </div>
          <div className="divide-y divide-dark-300">
            {activities.map((activity, i) => (
              <div key={i} className="px-4 sm:px-6 py-4">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <div className="flex items-center flex-wrap gap-2">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium ${
                        activity.action === 'BUY'
                          ? 'bg-accent-green bg-opacity-20 text-accent-green'
                          : 'bg-accent-red bg-opacity-20 text-accent-red'
                      }`}
                    >
                      {activity.action}
                    </span>
                    <span className="text-base text-gray-300">
                      {activity.quantity} {activity.symbol} @ ${activity.price}
                    </span>
                  </div>
                  <div className="flex items-center text-base text-gray-400 gap-2">
                    <span>{activity.agent}</span>
                    <span>{activity.time}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 