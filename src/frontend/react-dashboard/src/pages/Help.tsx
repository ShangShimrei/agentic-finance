import React from 'react'
import { QuestionMarkCircleIcon } from '@heroicons/react/24/outline'

const Help = () => {
  return (
    <div className="h-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Help Center</h1>
          <p className="text-gray-400">Guides and resources to help you get the most out of the platform</p>
        </div>
      </div>
      
      <div className="bg-secondary-300 rounded-xl p-8 text-center">
        <QuestionMarkCircleIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h2 className="text-xl font-medium text-white mb-2">Help resources coming soon</h2>
        <p className="text-gray-400 max-w-md mx-auto">
          User guides, FAQ sections, and support resources will be available in the next update!
        </p>
      </div>
    </div>
  )
}

export default Help 