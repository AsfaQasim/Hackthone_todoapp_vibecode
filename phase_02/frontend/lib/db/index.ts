import pool from './client';
import { initializeUsersTable } from './models';

// Initialize the database connection and tables
export async function initializeDatabase() {
  try {
    await initializeUsersTable();
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
    throw error;
  }
}

// Export the pool for direct queries if needed
export { pool };

// Close the pool when the application shuts down
process.on('SIGINT', async () => {
  console.log('Closing database connection...');
  await pool.end();
  process.exit(0);
});