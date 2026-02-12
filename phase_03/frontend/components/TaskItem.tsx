'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trash2, CheckCircle, Circle } from 'lucide-react';
import Button from './ui/Button';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
}

interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: number) => void;
  onDelete: (id: number) => void;
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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleDelete = () => {
    // Ensure the task.id is a valid number before calling delete
    if (task.id && typeof task.id === 'number' && !isNaN(task.id)) {
      onDelete(task.id);
      setShowDeleteConfirm(false);
    } else {
      console.error('Invalid task ID:', task.id);
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: 0.3 }}
      className={`p-5 rounded-xl border backdrop-blur-lg transition-all duration-300 ${
        task.completed
          ? 'bg-green-900/10 border-green-800/30'
          : 'bg-white/10 border-white/20 hover:border-cyan-500/30'
      }`}
    >
      <div className="flex justify-between items-start">
        <div className="flex items-start space-x-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => !isUpdating && onToggleComplete(task.id)}
            disabled={isUpdating}
            className="mt-1 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-full"
            aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          >
            {task.completed ? (
              <CheckCircle className="h-6 w-6 text-green-500" />
            ) : (
              <Circle className="h-6 w-6 text-gray-400" />
            )}
          </motion.button>

          <div className="flex-1 min-w-0">
            <motion.h3
              className={`font-medium text-lg truncate ${
                task.completed
                  ? 'text-gray-500 line-through'
                  : 'text-white'
              }`}
              animate={{
                color: task.completed ? '#9CA3AF' : '#FFFFFF'
              }}
              transition={{ duration: 0.2 }}
            >
              {task.title}
            </motion.h3>

            {task.description && (
              <p className="text-gray-300 mt-2 break-words">{task.description}</p>
            )}

            <p className="text-xs text-gray-500 mt-3">
              Created: {formatDate(task.created_at)}
            </p>
          </div>
        </div>

        <div className="flex space-x-2">
          {!showDeleteConfirm ? (
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => setShowDeleteConfirm(true)}
              className="text-gray-500 hover:text-red-400 transition-colors p-1"
              aria-label="Delete task"
            >
              <Trash2 className="h-5 w-5" />
            </motion.button>
          ) : (
            <div className="flex space-x-2">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleDelete}
                className="text-red-500 hover:text-red-400 transition-colors p-1"
                aria-label="Confirm delete"
              >
                {isDeleting ? (
                  <motion.span
                    animate={{ rotate: 360 }}
                    transition={{ duration: 0.5, repeat: Infinity, ease: "linear" }}
                  >
                    <Trash2 className="h-5 w-5" />
                  </motion.span>
                ) : (
                  <Trash2 className="h-5 w-5" />
                )}
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setShowDeleteConfirm(false)}
                className="text-gray-500 hover:text-gray-300 transition-colors p-1"
                aria-label="Cancel delete"
              >
                <span className="h-5 w-5">✕</span>
              </motion.button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default TaskItem;