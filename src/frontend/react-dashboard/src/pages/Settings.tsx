import React from 'react'
import { CogIcon } from '@heroicons/react/24/outline'

const Settings = () => {
  return (
    <div className="h-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Settings</h1>
          <p className="text-gray-400">Manage your account and preferences</p>
        </div>
      </div>
      
      <div className="bg-secondary-300 rounded-xl p-8 text-center">
        <CogIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h2 className="text-xl font-medium text-white mb-2">Settings coming soon</h2>
        <p className="text-gray-400 max-w-md mx-auto">
          Account settings, security preferences, and notification controls will be available in the next update!
        </p>
      </div>
    </div>
  )
}

export default Settings 