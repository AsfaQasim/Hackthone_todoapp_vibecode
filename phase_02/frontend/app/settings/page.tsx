'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Sidebar from '../../components/Sidebar';
import { Card, CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import PageTransition from '../../components/PageTransition';

export default function SettingsPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [theme, setTheme] = useState('dark');
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in by checking for auth token in cookies
    const tokenExists = document.cookie
      .split('; ')
      .find(row => row.startsWith('auth_token='));

    if (!tokenExists) {
      router.push('/login');
    } else {
      setIsLoggedIn(true);
    }
  }, [router]);

  const handleSaveSettings = () => {
    // In a real app, you would save settings to the backend
    console.log('Settings saved:', { notifications, theme });
    alert('Settings saved successfully!');
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8 text-center">
          <h2 className="text-2xl font-bold text-gray-200">Please log in</h2>
          <p className="text-gray-400">You need to be logged in to access settings</p>
          <Button
            onClick={() => router.push('/login')}
            variant="primary"
          >
            Go to Login
          </Button>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="flex min-h-screen">
        <Sidebar />
        
        <div className="flex-1 md:ml-64 transition-all duration-300">
          <div className="max-w-4xl mx-auto px-4 py-8">
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mb-10 text-center"
            >
              <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                Settings
              </h1>
              <p className="text-gray-400 mt-2">Configure your account preferences</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="space-y-6"
            >
              <Card>
                <CardContent className="p-0">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-white mb-4">Notification Preferences</h2>
                    
                    <div className="flex items-center justify-between py-3 border-b border-gray-800">
                      <div>
                        <h3 className="font-medium text-gray-200">Email Notifications</h3>
                        <p className="text-sm text-gray-400">Receive email updates about your tasks</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={notifications}
                          onChange={() => setNotifications(!notifications)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-cyan-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-600"></div>
                      </label>
                    </div>
                    
                    <div className="flex items-center justify-between py-3">
                      <div>
                        <h3 className="font-medium text-gray-200">Push Notifications</h3>
                        <p className="text-sm text-gray-400">Receive push notifications on your devices</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={notifications}
                          onChange={() => setNotifications(!notifications)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-cyan-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-600"></div>
                      </label>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-0">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-white mb-4">Appearance</h2>
                    
                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-300 mb-2">Theme</label>
                      <div className="grid grid-cols-3 gap-4">
                        <button
                          onClick={() => setTheme('light')}
                          className={`p-4 rounded-lg border ${
                            theme === 'light'
                              ? 'border-cyan-500 bg-cyan-900/20'
                              : 'border-gray-700 bg-gray-800/50'
                          }`}
                        >
                          <div className="text-center">
                            <div className="mx-auto bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16 mb-2" />
                            <span className="text-gray-300">Light</span>
                          </div>
                        </button>
                        
                        <button
                          onClick={() => setTheme('dark')}
                          className={`p-4 rounded-lg border ${
                            theme === 'dark'
                              ? 'border-cyan-500 bg-cyan-900/20'
                              : 'border-gray-700 bg-gray-800/50'
                          }`}
                        >
                          <div className="text-center">
                            <div className="mx-auto bg-gray-800 border-2 border-dashed rounded-xl w-16 h-16 mb-2" />
                            <span className="text-gray-300">Dark</span>
                          </div>
                        </button>
                        
                        <button
                          onClick={() => setTheme('system')}
                          className={`p-4 rounded-lg border ${
                            theme === 'system'
                              ? 'border-cyan-500 bg-cyan-900/20'
                              : 'border-gray-700 bg-gray-800/50'
                          }`}
                        >
                          <div className="text-center">
                            <div className="mx-auto bg-gradient-to-br from-gray-800 to-gray-900 border-2 border-dashed rounded-xl w-16 h-16 mb-2" />
                            <span className="text-gray-300">System</span>
                          </div>
                        </button>
                      </div>
                    </div>
                    
                    <Button 
                      variant="primary" 
                      className="w-full"
                      onClick={handleSaveSettings}
                    >
                      Save Settings
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}