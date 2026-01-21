import fs from 'fs';
import path from 'path';

const USERS_FILE = path.join(process.cwd(), 'data', 'users.json');

// Ensure data directory exists
const dataDir = path.dirname(USERS_FILE);
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// Initialize users file if it doesn't exist
if (!fs.existsSync(USERS_FILE)) {
  fs.writeFileSync(USERS_FILE, '{}', 'utf8');
}

export function getUsers(): Record<string, { password: string; email: string }> {
  const data = fs.readFileSync(USERS_FILE, 'utf8');
  return JSON.parse(data);
}

export function saveUsers(users: Record<string, { password: string; email: string }>): void {
  fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), 'utf8');
}

export function addUser(email: string, password: string): void {
  const users = getUsers();
  users[email] = { password, email };
  saveUsers(users);
}

export function getUser(email: string) {
  const users = getUsers();
  return users[email];
}