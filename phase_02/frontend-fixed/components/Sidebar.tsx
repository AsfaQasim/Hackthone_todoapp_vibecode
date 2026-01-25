'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Calendar, Settings, LogOut, User, Menu, X } from 'lucide-react';
import { motion } from 'framer-motion';

const Sidebar = () => {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { href: '/tasks', label: 'Tasks', icon: Calendar },

  ];

  const handleLogout = () => {
    // Remove the auth token from cookies
    document.cookie = 'auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
    // Redirect to login page
    window.location.href = '/login';
  };

  return (
    <>
      {/* Mobile menu button */}
      <button
        className="md:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-gray-800 text-gray-300 shadow-lg"
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
      >
        {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </button>

      {/* Sidebar overlay for mobile */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      <motion.aside
        initial={{ x: -300, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.3 }}
        className={`fixed inset-y-0 left-0 z-40 w-64 sm:w-72 bg-gray-900/90 backdrop-blur-lg border-r border-gray-800 transform ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
          } transition-transform duration-300 ease-in-out md:translate-x-0`}
      >
        <div className="flex flex-col items-start justify-start p-4 sm:p-6 min-h-[100px]">
          <h1 className="text-lg sm:text-2xl font-extrabold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            TODO_APP
          </h1>
          <p className="text-gray-400 text-xs sm:text-sm mt-1">Task Management</p>
        </div>


        <nav className="px-4 py-4 sm:py-6">
          <ul className="space-y-2">
            {navItems.map((item) => {
              const IconComponent = item.icon;
              const isActive = pathname === item.href;

              return (
                <li key={item.href}>
                  <Link href={item.href} onClick={() => setMobileMenuOpen(false)}>
                    <motion.div
                      whileHover={{ x: 4 }}
                      className={`flex items-center px-3 py-2.5 sm:px-4 sm:py-3 rounded-lg transition-all text-sm sm:text-base ${isActive
                        ? 'bg-cyan-900/30 text-cyan-400 border border-cyan-800/50'
                        : 'text-gray-300 hover:bg-gray-800/50'
                        }`}
                    >
                      <IconComponent className="h-4 w-4 sm:h-5 sm:w-5 mr-2 sm:mr-3" />
                      <span>{item.label}</span>
                    </motion.div>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-800">
          <button
            onClick={handleLogout}
            className="flex items-center w-full px-3 py-2.5 sm:px-4 sm:py-3 text-gray-300 hover:bg-gray-800/50 rounded-lg transition-all text-sm sm:text-base"
          >
            <LogOut className="h-4 w-4 sm:h-5 sm:w-5 mr-2 sm:mr-3" />
            <span>Logout</span>
          </button>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;