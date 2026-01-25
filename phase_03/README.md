# Hackathon Todo Vibecode - Phase 03

This project implements a Todo application with AI chatbot integration using MCP architecture, with authentication using Next.js, Better Auth, FastAPI, and Neon DB.

## Phase 3 Constitution

This project follows the Phase 3 Spec Constitution which mandates:
- Stateless server architecture (no in-memory conversation/task state)
- Database as the only source of truth (Neon PostgreSQL)
- MCP-only task operations (agents use MCP tools, no direct DB access)
- JWT authentication enforcement
- Message persistence for all user/assistant interactions

## Project Structure

```
phase_03/
├── backend/          # FastAPI backend with MCP tools
├── frontend/         # Next.js frontend with AI chat interface
│   ├── app/          # App Router pages
│   ├── components/   # React components
│   ├── lib/          # Utilities and auth setup
│   ├── prisma/       # Database schema
│   └── public/       # Static assets
├── .env.local       # Environment variables
├── .specify/        # SpecKit Plus templates and scripts
│   └── memory/
│       └── constitution.md  # Project constitution
└── README.md
```

## Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with your environment variables:
   ```
   # App URLs
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
   BETTER_AUTH_URL=http://localhost:3000

   # Security (Must match Backend)
   BETTER_AUTH_SECRET=your_secure_random_string_here

   # Database (Neon DB - Ensure this is the Transaction Mode URL or Session Mode if using Prisma)
   DATABASE_URL="postgres://user:password@ep-host.aws.neon.tech/neondb?sslmode=require"
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd ../backend
   ```

2. Set up your Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

## Features

- ✅ Next.js 14+ with App Router
- ✅ Better Auth integration with JWT enforcement
- ✅ Neon DB (PostgreSQL) with Prisma ORM
- ✅ Proper error handling for API calls
- ✅ Environment configuration
- ✅ Flattened project structure (no nested folders)
- ✅ MCP-based AI agent integration
- ✅ Stateless server architecture
- ✅ Message persistence for chat conversations
- ✅ User isolation and ownership enforcement

## Troubleshooting

If you encounter issues with the `next` command not being recognized:
- Use `npx next dev` instead of `npm run dev`
- Make sure you're running the command from the `frontend` directory
- Check that dependencies are properly installed

## Notes

- The frontend structure has been flattened from `frontend/my-app` to `frontend/`
- Better Auth is configured with Prisma adapter for Neon DB
- The project uses Next.js App Router (app directory)
- Environment variables are properly configured for both frontend and backend
- MCP tools are used for all task operations by the AI agent
- Server maintains no conversation state in memory (stateless architecture)
- All messages are persisted to the database for continuity