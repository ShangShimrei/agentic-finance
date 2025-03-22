import React, { useState, useRef, useEffect } from 'react'
import { 
  PaperAirplaneIcon, 
  XMarkIcon,
  ChatBubbleLeftRightIcon,
  ChevronDownIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

interface ChatAssistantProps {
  isOpen: boolean;
  onClose: () => void;
}

// Main Chat component
const ChatAssistant: React.FC<ChatAssistantProps> = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm Yuki, your AI assistant. How can I help you understand the dashboard today?",
      sender: 'assistant',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);
  
  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const handleSend = () => {
    if (inputValue.trim() === '') return;
    
    const newMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, newMessage]);
    setInputValue('');
    setIsTyping(true);
    
    // Simulate AI response
    setTimeout(() => {
      const responseMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: generateResponse(inputValue),
        sender: 'assistant',
        timestamp: new Date()
      };
      
      setIsTyping(false);
      setMessages(prev => [...prev, responseMessage]);
    }, 1500);
  };
  
  const generateResponse = (query: string): string => {
    // This is a mock response generator
    // In a real application, this would call an actual AI service
    
    const lowercaseQuery = query.toLowerCase();
    
    if (lowercaseQuery.includes('chart') || lowercaseQuery.includes('graph')) {
      return "The charts on the dashboard display price movements over time. The line charts show continuous price trends, while candlestick charts provide more detail with open, high, low, and close values for each time period. Green candles indicate price increases, while red shows decreases. You can change the time period using the buttons above the chart.";
    }
    
    if (lowercaseQuery.includes('portfolio') || lowercaseQuery.includes('holdings')) {
      return "Your portfolio section shows all your current holdings, their allocation percentages, current values, and performance metrics. The pie chart visualizes your asset allocation across different categories, helping you understand your diversification at a glance.";
    }
    
    if (lowercaseQuery.includes('trading') || lowercaseQuery.includes('buy') || lowercaseQuery.includes('sell')) {
      return "To execute trades, navigate to the Assets section and select the asset you wish to trade. You'll find buy/sell buttons with options to set limit orders, market orders, or stop-loss orders. Always review market conditions and consider consulting a financial advisor before making significant trades.";
    }
    
    if (lowercaseQuery.includes('ai') || lowercaseQuery.includes('agent') || lowercaseQuery.includes('model context protocol')) {
      return "Our platform uses specialized AI agents powered by the Model Context Protocol (MCP) to analyze market data and generate insights. These agents include Technical Agents that analyze price patterns, Fundamental Agents that evaluate company financials, and Sentiment Agents that assess market mood from news and social media. Together, they provide comprehensive trading signals.";
    }

    if (lowercaseQuery.includes('candlestick')) {
      return "Candlestick charts are a type of financial chart that shows the price movement of an asset. Each 'candle' represents a specific time period (e.g., 1 day, 1 hour). The body of the candle shows the opening and closing prices, while the 'wicks' or 'shadows' show the high and low prices during that period. In our platform, green candles indicate that the closing price was higher than the opening (bullish), while red candles indicate the closing price was lower than the opening (bearish).";
    }

    if (lowercaseQuery.includes('indicator') || lowercaseQuery.includes('technical')) {
      return "Technical indicators are mathematical calculations based on price, volume, or open interest of a security. Our platform provides several key indicators:\n\n- Moving Averages (MA): Shows the average price over a specific period\n- Relative Strength Index (RSI): Measures the speed and change of price movements (overbought/oversold)\n- MACD (Moving Average Convergence Divergence): Shows the relationship between two moving averages\n- Bollinger Bands: Indicates volatility with bands that contract and expand\n\nYou can add these indicators to charts by clicking the 'Indicators' button above the chart.";
    }

    if (lowercaseQuery.includes('market sentiment') || lowercaseQuery.includes('news impact')) {
      return "Our platform analyzes market sentiment from various sources including news articles, social media, and analyst reports. The sentiment score (ranging from -100 to +100) indicates the overall market mood toward an asset. Positive scores suggest bullish sentiment, while negative scores suggest bearish sentiment. The News section provides the latest articles with their sentiment impact highlighted, helping you understand how news events might affect your investments.";
    }

    if (lowercaseQuery.includes('asset allocation') || lowercaseQuery.includes('diversification')) {
      return "Diversification is a risk management strategy that mixes various investments to reduce exposure to any single asset or risk. The Portfolio section visualizes your asset allocation across different categories through pie and bar charts. Our AI recommends optimal asset allocation based on your risk profile, market conditions, and investment goals. The color-coding helps you quickly identify over-concentrated positions that might need rebalancing.";
    }

    if (lowercaseQuery.includes('translate') || lowercaseQuery.includes('explain') || lowercaseQuery.includes('what does') || lowercaseQuery.includes('what is')) {
      const financialTerms = {
        'bull market': 'A bull market is a period of time in financial markets when the price of an asset or security rises continuously. It typically indicates investor confidence and economic growth.',
        'bear market': 'A bear market is a period of time when stock prices are falling, typically by 20% or more, accompanied by widespread pessimism and negative investor sentiment.',
        'volatility': 'Volatility measures how much and how quickly the price of an asset fluctuates. Higher volatility indicates larger, more rapid price swings and generally implies higher risk.',
        'liquidity': 'Liquidity refers to how easily an asset can be bought or sold in the market without affecting its price. Cash is the most liquid asset, while real estate is typically less liquid.',
        'market cap': 'Market capitalization (market cap) is the total value of a company\'s outstanding shares, calculated by multiplying the current share price by the total number of shares.',
        'dividend': 'A dividend is a distribution of a portion of a company\'s earnings to its shareholders as decided by its board of directors.',
        'yield': 'Yield is the income returned on an investment, such as interest or dividends received from holding a security. Usually expressed as an annual percentage rate.',
        'trading volume': 'Trading volume is the total number of shares or contracts traded in a security or market during a given period. It indicates the level of activity and liquidity.',
        'resistance level': 'A resistance level is a price point on a chart where sellers are likely to overpower buyers, causing the price to stop rising and potentially reverse direction.',
        'support level': 'A support level is a price point on a chart where buyers are likely to overpower sellers, causing the price to stop falling and potentially reverse direction.',
        'market order': 'A market order is an instruction to buy or sell a security immediately at the best available current price.',
        'limit order': 'A limit order is an instruction to buy or sell a security at a specific price or better. It allows precise control over the execution price.',
        'stop loss': 'A stop-loss order is designed to limit an investor\'s loss on a position by automatically selling when the price reaches a predetermined level.'
      };
      
      for (const [term, explanation] of Object.entries(financialTerms)) {
        if (lowercaseQuery.includes(term)) {
          return explanation;
        }
      }
      
      return "I'd be happy to explain any financial term or concept. Could you please specify which trading term or dashboard element you'd like me to explain?";
    }
    
    return "That's a great question. As your AI assistant, I can help explain various aspects of the dashboard, trading concepts, or market analysis. Could you provide more specific details about what you'd like to know, or which part of the platform you need help with?";
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };
  
  // Don't render anything if not open
  if (!isOpen) return null;
  
  return (
    <div className="fixed bottom-0 left-64 z-20" onClick={e => e.stopPropagation()}>
      <div className="bg-secondary-300 w-80 rounded-t-xl shadow-xl flex flex-col h-[500px] border border-secondary-200">
        {/* Header */}
        <div className="p-4 border-b border-secondary-200 flex justify-between items-center">
          <div className="flex items-center">
            <div className="bg-primary-500 h-8 w-8 rounded-full flex items-center justify-center">
              <span className="text-white font-bold">Y</span>
            </div>
            <div className="ml-3">
              <h3 className="text-lg font-semibold text-white">Yuki AI Assistant</h3>
              <p className="text-xs text-gray-400">Finance Expert</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map(message => (
            <div 
              key={message.id} 
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div 
                className={`max-w-[80%] rounded-lg px-4 py-3 ${
                  message.sender === 'user' 
                    ? 'bg-primary-500 text-white' 
                    : 'bg-secondary-200 text-gray-200'
                }`}
              >
                <p className="text-base font-medium">{message.text}</p>
                <p className="text-xs text-gray-400 mt-1">
                  {message.timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-secondary-200 text-gray-200 rounded-lg px-4 py-3">
                <div className="typing-animation">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input */}
        <div className="p-4 border-t border-secondary-200">
          <div className="flex items-center bg-secondary-200 rounded-lg overflow-hidden">
            <input
              ref={inputRef}
              type="text"
              placeholder="Ask me anything about trading..."
              className="flex-1 bg-transparent border-none outline-none text-gray-300 p-3 text-base"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button 
              onClick={handleSend}
              className="bg-primary-500 text-white p-3 rounded-r-lg"
              disabled={inputValue.trim() === ''}
            >
              <PaperAirplaneIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Chat bubble button component that toggles the chat
export const ChatButton: React.FC<{ id?: string }> = ({ id }) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const toggleChat = () => {
    setIsOpen(!isOpen);
    console.log("Chat toggled:", !isOpen); // Add logging to check if toggle is working
  };
  
  return (
    <>
      <button
        id={id}
        onClick={toggleChat}
        className="fixed bottom-4 right-4 bg-primary-500 text-white rounded-full p-3 shadow-lg hover:bg-primary-600 transition-colors z-40 flex items-center"
      >
        {isOpen ? (
          <ChevronDownIcon className="h-6 w-6" />
        ) : (
          <>
            <ChatBubbleLeftRightIcon className="h-6 w-6" />
            <span className="ml-2 font-medium">Ask Yuki</span>
          </>
        )}
      </button>
      <ChatAssistant isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  )
}

export default ChatAssistant 