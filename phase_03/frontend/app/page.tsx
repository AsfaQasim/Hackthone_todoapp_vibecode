'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { ArrowRight, CheckCircle, Zap, Shield, Sparkles, TrendingUp, Users } from 'lucide-react';
import PageTransition from '../components/PageTransition';
import { useAuth } from '../contexts/AuthContext';

export default function Home() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="mx-auto mb-4"
          >
            <Sparkles className="h-12 w-12 text-cyan-400" />
          </motion.div>
          <p className="text-gray-300">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="min-h-screen flex flex-col relative overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.5, 0.3],
            }}
            transition={{ duration: 8, repeat: Infinity }}
            className="absolute top-20 left-10 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1.2, 1, 1.2],
              opacity: [0.3, 0.5, 0.3],
            }}
            transition={{ duration: 10, repeat: Infinity }}
            className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"
          />
        </div>

        <div className="flex-grow flex items-center justify-center px-4 py-12 relative z-10">
          <div className="max-w-6xl mx-auto text-center">
            {/* Hero Section */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="mb-12"
            >
              <motion.div
                animate={{
                  y: [0, -10, 0],
                }}
                transition={{ duration: 3, repeat: Infinity }}
                className="inline-block mb-6"
              >
                <Sparkles className="h-16 w-16 text-cyan-400 mx-auto" />
              </motion.div>

              <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold mb-6">
                <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
                  VibeCode
                </span>
                <br />
                <span className="text-white">Task Manager</span>
              </h1>

              <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-4">
                The premium task management solution designed for professionals
              </p>
              <p className="text-lg text-gray-400 max-w-2xl mx-auto">
                Boost productivity with AI-powered task management, beautiful UI, and seamless synchronization
              </p>
            </motion.div>

            {/* CTA Buttons */}
            {user ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="flex flex-col sm:flex-row justify-center gap-4 mb-16"
              >
                <Link href="/dashboard" className="w-full sm:w-auto">
                  <motion.button
                    whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(6, 182, 212, 0.5)" }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-semibold rounded-2xl hover:from-cyan-500 hover:to-blue-500 transition-all shadow-lg shadow-cyan-500/30 flex items-center justify-center gap-2"
                  >
                    <Sparkles className="h-5 w-5" />
                    Go to Dashboard
                    <ArrowRight className="h-5 w-5" />
                  </motion.button>
                </Link>

                <Link href="/tasks" className="w-full sm:w-auto">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full sm:w-auto px-8 py-4 glass-card text-white font-semibold rounded-2xl hover-glow flex items-center justify-center gap-2"
                  >
                    Manage Tasks
                    <ArrowRight className="h-5 w-5" />
                  </motion.button>
                </Link>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="flex flex-col sm:flex-row justify-center gap-4 mb-16"
              >
                <Link href="/login" className="w-full sm:w-auto">
                  <motion.button
                    whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(6, 182, 212, 0.5)" }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-semibold rounded-2xl hover:from-cyan-500 hover:to-blue-500 transition-all shadow-lg shadow-cyan-500/30 flex items-center justify-center gap-2"
                  >
                    <Sparkles className="h-5 w-5" />
                    Get Started
                    <ArrowRight className="h-5 w-5" />
                  </motion.button>
                </Link>

                <Link href="/signup" className="w-full sm:w-auto">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full sm:w-auto px-8 py-4 glass-card text-white font-semibold rounded-2xl hover-glow flex items-center justify-center gap-2"
                  >
                    Create Account
                    <ArrowRight className="h-5 w-5" />
                  </motion.button>
                </Link>
              </motion.div>
            )}

            {/* Feature Cards */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto"
            >
              {[
                {
                  icon: Zap,
                  title: 'Lightning Fast',
                  description: 'Optimized performance with instant task updates and real-time sync',
                  gradient: 'from-yellow-500/20 to-orange-500/10',
                  iconColor: 'text-yellow-400',
                  borderColor: 'border-yellow-500/30'
                },
                {
                  icon: Shield,
                  title: 'Secure by Design',
                  description: 'Enterprise-grade security with JWT authentication and encrypted data',
                  gradient: 'from-green-500/20 to-emerald-500/10',
                  iconColor: 'text-green-400',
                  borderColor: 'border-green-500/30'
                },
                {
                  icon: CheckCircle,
                  title: 'Always Synced',
                  description: 'Access your tasks from anywhere with seamless cloud synchronization',
                  gradient: 'from-cyan-500/20 to-blue-500/10',
                  iconColor: 'text-cyan-400',
                  borderColor: 'border-cyan-500/30'
                },
                {
                  icon: Sparkles,
                  title: 'AI-Powered',
                  description: 'Smart task suggestions and intelligent organization with AI assistant',
                  gradient: 'from-purple-500/20 to-pink-500/10',
                  iconColor: 'text-purple-400',
                  borderColor: 'border-purple-500/30'
                },
                {
                  icon: TrendingUp,
                  title: 'Track Progress',
                  description: 'Visualize your productivity with detailed analytics and insights',
                  gradient: 'from-blue-500/20 to-indigo-500/10',
                  iconColor: 'text-blue-400',
                  borderColor: 'border-blue-500/30'
                },
                {
                  icon: Users,
                  title: 'Team Ready',
                  description: 'Built for collaboration with multi-user support and sharing',
                  gradient: 'from-pink-500/20 to-rose-500/10',
                  iconColor: 'text-pink-400',
                  borderColor: 'border-pink-500/30'
                }
              ].map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                  className={`glass-card rounded-2xl p-6 hover-glow ${feature.borderColor}`}
                >
                  <motion.div
                    whileHover={{ rotate: 360, scale: 1.2 }}
                    transition={{ duration: 0.6 }}
                    className={`w-14 h-14 bg-gradient-to-br ${feature.gradient} rounded-xl flex items-center justify-center mb-4 mx-auto`}
                  >
                    <feature.icon className={`h-7 w-7 ${feature.iconColor}`} />
                  </motion.div>
                  <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </div>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="py-8 text-center text-gray-500 text-sm relative z-10"
        >
          <p className="flex items-center justify-center gap-2">
            © {new Date().getFullYear()} VibeCode. Crafted with
            <motion.span
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            >
              ❤️
            </motion.span>
            for productivity
          </p>
        </motion.footer>
      </div>
    </PageTransition>
  );
}
