import React from 'react'
import { Link } from 'react-router-dom'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

const NotFound = () => {
  return (
    <div className="h-screen bg-secondary-400 flex items-center justify-center p-6">
      <div className="bg-secondary-300 rounded-xl p-8 max-w-md w-full text-center">
        <ExclamationTriangleIcon className="mx-auto h-16 w-16 text-yellow-500 mb-4" />
        <h1 className="text-3xl font-bold text-white mb-2">404 - Page Not Found</h1>
        <p className="text-gray-400 mb-6">
          The page you are looking for doesn't exist or has been moved.
        </p>
        <Link 
          to="/" 
          className="inline-block bg-primary-500 hover:bg-primary-600 text-white font-medium py-2 px-6 rounded-md transition-colors"
        >
          Return to Dashboard
        </Link>
      </div>
    </div>
  )
}

export default NotFound 