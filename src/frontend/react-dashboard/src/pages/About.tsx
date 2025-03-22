import React from 'react'
import { 
  UserGroupIcon, 
  DocumentTextIcon, 
  InformationCircleIcon, 
  EnvelopeIcon 
} from '@heroicons/react/24/outline'

// Social media icons
const FacebookIcon = () => (
  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
    <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
  </svg>
)

const TwitterIcon = () => (
  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
  </svg>
)

const InstagramIcon = () => (
  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
    <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
  </svg>
)

const LinkedInIcon = () => (
  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
  </svg>
)

const TelegramIcon = () => (
  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
    <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.96 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
  </svg>
)

const RedditIcon = () => (
  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
    <path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z" />
  </svg>
)

const About = () => {
  const socialLinks = [
    { name: 'Facebook', icon: <FacebookIcon />, url: 'https://facebook.com' },
    { name: 'Twitter', icon: <TwitterIcon />, url: 'https://twitter.com' },
    { name: 'Instagram', icon: <InstagramIcon />, url: 'https://instagram.com' },
    { name: 'LinkedIn', icon: <LinkedInIcon />, url: 'https://linkedin.com' },
    { name: 'Telegram', icon: <TelegramIcon />, url: 'https://telegram.org' },
    { name: 'Reddit', icon: <RedditIcon />, url: 'https://reddit.com' },
  ]

  const footerLinks = [
    { name: 'Press', url: '#' },
    { name: 'Terms', url: '#' },
    { name: 'Legal', url: '#' },
    { name: 'Notices', url: '#' },
    { name: 'Downloads', url: '#' },
  ]

  return (
    <div className="h-full">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">About Us</h1>
          <p className="text-xl text-gray-400">Our mission, vision, and team</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Vision & Mission Section */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-secondary-300 rounded-xl p-6">
            <div className="flex items-center mb-4">
              <UserGroupIcon className="h-6 w-6 text-primary-500 mr-2" />
              <h2 className="text-2xl font-medium text-white">Vision Statement</h2>
            </div>
            <p className="text-lg text-gray-300 mb-4">
              "To democratize finance by harnessing the power of AI—making sophisticated market insights and investment strategies accessible to everyone, from seasoned professionals to everyday investors."
            </p>
          </div>
          
          <div className="bg-secondary-300 rounded-xl p-6">
            <div className="flex items-center mb-4">
              <DocumentTextIcon className="h-6 w-6 text-primary-500 mr-2" />
              <h2 className="text-2xl font-medium text-white">Mission Statement</h2>
            </div>
            <p className="text-lg text-gray-300">
              "Our mission is to build a modular, AI-driven platform that transforms real-time market data into actionable financial intelligence. By leveraging specialized AI agents and innovative tools like our Model Context Protocol, we streamline risk management, portfolio optimization, and trading decisions. We are dedicated to empowering individuals and organizations to make informed, transparent, and effective financial decisions—opening the world of finance to all."
            </p>
          </div>
        </div>
        
        {/* Developer Info */}
        <div className="space-y-6">
          <div className="bg-secondary-300 rounded-xl p-6">
            <div className="flex items-center mb-4">
              <InformationCircleIcon className="h-6 w-6 text-primary-500 mr-2" />
              <h2 className="text-2xl font-medium text-white">Developer</h2>
            </div>
            <div className="flex flex-col items-center text-center mb-4">
              <div className="h-24 w-24 bg-primary-500/20 rounded-full flex items-center justify-center mb-3">
                <span className="text-3xl font-bold text-primary-500">SS</span>
              </div>
              <h3 className="text-xl font-medium text-white">Shang Shimrei</h3>
              <div className="flex items-center mt-2 text-primary-400 text-base">
                <EnvelopeIcon className="h-5 w-5 mr-1" />
                <a href="mailto:shangshimrei@gmail.com" className="hover:text-primary-300">
                  shangshimrei@gmail.com
                </a>
              </div>
            </div>
          </div>
          
          {/* Community Links */}
          <div className="bg-secondary-300 rounded-xl p-6">
            <h2 className="text-2xl font-medium text-white mb-4">Connect With Us</h2>
            <div className="grid grid-cols-3 gap-4">
              {socialLinks.map((link) => (
                <a 
                  key={link.name}
                  href={link.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex flex-col items-center text-gray-400 hover:text-primary-500 transition-colors"
                >
                  <div className="p-3 rounded-full bg-secondary-200 hover:bg-secondary-100 mb-2">
                    {link.icon}
                  </div>
                  <span className="text-sm">{link.name}</span>
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      {/* Footer Links */}
      <div className="mt-10 pt-6 border-t border-secondary-200">
        <div className="flex flex-wrap justify-center gap-6">
          {footerLinks.map((link) => (
            <a 
              key={link.name}
              href={link.url}
              className="text-gray-400 hover:text-primary-500 text-base"
            >
              {link.name}
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}

export default About 