# Hackathon Todo Vibecode - Phase 02

This project implements a Todo application with authentication using Next.js, Better Auth, FastAPI, and Neon DB.

## Project Structure

```
phase_02/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend (flattened structure)
│   ├── app/          # App Router pages
│   ├── components/   # React components
│   ├── lib/          # Utilities and auth setup
│   ├── prisma/       # Database schema
│   └── public/       # Static assets
├── .env.local       # Environment variables
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
- ✅ Better Auth integration
- ✅ Neon DB (PostgreSQL) with Prisma ORM
- ✅ Proper error handling for API calls
- ✅ Environment configuration
- ✅ Flattened project structure (no nested folders)

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