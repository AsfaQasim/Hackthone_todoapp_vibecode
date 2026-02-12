

# MASTER INSTRUCTION: Fix Better Auth, Neon DB, and Next.js 16 Implementation

You are an expert Senior Full Stack Engineer. We are fixing a broken authentication implementation in a project using **Next.js 16 (Stable App Router)**, **Better Auth**, **FastAPI**, and **Neon DB (PostgreSQL)**.

The current project state has critical configuration errors (nested folders, connection refusals, and database adapter failures). You must execute the following plan strictly.

### 1. 🧹 PROJECT HYGIENE (CRITICAL)
**Goal:** Eliminate version conflicts and structure issues.
- **Flatten the Structure:** I currently have a `frontend` folder AND a nested `frontend/my-app` folder. This is wrong. Move all source code from `frontend/my-app` to `frontend/` and **delete** the `my-app` folder entirely.
- **Clean Configuration:** Delete any `next.config.js` or `eslint.config.js` if TypeScript versions (`.ts`) exist. Keep only one source of truth.
- **Dependencies:** Ensure `package.json` includes:
  - `"next": "14.2.x"` or `"15.x"` (or "latest stable")
  - `"better-auth": "^1.1.0"`
  - `"@prisma/client": "latest"`
  - `"pg": "latest"` (Required for Neon DB connectivity)

### 2. 🌍 ENVIRONMENT & NEON DB SETUP
**Goal:** Establish a solid connection to Neon DB.
- Create/Update `.env.local` in the `frontend` root with these EXACT keys:
  ```env
  # App URLs
  NEXT_PUBLIC_API_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
  BETTER_AUTH_URL=http://localhost:3000
  
  # Security (Must match Backend)
  BETTER_AUTH_SECRET=your_secure_random_string_here
  
  # Database (Neon DB - Ensure this is the Transaction Mode URL or Session Mode if using Prisma)
  DATABASE_URL="postgres://user:password@ep-host.aws.neon.tech/neondb?sslmode=require"


  3. 🛡️ AUTH CONFIGURATION (Next.js 16 Standard)
Goal: Initialize Better Auth with the Prisma adapter correctly.

Update lib/auth.ts:

Do NOT use edge-specific runtimes unless necessary. Use standard Node.js runtime for the database adapter to avoid "adapter initialization" errors.

import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const auth = betterAuth({
    database: prismaAdapter(prisma, {
        provider: "postgresql", // Explicitly set for Neon
    }),
    emailAndPassword: {
        enabled: true,
    },
    // CORS/Trusted Origin settings for Next.js 16
    trustedOrigins: ["http://localhost:3000"], 
});


🧩 DATABASE SCHEMA (Prisma + Neon)
Goal: Ensure the database has the required Better Auth tables.

Update prisma/schema.prisma:

Code snippet

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Paste the standard Better Auth User, Session, Account, Verification schemas here
// Ensure "User" table includes an "id" field that matches the Backend's expectation (String/UUID)
Action: Run npx prisma generate and npx prisma db push immediately after updating this file.

5. 📡 API CLIENT FIX (The ECONNREFUSED Fix)
Goal: Stop the frontend from crashing when the backend is offline or unreachable.

Update lib/api.ts:

Use authClient.getSession() to get tokens.

Wrap the fetch call in a try/catch block.

If fetch fails (Network Error), return a clean error message to the UI instead of crashing the Next.js server.

TypeScript

// Example safety check
if (!process.env.NEXT_PUBLIC_API_URL) {
    throw new Error("NEXT_PUBLIC_API_URL is not defined");
}
6. 🚀 EXECUTION ORDER
Clean the folder structure.

Install dependencies (npm install pg @prisma/client).

Update .env.local.

Run Prisma Generate.

Start the server (npm run dev) and verify /api/auth/session returns valid JSON (or null) and NOT a 500 error.
