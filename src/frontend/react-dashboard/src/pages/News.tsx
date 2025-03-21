import React from 'react'
import { NewspaperIcon } from '@heroicons/react/24/outline'

const News = () => {
  return (
    <div className="h-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">News</h1>
          <p className="text-gray-400">Financial news and market insights</p>
        </div>
      </div>
      
      <div className="bg-secondary-300 rounded-xl p-8 text-center">
        <NewspaperIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h2 className="text-xl font-medium text-white mb-2">News coming soon</h2>
        <p className="text-gray-400 max-w-md mx-auto">
          Stay tuned for the latest market news, financial updates, and expert insights. Coming in the next update!
        </p>
      </div>
    </div>
  )
}

export default News 