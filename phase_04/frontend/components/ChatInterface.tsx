'use client';

import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Bot, User } from 'lucide-react';
import Button from './ui/Button';
import Textarea from './Textarea';
import { useAuth } from '../contexts/AuthContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolCalls?: any[];
}

interface ChatInterfaceProps {
  userId: string;
  onTaskAdded?: () => void;  // Callback to notify parent when a task is added
}

export default function ChatInterface({ userId, onTaskAdded }: ChatInterfaceProps) {
  const { user, loading: authLoading } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome-message',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant. You can ask me to help you manage your tasks.',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check connection to backend and scroll to bottom of messages
  useEffect(() => {
    // Check if backend is accessible via Next.js API proxy
    const checkConnection = async () => {
      try {
        // Use Next.js API route proxy instead of direct backend call
        const response = await fetch('/api/health');
        if (response.ok) {
          setConnectionStatus('connected');
        } else {
          setConnectionStatus('disconnected');
        }
      } catch (error) {
        console.error('Backend connection failed:', error);
        setConnectionStatus('disconnected');
      }
    };

    checkConnection();
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || authLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Wait for auth to finish loading, then check if user is authenticated
      if (authLoading) {
        // Wait a bit for auth to load if still loading
        await new Promise(resolve => setTimeout(resolve, 100));
      }

      if (!user) {
        throw new Error('User not authenticated');
      }

      // Call the frontend proxy API which forwards to the backend
      // The auth cookie will be included automatically with credentials: 'include'
      const response = await fetch(`/api/chat/${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // The API route will extract the token from cookies and forward it to the backend
        },
        credentials: 'include', // Include cookies in the request
        body: JSON.stringify({
          message: inputValue,
          conversation_id: localStorage.getItem('conversation_id') || null,
        }),
      });

      if (response.status === 401) {
        // Token expired or invalid, show error message instead of redirecting
        const errorMessage: Message = {
          id: `error-${Date.now()}`,
          role: 'assistant',
          content: 'Your session has expired. Please refresh the page or log in again.',
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, errorMessage]);
        setIsLoading(false);
        return;
      }

      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch (parseError) {
          // If response is not JSON, create a generic error
          errorData = {
            error: `HTTP ${response.status} - ${response.statusText}`,
            details: 'Response was not in JSON format'
          };
        }

        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      let data;
      try {
        data = await response.json();
      } catch (parseError) {
        // Handle case where response is not JSON even though status was OK
        throw new Error('Response was not in JSON format');
      }

      // Save conversation ID to localStorage
      localStorage.setItem('conversation_id', data.conversation_id);

      // Add assistant message
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        toolCalls: data.tool_calls || [],
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check if any tool calls were made that affect the task list
      if (data.tool_calls && Array.isArray(data.tool_calls)) {
        const hasTaskRelatedCall = data.tool_calls.some((call: any) =>
          call.tool_name === 'add_task' ||
          call.tool_name === 'create_task' ||
          call.tool_name === 'createTask' ||
          call.tool_name === 'update_task' ||
          call.tool_name === 'delete_task'
        );

        if (hasTaskRelatedCall && onTaskAdded) {
          // Call the callback to notify parent component that tasks may have changed
          onTaskAdded();
        }
      }
    } catch (error: any) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}. Please try again.`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-900/50 backdrop-blur-lg border border-gray-800 rounded-xl p-4">
      {/* Connection Status Indicator */}
      <div className="mb-3 flex items-center justify-between">
        <div className="flex items-center">
          <div className={`w-2 h-2 rounded-full mr-2 ${
            connectionStatus === 'connected' ? 'bg-green-500' :
            connectionStatus === 'checking' ? 'bg-yellow-500 animate-pulse' : 'bg-red-500'
          }`}></div>
          <span className="text-xs text-gray-400">
            {connectionStatus === 'connected' ? 'Connected to AI Assistant' :
             connectionStatus === 'checking' ? 'Connecting...' : 'Connection issue'}
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto max-h-[500px] mb-4 pr-2 custom-scrollbar">
        <div className="space-y-4">
          {messages.map((message) => (
            // Skip the welcome message if connection is not established
            message.id !== 'welcome-message' || connectionStatus !== 'disconnected' ? (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl p-4 ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-br-none'
                      : 'bg-gray-800 text-gray-100 rounded-bl-none'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    {message.role === 'assistant' && (
                      <div className="mt-0.5 flex-shrink-0">
                        <Bot className="h-5 w-5 text-cyan-400" />
                      </div>
                    )}
                    <div className="flex-1">
                      <p className="whitespace-pre-wrap">{message.content}</p>

                      {message.toolCalls && message.toolCalls.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-gray-700">
                          <p className="text-xs text-gray-400 mb-1">Actions taken:</p>
                          <div className="text-xs bg-gray-900 p-2 rounded">
                            {message.toolCalls.map((call, idx) => (
                              <div key={idx} className="mb-1 last:mb-0">
                                <span className="font-mono text-cyan-400">{call.tool_name}</span>
                                <span className="text-gray-500 ml-2">
                                  {JSON.stringify(call.arguments)}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                    {message.role === 'user' && (
                      <div className="mt-0.5 flex-shrink-0">
                        <User className="h-5 w-5 text-white/80" />
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            ) : null
          ))}
          {connectionStatus === 'disconnected' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="max-w-[80%] rounded-2xl bg-gray-800 text-gray-100 rounded-bl-none p-4">
                <div className="flex items-center gap-3">
                  <Bot className="h-5 w-5 text-cyan-400" />
                  <p className="text-sm text-gray-300">
                    Unable to connect to the AI Assistant. Please make sure the backend server is running.
                  </p>
                </div>
              </div>
            </motion.div>
          )}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="max-w-[80%] rounded-2xl bg-gray-800 text-gray-100 rounded-bl-none p-4">
                <div className="flex items-center gap-3">
                  <Bot className="h-5 w-5 text-cyan-400" />
                  <div className="flex space-x-2">
                    <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce delay-75"></div>
                    <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce delay-150"></div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mt-auto">
        <div className="flex gap-2">
          <Textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={
              connectionStatus === 'connected'
                ? "Ask me to manage your tasks..."
                : "Backend unavailable - check if server is running"
            }
            className={`flex-1 resize-none min-h-[60px] max-h-32 py-3 px-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent ${
              connectionStatus === 'connected'
                ? 'bg-gray-800 border border-gray-700 text-white placeholder-gray-500'
                : 'bg-gray-900 border border-red-900 text-gray-400 placeholder-red-800'
            }`}
            disabled={isLoading || connectionStatus !== 'connected'}
          />
          <Button
            type="submit"
            disabled={!inputValue.trim() || isLoading || connectionStatus !== 'connected'}
            className={`self-end px-4 py-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed ${
              connectionStatus === 'connected'
                ? 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            }`}
          >
            <Send className="h-5 w-5" />
          </Button>
        </div>
        <p className="text-xs text-gray-500 mt-2 text-center">
          {connectionStatus === 'connected'
            ? "VibeCode AI Assistant can help you manage tasks with natural language"
            : "Please start the backend server (port 8000) to enable AI features"}
        </p>
      </form>
    </div>
  );
}