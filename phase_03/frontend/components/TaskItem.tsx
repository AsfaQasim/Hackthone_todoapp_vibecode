'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trash2, CheckCircle, Circle, Clock, Sparkles } from 'lucide-react';

interface Task {
  id: string | number;  // Support both UUID (string) and legacy number IDs
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  user_id?: number | string;  // Optional field that may be present
}

interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: string | number) => void;
  onDelete: (id: string | number) => void;
  isUpdating?: boolean;
  isDeleting?: boolean;
}

const TaskItem = ({
  task,
  onToggleComplete,
  onDelete,
  isUpdating = false,
  isDeleting = false
}: TaskItemProps) => {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleToggle = () => {
    if (!isUpdating) {
      onToggleComplete(task.id);
      
      // Simple celebration animation when task is completed
      if (!task.completed) {
        // You can add confetti here later when you have space
        console.log('Task completed! 🎉');
      }
    }
  };

  const handleDelete = () => {
    console.log('🗑️ TaskItem handleDelete called for task:', task.id);
    console.log('Task details:', { id: task.id, type: typeof task.id });
    
    if (task.id) {
      console.log('✅ Valid task ID, calling onDelete');
      onDelete(task.id);
      setShowDeleteConfirm(false);
    } else {
      console.error('❌ Invalid task ID:', task.id);
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: -50, scale: 0.9 }}
      animate={{ 
        opacity: 1, 
        x: 0, 
        scale: 1,
        rotateX: 0
      }}
      exit={{ 
        opacity: 0, 
        x: 100, 
        scale: 0.8,
        transition: { duration: 0.3 }
      }}
      whileHover={{ 
        scale: 1.02,
        transition: { duration: 0.2 }
      }}
      transition={{ 
        type: "spring",
        stiffness: 300,
        damping: 25
      }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className={`relative p-5 rounded-2xl border backdrop-blur-xl transition-all duration-300 overflow-hidden ${
        task.completed
          ? 'bg-gradient-to-br from-green-900/20 to-emerald-900/10 border-green-500/40 shadow-lg shadow-green-500/20'
          : 'bg-gradient-to-br from-white/10 to-white/5 border-white/20 hover:border-cyan-400/50 hover:shadow-xl hover:shadow-cyan-500/20'
      }`}
    >
      {/* Animated background gradient */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 via-blue-500/10 to-purple-500/10"
        animate={{
          opacity: isHovered ? 1 : 0,
          scale: isHovered ? 1 : 0.8
        }}
        transition={{ duration: 0.3 }}
      />

      {/* Sparkle effect for completed tasks */}
      {task.completed && (
        <motion.div
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          className="absolute top-2 right-2"
        >
          <Sparkles className="h-5 w-5 text-yellow-400" />
        </motion.div>
      )}

      <div className="relative flex justify-between items-start">
        <div className="flex items-start space-x-4 flex-1">
          <motion.button
            whileHover={{ scale: 1.15, rotate: 5 }}
            whileTap={{ scale: 0.85 }}
            onClick={handleToggle}
            disabled={isUpdating}
            className="mt-1 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-full relative"
            aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          >
            <AnimatePresence mode="wait">
              {task.completed ? (
                <motion.div
                  key="completed"
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  exit={{ scale: 0, rotate: 180 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  <CheckCircle className="h-7 w-7 text-green-400 drop-shadow-lg" />
                </motion.div>
              ) : (
                <motion.div
                  key="incomplete"
                  initial={{ scale: 0, rotate: 180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  exit={{ scale: 0, rotate: -180 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  <Circle className="h-7 w-7 text-gray-400 hover:text-cyan-400 transition-colors" />
                </motion.div>
              )}
            </AnimatePresence>
          </motion.button>

          <div className="flex-1 min-w-0">
            <motion.h3
              className={`font-semibold text-lg ${
                task.completed
                  ? 'text-gray-400 line-through'
                  : 'text-white'
              }`}
              animate={{
                color: task.completed ? '#9CA3AF' : '#FFFFFF',
                x: task.completed ? 5 : 0
              }}
              transition={{ duration: 0.3 }}
            >
              {task.title}
            </motion.h3>

            <AnimatePresence>
              {task.description && (
                <motion.p
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className={`mt-2 text-sm break-words ${
                    task.completed ? 'text-gray-500' : 'text-gray-300'
                  }`}
                >
                  {task.description}
                </motion.p>
              )}
            </AnimatePresence>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="flex items-center gap-2 text-xs text-gray-500 mt-3"
            >
              <Clock className="h-3 w-3" />
              <span>{formatDate(task.created_at)}</span>
            </motion.div>
          </div>
        </div>

        <div className="flex space-x-2 ml-4">
          <AnimatePresence mode="wait">
            {!showDeleteConfirm ? (
              <motion.button
                key="delete-btn"
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0 }}
                whileHover={{ scale: 1.2, rotate: 10 }}
                whileTap={{ scale: 0.8 }}
                onClick={() => setShowDeleteConfirm(true)}
                className="text-gray-500 hover:text-red-400 transition-colors p-2 rounded-lg hover:bg-red-500/10"
                aria-label="Delete task"
              >
                <Trash2 className="h-5 w-5" />
              </motion.button>
            ) : (
              <motion.div
                key="confirm-btns"
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0 }}
                className="flex space-x-2"
              >
                <motion.button
                  whileHover={{ scale: 1.15 }}
                  whileTap={{ scale: 0.85 }}
                  onClick={handleDelete}
                  disabled={isDeleting}
                  className="text-white bg-red-500 hover:bg-red-600 transition-colors p-2 rounded-lg shadow-lg"
                  aria-label="Confirm delete"
                >
                  {isDeleting ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      <Trash2 className="h-4 w-4" />
                    </motion.div>
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.15 }}
                  whileTap={{ scale: 0.85 }}
                  onClick={() => setShowDeleteConfirm(false)}
                  className="text-white bg-gray-600 hover:bg-gray-700 transition-colors p-2 rounded-lg shadow-lg"
                  aria-label="Cancel delete"
                >
                  <span className="text-sm font-bold">✕</span>
                </motion.button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
};

export default TaskItem;