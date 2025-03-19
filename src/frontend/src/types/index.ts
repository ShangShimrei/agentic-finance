export interface Activity {
  action: 'BUY' | 'SELL' | 'HOLD';
  symbol: string;
  quantity: number;
  price: number;
  agent: string;
  time: string;
}

export interface AgentSignal {
  symbol: string;
  action: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  reasoning: string;
}

export interface PortfolioMetric {
  title: string;
  value: string;
  change: number;
  changeText: string;
}

export interface PerformanceData {
  x: string[];
  y: number[];
}

export interface AgentSignalsData {
  agents: string[];
  confidence: number[];
  signals: ('BUY' | 'SELL' | 'HOLD')[];
} 