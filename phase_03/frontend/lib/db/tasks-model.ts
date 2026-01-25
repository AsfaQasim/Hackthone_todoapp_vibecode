import pool from './client';

// Initialize the tasks table if it doesn't exist
export async function initializeTasksTable() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('Tasks table initialized successfully');
  } catch (error) {
    console.error('Error initializing tasks table:', error);
    throw error;
  }
}

// Create a new task
export async function createTask(userId: number, title: string, description?: string): Promise<any> {
  try {
    const result = await pool.query(
      'INSERT INTO tasks (user_id, title, description, completed) VALUES ($1, $2, $3, $4) RETURNING *',
      [userId, title, description || null, false]
    );

    return result.rows[0];
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
}

// Get tasks for a user
export async function getTasksByUserId(userId: number): Promise<any[]> {
  try {
    const result = await pool.query(
      'SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC',
      [userId]
    );

    return result.rows;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
}

// Get a specific task by ID for a specific user
export async function getTaskById(taskId: number, userId: number) {
  try {
    const result = await pool.query(
      'SELECT * FROM tasks WHERE id = $1 AND user_id = $2',
      [taskId, userId]
    );

    return result.rows[0] || null;
  } catch (error) {
    console.error('Error fetching task by ID:', error);
    throw error;
  }
}

// Update a task for a specific user
export async function updateTask(taskId: number, userId: number, updates: { title?: string; description?: string; completed?: boolean }) {
  try {
    const { title, description, completed } = updates;
    const result = await pool.query(
      'UPDATE tasks SET title = COALESCE($1, title), description = COALESCE($2, description), completed = COALESCE($3, completed) WHERE id = $4 AND user_id = $5 RETURNING *',
      [title, description, completed, taskId, userId]
    );

    return result.rows[0];
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
}

// Delete a task for a specific user
export async function deleteTask(taskId: number, userId: number) {
  try {
    const result = await pool.query(
      'DELETE FROM tasks WHERE id = $1 AND user_id = $2',
      [taskId, userId]
    );

    // Return the number of affected rows to confirm deletion
    return result.rowCount;
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
}