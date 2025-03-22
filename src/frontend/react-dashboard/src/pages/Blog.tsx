import React from 'react'
import { DocumentTextIcon } from '@heroicons/react/24/outline'

interface BlogPost {
  id: number;
  title: string;
  excerpt: string;
  author: string;
  date: string;
  readTime: string;
  category: string;
  image: string;
}

const Blog = () => {
  // Mock blog posts data
  const blogPosts: BlogPost[] = [
    {
      id: 1,
      title: "Understanding Market Volatility with AI Insights",
      excerpt: "How our AI agents process market signals to provide actionable insights during volatile trading periods.",
      author: "Shang Shimrei",
      date: "March 22, 2025",
      readTime: "8 min read",
      category: "Market Analysis",
      image: "https://images.unsplash.com/photo-1609921212029-bb5a28e60960?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80"
    },
    {
      id: 2,
      title: "The Future of Decentralized Finance and AI",
      excerpt: "Exploring the intersection of DeFi protocols and artificial intelligence for optimized trading strategies.",
      author: "Alex Johnson",
      date: "March 18, 2025",
      readTime: "12 min read",
      category: "DeFi",
      image: "https://images.unsplash.com/photo-1639322537228-f710d846310a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80"
    },
    {
      id: 3,
      title: "Building a Diversified Portfolio in 2025",
      excerpt: "Key considerations for balancing traditional and digital assets in today's complex market environment.",
      author: "Sarah Chen",
      date: "March 15, 2025",
      readTime: "10 min read",
      category: "Portfolio Management",
      image: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80"
    },
    {
      id: 4,
      title: "How Model Context Protocol is Revolutionizing Financial Analysis",
      excerpt: "A deep dive into our proprietary MCP technology and how it's changing the way AI understands financial markets.",
      author: "Shang Shimrei",
      date: "March 10, 2025",
      readTime: "15 min read",
      category: "Technology",
      image: "https://images.unsplash.com/photo-1639815188546-c43c240ff4df?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80"
    }
  ];

  return (
    <div className="h-full">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Blog</h1>
          <p className="text-xl text-gray-400">Insights, analyses, and updates from our team</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {blogPosts.map((post) => (
          <div 
            key={post.id} 
            className="bg-secondary-300 rounded-xl overflow-hidden hover:bg-secondary-200 transition-colors"
          >
            <div className="h-56 overflow-hidden">
              <img 
                src={post.image} 
                alt={post.title} 
                className="w-full h-full object-cover"
              />
            </div>
            <div className="p-6">
              <div className="flex justify-between items-center mb-3">
                <span className="bg-primary-500/20 text-primary-400 px-3 py-1 rounded-full text-base">
                  {post.category}
                </span>
                <span className="text-gray-400 text-base">{post.readTime}</span>
              </div>
              <h2 className="text-2xl font-semibold text-white mb-3">{post.title}</h2>
              <p className="text-lg text-gray-300 mb-4">{post.excerpt}</p>
              <div className="flex justify-between items-center">
                <div className="text-base text-gray-400">
                  By <span className="text-primary-400">{post.author}</span>
                </div>
                <div className="text-base text-gray-400">{post.date}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {blogPosts.length === 0 && (
        <div className="bg-secondary-300 rounded-xl p-10 text-center">
          <DocumentTextIcon className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h2 className="text-2xl font-medium text-white mb-2">No blog posts available</h2>
          <p className="text-lg text-gray-400 max-w-md mx-auto">
            Check back soon for insightful articles and updates from our team.
          </p>
        </div>
      )}
    </div>
  )
}

export default Blog 