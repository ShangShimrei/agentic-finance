import { useState } from 'react';
import { 
  UserCircleIcon, 
  ChevronDownIcon, 
  ArrowRightOnRectangleIcon,
  Cog6ToothIcon,
  UserPlusIcon
} from '@heroicons/react/24/outline';

interface UserProps {
  username: string;
  avatar?: string;
  userType: string;
}

const UserAccount: React.FC<UserProps> = ({ username, avatar, userType }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };
  
  const handleLogout = () => {
    console.log('User logged out');
    // Add actual logout logic here
    setIsMenuOpen(false);
  };
  
  const openAuthModal = (mode: 'login' | 'register') => {
    setAuthMode(mode);
    setShowAuthModal(true);
    setIsMenuOpen(false);
  };
  
  return (
    <div className="relative">
      {/* User profile button */}
      <button 
        onClick={toggleMenu}
        className="flex items-center space-x-3 focus:outline-none"
      >
        <div className="flex items-center">
          {avatar ? (
            <img 
              src={avatar} 
              alt={username} 
              className="h-8 w-8 rounded-full object-cover"
            />
          ) : (
            <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center">
              <UserCircleIcon className="h-6 w-6 text-white" />
            </div>
          )}
          <div className="ml-3">
            <p className="text-base font-medium text-white">{username}</p>
            <p className="text-sm text-gray-400">{userType}</p>
          </div>
        </div>
        <ChevronDownIcon className={`h-4 w-4 text-gray-400 transition-transform ${isMenuOpen ? 'rotate-180' : 'rotate-0'}`} />
      </button>
      
      {/* Dropdown menu */}
      {isMenuOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-secondary-200 rounded-md shadow-lg overflow-hidden z-50">
          <div className="py-1">
            <button
              onClick={() => openAuthModal('login')}
              className="w-full px-4 py-2 text-sm text-gray-300 hover:bg-secondary-100 flex items-center"
            >
              <ArrowRightOnRectangleIcon className="h-4 w-4 mr-2" />
              Sign In
            </button>
            <button
              onClick={() => openAuthModal('register')}
              className="w-full px-4 py-2 text-sm text-gray-300 hover:bg-secondary-100 flex items-center"
            >
              <UserPlusIcon className="h-4 w-4 mr-2" />
              Create Account
            </button>
            <button
              className="w-full px-4 py-2 text-sm text-gray-300 hover:bg-secondary-100 flex items-center"
            >
              <Cog6ToothIcon className="h-4 w-4 mr-2" />
              Settings
            </button>
            <button
              onClick={handleLogout}
              className="w-full px-4 py-2 text-sm text-primary-500 hover:bg-secondary-100 flex items-center"
            >
              <ArrowRightOnRectangleIcon className="h-4 w-4 mr-2" />
              Logout
            </button>
          </div>
        </div>
      )}
      
      {/* Auth Modal */}
      {showAuthModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-secondary-300 rounded-lg shadow-xl max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-white">
                {authMode === 'login' ? 'Sign In' : 'Create Account'}
              </h2>
              <button 
                onClick={() => setShowAuthModal(false)}
                className="text-gray-400 hover:text-white"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            {/* Auth Tabs */}
            <div className="flex border-b border-secondary-200 mb-6">
              <button 
                onClick={() => setAuthMode('login')}
                className={`py-2 px-4 font-medium ${authMode === 'login' ? 'text-primary-500 border-b-2 border-primary-500' : 'text-gray-400'}`}
              >
                Sign In
              </button>
              <button 
                onClick={() => setAuthMode('register')}
                className={`py-2 px-4 font-medium ${authMode === 'register' ? 'text-primary-500 border-b-2 border-primary-500' : 'text-gray-400'}`}
              >
                Create Account
              </button>
            </div>
            
            {/* Email/Password Form */}
            <form className="space-y-4">
              {authMode === 'register' && (
                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-1">Username</label>
                  <input 
                    type="text" 
                    id="username" 
                    className="w-full bg-secondary-200 rounded-md border border-secondary-100 focus:border-primary-500 focus:ring-0 text-white px-3 py-2"
                    placeholder="Enter your username"
                  />
                </div>
              )}
              
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-1">Email Address</label>
                <input 
                  type="email" 
                  id="email" 
                  className="w-full bg-secondary-200 rounded-md border border-secondary-100 focus:border-primary-500 focus:ring-0 text-white px-3 py-2"
                  placeholder="Enter your email"
                />
              </div>
              
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-1">Password</label>
                <input 
                  type="password" 
                  id="password" 
                  className="w-full bg-secondary-200 rounded-md border border-secondary-100 focus:border-primary-500 focus:ring-0 text-white px-3 py-2"
                  placeholder={authMode === 'login' ? "Enter your password" : "Create a password"}
                />
              </div>
              
              {authMode === 'register' && (
                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-1">Confirm Password</label>
                  <input 
                    type="password" 
                    id="confirmPassword" 
                    className="w-full bg-secondary-200 rounded-md border border-secondary-100 focus:border-primary-500 focus:ring-0 text-white px-3 py-2"
                    placeholder="Confirm your password"
                  />
                </div>
              )}
              
              <button 
                type="submit" 
                className="w-full bg-primary-500 hover:bg-primary-600 text-white font-medium py-2 px-4 rounded-md transition-colors"
              >
                {authMode === 'login' ? 'Sign In' : 'Create Account'}
              </button>
            </form>
            
            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-secondary-200"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-secondary-300 text-gray-400">Or continue with</span>
              </div>
            </div>
            
            {/* Social Logins */}
            <div className="grid grid-cols-3 gap-3">
              <button className="flex justify-center items-center py-2 px-4 border border-secondary-200 rounded-md hover:bg-secondary-200 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="text-white" viewBox="0 0 16 16">
                  <path d="M15.545 6.558a9.42 9.42 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.689 7.689 0 0 1 5.352 2.082l-2.284 2.284A4.347 4.347 0 0 0 8 3.166c-2.087 0-3.86 1.408-4.492 3.304a4.792 4.792 0 0 0 0 3.063h.003c.635 1.893 2.405 3.301 4.492 3.301 1.078 0 2.004-.276 2.722-.764h-.003a3.702 3.702 0 0 0 1.599-2.431H8v-3.08h7.545z"/>
                </svg>
              </button>
              <button className="flex justify-center items-center py-2 px-4 border border-secondary-200 rounded-md hover:bg-secondary-200 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="text-white" viewBox="0 0 16 16">
                  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                </svg>
              </button>
              <button className="flex justify-center items-center py-2 px-4 border border-secondary-200 rounded-md hover:bg-secondary-200 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="text-white" viewBox="0 0 16 16">
                  <path d="M11.182.008C11.148-.03 9.923.023 8.857 1.18c-1.066 1.156-.902 2.482-.878 2.516.024.034 1.52.087 2.475-1.258.955-1.345.762-2.391.728-2.43Zm3.314 11.733c-.048-.096-2.325-1.234-2.113-3.422.212-2.189 1.675-2.789 1.698-2.854.023-.065-.597-.79-1.254-1.157a3.692 3.692 0 0 0-1.563-.434c-.108-.003-.483-.095-1.254.116-.508.139-1.653.589-1.968.607-.316.018-1.256-.522-2.267-.665-.647-.125-1.333.131-1.824.328-.49.196-1.422.754-2.074 2.237-.652 1.482-.311 3.83-.067 4.56.244.729.625 1.924 1.273 2.796.576.984 1.34 1.667 1.659 1.899.319.232 1.219.386 1.843.067.502-.308 1.408-.485 1.766-.472.357.013 1.061.154 1.782.539.571.197 1.111.115 1.652-.105.541-.221 1.324-1.059 2.238-2.758.347-.79.505-1.217.473-1.282Z"/>
                  <path d="M11.182.008C11.148-.03 9.923.023 8.857 1.18c-1.066 1.156-.902 2.482-.878 2.516.024.034 1.52.087 2.475-1.258.955-1.345.762-2.391.728-2.43Zm3.314 11.733c-.048-.096-2.325-1.234-2.113-3.422.212-2.189 1.675-2.789 1.698-2.854.023-.065-.597-.79-1.254-1.157a3.692 3.692 0 0 0-1.563-.434c-.108-.003-.483-.095-1.254.116-.508.139-1.653.589-1.968.607-.316.018-1.256-.522-2.267-.665-.647-.125-1.333.131-1.824.328-.49.196-1.422.754-2.074 2.237-.652 1.482-.311 3.83-.067 4.56.244.729.625 1.924 1.273 2.796.576.984 1.34 1.667 1.659 1.899.319.232 1.219.386 1.843.067.502-.308 1.408-.485 1.766-.472.357.013 1.061.154 1.782.539.571.197 1.111.115 1.652-.105.541-.221 1.324-1.059 2.238-2.758.347-.79.505-1.217.473-1.282Z"/>
                </svg>
              </button>
            </div>
            
            {/* Switch mode links */}
            <div className="mt-6 text-center text-sm">
              {authMode === 'login' ? (
                <p className="text-gray-400">
                  Don't have an account? 
                  <button onClick={() => setAuthMode('register')} className="ml-1 text-primary-500 hover:text-primary-400">
                    Create one
                  </button>
                </p>
              ) : (
                <p className="text-gray-400">
                  Already have an account? 
                  <button onClick={() => setAuthMode('login')} className="ml-1 text-primary-500 hover:text-primary-400">
                    Sign in
                  </button>
                </p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserAccount; 