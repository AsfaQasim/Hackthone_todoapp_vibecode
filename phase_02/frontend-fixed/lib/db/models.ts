import pool from './client';
import bcrypt from 'bcrypt';

// Define the User interface
export interface User {
  id: number;
  email: string;
  password: string;
  created_at: Date;
}

// Create the users table if it doesn't exist
export async function initializeUsersTable() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('Users table initialized successfully');
  } catch (error) {
    console.error('Error initializing users table:', error);
    throw error;
  }
}

// Create a new user
export async function createUser(email: string, password: string): Promise<User> {
  try {
    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10);
    
    const result = await pool.query(
      'INSERT INTO users (email, password) VALUES ($1, $2) RETURNING *',
      [email.toLowerCase(), hashedPassword]
    );
    
    return result.rows[0];
  } catch (error: any) {
    if (error.code === '23505') { // Unique violation error code
      throw new Error('User with this email already exists');
    }
    throw error;
  }
}

// Find a user by email
export async function findUserByEmail(email: string): Promise<User | null> {
    try {
    const result = await pool.query(
      'SELECT * FROM users WHERE email = $1',
      [email.toLowerCase()]
    );
    
    return result.rows.length > 0 ? result.rows[0] : null;
  } catch (error) {
    console.error('Error finding user by email:', error);
    throw error;
  }
}

// Find a user by ID
export async function findUserById(id: number): Promise<User | null> {
  try {
    const result = await pool.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    
    return result.rows.length > 0 ? result.rows[0] : null;
  } catch (error) {
    console.error('Error finding user by ID:', error);
    throw error;
  }
}