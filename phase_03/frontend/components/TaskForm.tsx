'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Sparkles } from 'lucide-react';
import { Card, CardContent } from './ui/Card';
import Input from './ui/Input';
import Textarea from './ui/Textarea';
import Button from './ui/Button';

interface TaskFormProps {
  onAddTask: (title: string, description: string) => void;
  isLoading?: boolean;
}

const TaskForm = ({ onAddTask, isLoading = false }: TaskFormProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [isExpanded, setIsExpanded] = useState(false);

  const validate = () => {
    const newErrors: { title?: string; description?: string } = {};
    
    if (!title.trim()) {
      newErrors.title = 'Task title is required';
    } else if (title.length > 100) {
      newErrors.title = 'Task title is too long (max 100 characters)';
    }
    
    if (description.length > 500) {
      newErrors.description = 'Description is too long (max 500 characters)';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validate()) {
      onAddTask(title, description);
      setTitle('');
      setDescription('');
      setErrors({});
      setIsExpanded(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ 
        type: "spring",
        stiffness: 300,
        damping: 25
      }}
    >
      <Card className="overflow-hidden border-2 border-cyan-500/30 hover:border-cyan-400/50 transition-all duration-300 shadow-xl shadow-cyan-500/10">
        <CardContent className="p-0">
          <motion.form 
            onSubmit={handleSubmit} 
            className="space-y-4 p-4 sm:p-6"
            layout
          >
            <motion.div 
              className="flex items-center justify-between mb-4"
              layout
            >
              <div className="flex items-center gap-3">
                <motion.div
                  animate={{ 
                    rotate: [0, 10, -10, 0],
                    scale: [1, 1.1, 1.1, 1]
                  }}
                  transition={{ 
                    duration: 2,
                    repeat: Infinity,
                    repeatDelay: 3
                  }}
                >
                  <Sparkles className="h-6 w-6 text-cyan-400" />
                </motion.div>
                <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                  Create New Task
                </h2>
              </div>
              
              <motion.button
                type="button"
                onClick={() => setIsExpanded(!isExpanded)}
                whileHover={{ scale: 1.1, rotate: 90 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-full bg-cyan-500/20 hover:bg-cyan-500/30 transition-colors"
              >
                <Plus className={`h-5 w-5 text-cyan-400 transition-transform duration-300 ${isExpanded ? 'rotate-45' : ''}`} />
              </motion.button>
            </motion.div>
            
            <motion.div layout>
              <Input
                label="Task Title *"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="What needs to be done?"
                error={errors.title}
                required
                className="transition-all duration-300"
              />
            </motion.div>
            
            <AnimatePresence>
              {isExpanded && (
                <motion.div
                  initial={{ opacity: 0, height: 0, y: -20 }}
                  animate={{ opacity: 1, height: 'auto', y: 0 }}
                  exit={{ opacity: 0, height: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  <Textarea
                    label="Description (Optional)"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Add more details about your task..."
                    error={errors.description}
                    rows={3}
                  />
                </motion.div>
              )}
            </AnimatePresence>
            
            <motion.div 
              className="pt-2"
              layout
            >
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={isLoading}
                  className="w-full py-3 sm:py-4 text-base sm:text-lg font-semibold bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50 transition-all duration-300"
                >
                  {isLoading ? (
                    <motion.span
                      animate={{ opacity: [1, 0.5, 1] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                    >
                      Adding task...
                    </motion.span>
                  ) : (
                    <span className="flex items-center justify-center gap-2">
                      <Plus className="h-5 w-5" />
                      Add Task
                    </span>
                  )}
                </Button>
              </motion.div>
            </motion.div>
          </motion.form>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default TaskForm;