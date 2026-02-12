import { initializeTasksTable } from './tasks-model';

// Initialize the database tables
export async function initializeDatabase() {
  try {
    await initializeTasksTable();
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
    throw error;
  }
}

// Export the pool for direct queries if needed
export { default as pool } from './client';