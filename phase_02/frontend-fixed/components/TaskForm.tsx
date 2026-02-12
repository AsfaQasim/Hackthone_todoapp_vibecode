'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
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
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
    >
      <Card>
        <CardContent className="p-0">
          <form onSubmit={handleSubmit} className="space-y-4 p-4 sm:p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Add New Task</h2>
            
            <Input
              label="Task Title *"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              error={errors.title}
              required
            />
            
            <Textarea
              label="Description (Optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add details..."
              error={errors.description}
              rows={3}
            />
            
            <div className="pt-2">
              <Button
                type="submit"
                variant="primary"
                isLoading={isLoading}
                className="w-full py-3 sm:py-4 text-base sm:text-lg"
              >
                {isLoading ? 'Adding task...' : 'Add Task'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default TaskForm;