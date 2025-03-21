import { createHashRouter } from 'react-router-dom'
import Dashboard from '../pages/Dashboard'
import Assets from '../pages/Assets'
import Market from '../pages/Market'
import Portfolio from '../pages/Portfolio'
import Transactions from '../pages/Transactions'
import News from '../pages/News'
import Settings from '../pages/Settings'
import Help from '../pages/Help'
import DashboardLayout from '../layouts/DashboardLayout'

const router = createHashRouter([
  {
    path: '/',
    element: <DashboardLayout />,
    children: [
      {
        path: '/',
        element: <Dashboard />,
      },
      {
        path: '/assets',
        element: <Assets />,
      },
      {
        path: '/market',
        element: <Market />,
      },
      {
        path: '/portfolio',
        element: <Portfolio />,
      },
      {
        path: '/transactions',
        element: <Transactions />,
      },
      {
        path: '/news',
        element: <News />,
      },
      {
        path: '/settings',
        element: <Settings />,
      },
      {
        path: '/help',
        element: <Help />,
      },
    ],
  },
])

export default router 