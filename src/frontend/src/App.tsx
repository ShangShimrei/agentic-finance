import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';

// Placeholder components for other routes
const Portfolio = () => <div>Portfolio View</div>;
const Research = () => <div>Research View</div>;
const Trading = () => <div>Trading View</div>;
const Agents = () => <div>Agents View</div>;
const Performance = () => <div>Performance View</div>;
const Settings = () => <div>Settings View</div>;

export default function App() {
  useEffect(() => {
    // Enable dark mode by default
    document.documentElement.classList.add('dark');
  }, []);

  return (
    <Router>
      <div className="dark">
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/portfolio" element={<Portfolio />} />
            <Route path="/research" element={<Research />} />
            <Route path="/trading" element={<Trading />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/performance" element={<Performance />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </div>
    </Router>
  );
} 