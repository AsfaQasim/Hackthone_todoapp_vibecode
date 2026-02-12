import { initializeDatabase } from './lib/db';
import { createUser, findUserByEmail } from './lib/db/models';
import bcrypt from 'bcrypt';

async function testConnection() {
  try {
    console.log('Initializing database connection...');
    await initializeDatabase();
    
    console.log('Database connected successfully!');
    
    // Test creating a user
    console.log('Testing user creation...');
    const testUser = await createUser('test@example.com', 'password123');
    console.log('Test user created:', testUser);
    
    // Test finding the user
    console.log('Testing user lookup...');
    const foundUser = await findUserByEmail('test@example.com');
    console.log('Found user:', foundUser);
    
    // Test password comparison
    if (foundUser) {
      const isValid = await bcrypt.compare('password123', foundUser.password);
      console.log('Password comparison result:', isValid);
    }
    
    console.log('Database test completed successfully!');
  } catch (error) {
    console.error('Database test failed:', error);
  }
}

testConnection();