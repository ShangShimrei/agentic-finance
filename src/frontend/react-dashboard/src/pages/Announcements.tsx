import React from 'react'
import { SpeakerWaveIcon, ClockIcon, CalendarIcon } from '@heroicons/react/24/outline'

interface Announcement {
  id: number;
  title: string;
  content: string;
  date: string;
  time: string;
  type: 'product' | 'feature' | 'update' | 'maintenance' | 'security';
  priority: 'high' | 'medium' | 'low';
}

const Announcements = () => {
  // Mock announcements data
  const announcements: Announcement[] = [
    {
      id: 1,
      title: "Platform Update: Version 2.5 Released",
      content: "We're excited to announce the release of version 2.5, featuring enhanced AI agent capabilities, improved chart visualizations, and better portfolio tracking. Update your application to access these new features.",
      date: "March 22, 2025",
      time: "09:00 AM",
      type: "update",
      priority: "high"
    },
    {
      id: 2,
      title: "New Feature: Sentiment Analysis for Crypto Assets",
      content: "Our AI agents now incorporate social media sentiment analysis for major cryptocurrencies. This feature helps you gauge market sentiment before making investment decisions.",
      date: "March 20, 2025",
      time: "02:30 PM",
      type: "feature",
      priority: "medium"
    },
    {
      id: 3,
      title: "Scheduled Maintenance: March 25th",
      content: "We will be performing scheduled maintenance on our servers on March 25th from 2:00 AM to 4:00 AM UTC. During this time, the platform may experience brief interruptions in service.",
      date: "March 25, 2025",
      time: "02:00 AM",
      type: "maintenance",
      priority: "medium"
    },
    {
      id: 4,
      title: "Security Alert: Enhanced Authentication Measures",
      content: "To better protect your account, we've added two-factor authentication support. We strongly recommend enabling this feature in your account settings for additional security.",
      date: "March 18, 2025",
      time: "11:15 AM",
      type: "security",
      priority: "high"
    },
    {
      id: 5,
      title: "New Partnership: Integration with TradingView",
      content: "We're thrilled to announce our partnership with TradingView, allowing seamless chart analysis integration within our platform. This collaboration brings professional-grade charting tools to your fingertips.",
      date: "March 15, 2025",
      time: "10:00 AM",
      type: "product",
      priority: "medium"
    }
  ];

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-400 bg-red-400/10';
      case 'medium':
        return 'text-yellow-400 bg-yellow-400/10';
      case 'low':
        return 'text-green-400 bg-green-400/10';
      default:
        return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'product':
        return 'text-purple-400 bg-purple-400/10';
      case 'feature':
        return 'text-blue-400 bg-blue-400/10';
      case 'update':
        return 'text-green-400 bg-green-400/10';
      case 'maintenance':
        return 'text-orange-400 bg-orange-400/10';
      case 'security':
        return 'text-red-400 bg-red-400/10';
      default:
        return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getTypeLabel = (type: string) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  return (
    <div className="h-full">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Announcements</h1>
          <p className="text-xl text-gray-400">Important updates and news about our platform</p>
        </div>
      </div>
      
      <div className="space-y-6">
        {announcements.map((announcement) => (
          <div 
            key={announcement.id} 
            className="bg-secondary-300 rounded-xl p-6 hover:bg-secondary-200 transition-colors"
          >
            <div className="flex flex-wrap items-center justify-between mb-4">
              <h2 className="text-2xl font-semibold text-white">{announcement.title}</h2>
              <div className="flex space-x-3 mt-2 sm:mt-0">
                <span className={`px-3 py-1 rounded-full text-base ${getPriorityColor(announcement.priority)}`}>
                  {announcement.priority.toUpperCase()} Priority
                </span>
                <span className={`px-3 py-1 rounded-full text-base ${getTypeColor(announcement.type)}`}>
                  {getTypeLabel(announcement.type)}
                </span>
              </div>
            </div>
            
            <p className="text-lg text-gray-300 mb-4">
              {announcement.content}
            </p>
            
            <div className="flex flex-wrap items-center text-base text-gray-400">
              <div className="flex items-center mr-6">
                <CalendarIcon className="h-5 w-5 mr-2 text-primary-400" />
                {announcement.date}
              </div>
              <div className="flex items-center">
                <ClockIcon className="h-5 w-5 mr-2 text-primary-400" />
                {announcement.time}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {announcements.length === 0 && (
        <div className="bg-secondary-300 rounded-xl p-10 text-center">
          <SpeakerWaveIcon className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h2 className="text-2xl font-medium text-white mb-2">No announcements available</h2>
          <p className="text-lg text-gray-400 max-w-md mx-auto">
            Check back soon for important updates and information about our platform.
          </p>
        </div>
      )}
    </div>
  )
}

export default Announcements 