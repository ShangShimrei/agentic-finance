import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardLayout from './layouts/DashboardLayout'
import Dashboard from './pages/Dashboard'
import Assets from './pages/Assets'
import Market from './pages/Market'
import Portfolio from './pages/Portfolio'
import Transactions from './pages/Transactions'
import News from './pages/News'
import Blog from './pages/Blog'
import Announcements from './pages/Announcements'
import About from './pages/About'
import Settings from './pages/Settings'
import Help from './pages/Help'
import NotFound from './pages/NotFound'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/" element={<DashboardLayout />}>
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="assets" element={<Assets />} />
        <Route path="market" element={<Market />} />
        <Route path="portfolio" element={<Portfolio />} />
        <Route path="transactions" element={<Transactions />} />
        <Route path="news" element={<News />} />
        <Route path="blog" element={<Blog />} />
        <Route path="announcements" element={<Announcements />} />
        <Route path="about" element={<About />} />
        <Route path="settings" element={<Settings />} />
        <Route path="help" element={<Help />} />
      </Route>
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default App 