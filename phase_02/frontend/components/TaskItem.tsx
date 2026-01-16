import { useState } from "react";

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskItemProps {
  task: Task;
  onToggleCompletion: (taskId: string, currentCompleted: boolean) => void;
  onEdit: () => void;
  onDelete: (taskId: string) => void;
}

export default function TaskItem({ task, onToggleCompletion, onEdit, onDelete }: TaskItemProps) {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div
      className={`border rounded-xl p-5 transition-all duration-300 ${
        task.completed
          ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200'
          : 'bg-white border-gray-200 hover:border-indigo-300'
      } shadow-sm hover:shadow-md w-full`}
    >
      <div className="flex flex-col gap-4">
        <div className="flex items-start gap-3">
          <button
            onClick={() => onToggleCompletion(task.id, task.completed)}
            className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center mt-1 transition-colors duration-300 ${
              task.completed
                ? 'bg-green-500 border-green-500'
                : 'border-gray-300 hover:border-indigo-400'
            }`}
            aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
          >
            {task.completed && (
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path>
              </svg>
            )}
          </button>

          <div className="flex-1 min-w-0">
            <h3
              className={`text-lg font-medium ${
                task.completed ? 'line-through text-gray-500' : 'text-gray-800'
              } break-words`}
            >
              {task.title}
            </h3>

            {task.description && (
              <p className="mt-2 text-gray-600 break-words">
                {task.description}
              </p>
            )}

            <div className="mt-3 text-sm text-gray-500 flex items-center">
              <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>
                Created: {formatDate(task.created_at)}
                {task.updated_at !== task.created_at && (
                  <>
                    <br />
                    Updated: {formatDate(task.updated_at)}
                  </>
                )}
              </span>
            </div>
          </div>
        </div>

        <div className="flex gap-2 flex-wrap">
          <button
            onClick={onEdit}
            className="px-4 py-2 bg-indigo-50 text-indigo-700 border border-indigo-200 rounded-lg cursor-pointer text-sm whitespace-nowrap hover:bg-indigo-100 transition-colors duration-300 flex items-center"
            aria-label="Edit task"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
            Edit
          </button>

          {!showDeleteConfirm ? (
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="px-4 py-2 bg-red-50 text-red-700 border border-red-200 rounded-lg cursor-pointer text-sm whitespace-nowrap hover:bg-red-100 transition-colors duration-300 flex items-center"
              aria-label="Delete task"
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              Delete
            </button>
          ) : (
            <div className="flex gap-2 flex-wrap">
              <button
                onClick={() => onDelete(task.id)}
                className="px-4 py-2 bg-red-600 text-white border border-red-600 rounded-lg cursor-pointer text-sm whitespace-nowrap hover:bg-red-700 transition-colors duration-300 flex items-center"
              >
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Confirm
              </button>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="px-4 py-2 bg-gray-100 text-gray-700 border border-gray-300 rounded-lg cursor-pointer text-sm whitespace-nowrap hover:bg-gray-200 transition-colors duration-300"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}