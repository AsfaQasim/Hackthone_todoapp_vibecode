# Frontend UI & Integration

This is the frontend implementation for the Todo application, built with Next.js 16+ using the App Router. It provides a responsive, authentication-aware interface that integrates securely with the Task Management API.

## Features

- **Authentication**: Secure signup and signin flows using Better Auth
- **Task Management**: Full CRUD operations for tasks with real-time updates
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop devices
- **User Isolation**: Each user can only access their own tasks
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading States**: Proper loading indicators during API operations

## Architecture

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with SessionProvider
│   ├── page.tsx            # Home page
│   ├── signup/page.tsx     # Signup page
│   ├── signin/page.tsx     # Signin page
│   ├── dashboard/page.tsx  # Dashboard page
│   ├── tasks/page.tsx      # Task management page
│   └── todos/page.tsx      # Alternative task page
├── components/
│   ├── Header.tsx          # Navigation header with auth state
│   ├── AuthComponent.tsx   # Login/signup form
│   ├── LogoutButton.tsx    # Logout functionality
│   └── task/
│       ├── TaskItem.tsx    # Individual task component
│       └── CreateTaskForm.tsx # Task creation form
├── lib/
│   ├── auth.ts             # Better Auth client configuration
│   └── api.ts              # API utility functions
├── types/
│   └── task.ts             # Task type definitions
├── middleware.ts           # Route protection middleware
├── pages/
│   └── api/
│       └── auth/
│           └── [...betterauth].ts  # Better Auth API routes
├── .env.local              # Environment variables
├── package.json            # Dependencies
└── README.md               # This file
```

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8080
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## API Integration

The frontend communicates with the backend API using the centralized API client in `lib/api.ts`. All requests include the JWT token from Better Auth in the Authorization header.

## Authentication Flow

1. Users sign up or sign in using the forms
2. Better Auth manages the session and JWT tokens
3. Middleware protects routes that require authentication
4. All API requests include the JWT token automatically

## Task Management Flow

1. Users can create new tasks using the form on the tasks page
2. Tasks are displayed in a list with options to edit, delete, or toggle completion
3. All operations are performed through the API with proper authentication
4. The UI updates in real-time after each operation

## Security Features

- JWT tokens are handled securely by Better Auth
- All API requests require authentication
- Users can only access their own tasks
- Protected routes redirect unauthenticated users to the signin page
- Proper error handling prevents information leakage

## Responsive Design

The UI is built with mobile-first principles using Tailwind CSS. It adapts to different screen sizes with appropriate layouts and touch targets.

## Error Handling

Comprehensive error handling is implemented at multiple levels:
- Form validation with user-friendly messages
- API error responses with appropriate feedback
- Loading states during operations
- Network error handling