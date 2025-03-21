import React from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import {
  ChartBarIcon,
  CoinIcon,
  GlobeAltIcon,
  WalletIcon,
  CreditCardIcon,
  NewspaperIcon,
  CogIcon,
  QuestionMarkCircleIcon
} from '../icons'

interface NavItem {
  name: string;
  path: string;
  icon: React.ReactNode;
}

const Sidebar = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  
  // Navigation items
  const navItems: NavItem[] = [
    {
      name: 'Dashboard',
      path: '/',
      icon: <ChartBarIcon className="w-5 h-5 mr-3" />
    },
    {
      name: 'Assets',
      path: '/assets',
      icon: <CoinIcon className="w-5 h-5 mr-3" />
    },
    {
      name: 'Market',
      path: '/market',
      icon: <GlobeAltIcon className="w-5 h-5 mr-3" />
    },
    {
      name: 'Portfolio',
      path: '/portfolio',
      icon: <WalletIcon className="w-5 h-5 mr-3" />
    },
    {
      name: 'Transactions',
      path: '/transactions',
      icon: <CreditCardIcon className="w-5 h-5 mr-3" />
    },
    {
      name: 'News',
      path: '/news',
      icon: <NewspaperIcon className="w-5 h-5 mr-3" />
    }
  ];
  
  // Utility navigation
  const utilityNavItems: NavItem[] = [
    {
      name: 'Settings',
      path: '/settings',
      icon: <CogIcon className="w-5 h-5 mr-3" />
    },
    {
      name: 'Help',
      path: '/help',
      icon: <QuestionMarkCircleIcon className="w-5 h-5 mr-3" />
    }
  ];
  
  return (
    <div className="bg-secondary-200 h-full w-60 p-4 flex flex-col">
      <div className="mb-8">
        <h1 className="text-xl font-bold text-white">YRS Finance</h1>
      </div>
      <div className="flex-1">
        <ul className="space-y-2">
          {navItems.map((item) => {
            const isActive = currentPath === item.path || 
                            (item.path !== '/' && currentPath.startsWith(item.path));
            
            return (
              <li key={item.name}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center text-gray-300 py-2 px-4 rounded-md ${
                      isActive ? 'bg-secondary-100 text-white' : 'hover:bg-secondary-100'
                    }`
                  }
                >
                  {item.icon}
                  <span>{item.name}</span>
                </NavLink>
              </li>
            );
          })}
        </ul>
      </div>
      <div>
        <ul className="space-y-2">
          {utilityNavItems.map((item) => {
            const isActive = currentPath === item.path;
            
            return (
              <li key={item.name}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center text-gray-300 py-2 px-4 rounded-md ${
                      isActive ? 'bg-secondary-100 text-white' : 'hover:bg-secondary-100'
                    }`
                  }
                >
                  {item.icon}
                  <span>{item.name}</span>
                </NavLink>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  )
}

export default Sidebar