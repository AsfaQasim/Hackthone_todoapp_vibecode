# Database Setup for Neon PostgreSQL

## Environment Variables

To connect to your Neon PostgreSQL database, update your `.env.local` file with the correct connection string:

```env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
```

## Setting up the Database

1. Create a project in [Neon Console](https://console.neon.tech/)
2. Copy the connection string from your Neon dashboard
3. Update the `DATABASE_URL` in your `.env.local` file
4. The database tables will be created automatically when you first run the application

## Required Tables

The application expects a `users` table with the following schema:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

This table will be created automatically when the application starts if it doesn't exist.

## Testing the Connection

To test if your database connection is working properly, you can run the application and try signing up a new user. If successful, the user will be stored in your Neon database.