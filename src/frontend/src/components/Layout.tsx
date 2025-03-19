import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  ChartBarIcon, 
  DocumentTextIcon,
  CurrencyDollarIcon,
  CogIcon,
  ArrowTrendingUpIcon,
  UserCircleIcon
} from '@heroicons/react/24/outline';
import clsx from 'clsx';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Portfolio', href: '/portfolio', icon: ChartBarIcon },
  { name: 'Research', href: '/research', icon: DocumentTextIcon },
  { name: 'Trading', href: '/trading', icon: CurrencyDollarIcon },
  { name: 'Agents', href: '/agents', icon: UserCircleIcon },
  { name: 'Performance', href: '/performance', icon: ArrowTrendingUpIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-dark-100">
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 w-64 bg-dark-200 border-r border-dark-300">
        {/* Logo */}
        <div className="flex h-16 items-center px-6">
          <h1 className="text-2xl font-bold text-white">
            Agentic Finance
          </h1>
        </div>

        {/* Navigation */}
        <nav className="mt-6 px-3">
          <div className="space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={clsx(
                    'nav-item',
                    isActive && 'active'
                  )}
                >
                  <item.icon
                    className={clsx(
                      'mr-3 h-6 w-6 flex-shrink-0',
                      isActive
                        ? 'text-white'
                        : 'text-gray-400 group-hover:text-white'
                    )}
                  />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </nav>
      </div>

      {/* Main content */}
      <div className="pl-64">
        {/* Header */}
        <header className="bg-dark-200 border-b border-dark-300">
          <div className="h-16 flex items-center px-6">
            <h2 className="text-lg font-medium text-white">
              {navigation.find((item) => item.href === location.pathname)?.name || 'Dashboard'}
            </h2>
          </div>
        </header>

        {/* Content */}
        <main className="py-6 px-6">
          <div className="mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
} 