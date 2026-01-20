# Todo App Frontend

This is the frontend for the Todo application using Next.js, Better Auth, and Neon DB.

## Setup Instructions

1. Make sure you have Node.js installed on your system.

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file in the root of the project with the following content:
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
   
   Or directly using:
   ```bash
   npx next dev
   ```

The application will be available at http://localhost:3000 (or another available port if 3000 is in use).

## Project Structure

- `app/` - Contains the Next.js 13+ app router pages
- `components/` - Reusable React components
- `lib/` - Utility functions and authentication setup
- `prisma/` - Database schema and migration files
- `public/` - Static assets

## Key Features

- Authentication using Better Auth
- Database integration with Neon DB (PostgreSQL)
- Prisma ORM for database operations
- Modern Next.js 14+ with App Router