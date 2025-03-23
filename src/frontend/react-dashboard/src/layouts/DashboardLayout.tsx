import { useState, useRef, useEffect } from 'react'
import { Outlet, NavLink } from 'react-router-dom'
import { 
  HomeIcon, 
  CurrencyDollarIcon, 
  ChartBarIcon, 
  BriefcaseIcon, 
  CogIcon,
  BellIcon,
  MagnifyingGlassIcon,
  NewspaperIcon,
  UserGroupIcon,
  DocumentTextIcon,
  SpeakerWaveIcon,
  ChatBubbleLeftRightIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import ChatAssistant from '../components/ChatAssistant'
import UserAccount from '../components/UserAccount'

const navigation = [
  { name: 'Dashboard', href: '/', current: true },
  { name: 'Portfolio', href: '/portfolio', current: false },
  { name: 'Assets', href: '/assets', current: false },
  { name: 'Market', href: '/market', current: false },
];

const DashboardLayout = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [chatOpen, setChatOpen] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  
  const toggleChat = () => {
    setChatOpen(!chatOpen)
    console.log("Chat toggled:", !chatOpen)
  }

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  return (
    <div className="flex h-screen bg-secondary-400 relative">
      {/* Mobile Menu Button - Only shown on mobile */}
      <button 
        onClick={toggleSidebar}
        className="md:hidden absolute top-4 left-4 z-50 p-2 rounded-md bg-secondary-300 text-white"
      >
        {sidebarOpen ? (
          <XMarkIcon className="h-6 w-6" />
        ) : (
          <Bars3Icon className="h-6 w-6" />
        )}
      </button>

      {/* Sidebar - Hidden by default on mobile, shown when toggled */}
      <div className={`
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'} 
        transform transition-transform duration-300 ease-in-out
        fixed md:relative z-40 w-64 bg-secondary-300 border-r border-secondary-200 flex flex-col h-full
      `}>
        <div className="flex items-center px-6 py-4 h-16 border-b border-secondary-200">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 bg-primary-500 rounded-md flex items-center justify-center">
              <span className="text-white font-bold">YRS</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Finance</h1>
          </div>
        </div>
        
        <div className="flex flex-col flex-grow justify-between">
          <nav className="mt-6 px-3 space-y-1 text-base">
            <NavLink to="/" className={({isActive}) => 
              `menu-item group ${isActive ? 'active' : ''}`
            } end>
              <HomeIcon className="sidebar-icon mr-3" />
              <span>Dashboard</span>
            </NavLink>
            
            <NavLink to="/assets" className={({isActive}) => 
              `menu-item group ${isActive ? 'active' : ''}`
            }>
              <CurrencyDollarIcon className="sidebar-icon mr-3" />
              <span>Assets</span>
            </NavLink>
            
            <NavLink to="/market" className={({isActive}) => 
              `menu-item group ${isActive ? 'active' : ''}`
            }>
              <ChartBarIcon className="sidebar-icon mr-3" />
              <span>Market</span>
              <span className="ml-auto bg-primary-500 px-2 py-0.5 text-xs rounded-full text-white">New</span>
            </NavLink>
            
            <NavLink to="/portfolio" className={({isActive}) => 
              `menu-item group ${isActive ? 'active' : ''}`
            }>
              <BriefcaseIcon className="sidebar-icon mr-3" />
              <span>Portfolio</span>
            </NavLink>
            
            <NavLink to="/news" className={({isActive}) => 
              `menu-item group ${isActive ? 'active' : ''}`
            }>
              <NewspaperIcon className="sidebar-icon mr-3" />
              <span>News</span>
            </NavLink>
            
            <NavLink to="/blog" className={({isActive}) => 
              `menu-item group ${isActive ? 'active' : ''}`
            }>
              <DocumentTextIcon className="sidebar-icon mr-3" />
              <span>Blog</span>
            </NavLink>
            
            <NavLink to="/announcements" className={({isActive}) => 
              `menu-item group ${isActive ? 'active' : ''}`
            }>
              <SpeakerWaveIcon className="sidebar-icon mr-3" />
              <span>Announcements</span>
            </NavLink>
            
            <NavLink to="/about" className={({isActive}) => 
              `menu-item group ${isActive ? 'active' : ''}`
            }>
              <UserGroupIcon className="sidebar-icon mr-3" />
              <span>About Us</span>
            </NavLink>
            
            <div className="menu-item group">
              <CogIcon className="sidebar-icon mr-3" />
              <span>Settings</span>
            </div>
          </nav>
          
          {/* Ask Yuki button at bottom of sidebar */}
          <div className="px-3 pb-6">
            <div 
              className="flex items-center justify-center bg-primary-500 hover:bg-primary-600 text-white rounded-lg py-4 px-4 cursor-pointer shadow-md transition-colors"
              onClick={toggleChat}
            >
              <ChatBubbleLeftRightIcon className="h-6 w-6 text-white mr-3" />
              <span className="text-lg font-semibold">Ask Yuki</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="h-16 bg-secondary-300 border-b border-secondary-200 flex items-center justify-between px-6">
          <div className="hidden md:flex items-center bg-secondary-200 rounded-md px-3 py-1.5 w-96">
            <MagnifyingGlassIcon className="h-5 w-5 text-gray-400 mr-2" />
            <input 
              type="text" 
              placeholder="Search..." 
              className="bg-transparent border-none outline-none text-gray-300 w-full"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          {/* For mobile - centered title */}
          <div className="md:hidden flex-1 flex justify-center">
            <h1 className="text-xl font-bold text-white">YRS Finance</h1>
          </div>
          
          <div className="flex items-center">
            <button className="p-2 rounded-md relative">
              <BellIcon className="h-6 w-6 text-gray-400" />
              <span className="absolute top-1 right-1 h-2 w-2 bg-primary-500 rounded-full"></span>
            </button>
            
            <div className="ml-4">
              <UserAccount 
                username="Shimrei" 
                userType="Premium Account" 
                avatar="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
              />
            </div>
          </div>
        </header>
        
        {/* Page Content */}
        <main className="flex-1 overflow-auto p-3 md:p-6 bg-secondary-400">
          <Outlet />
        </main>
      </div>
      
      {/* Overlay for mobile sidebar */}
      {sidebarOpen && (
        <div 
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={toggleSidebar}
        ></div>
      )}
      
      {/* Chat component */}
      <ChatAssistant isOpen={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  )
}

export default DashboardLayout 