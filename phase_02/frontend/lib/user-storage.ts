// This file is deprecated. Use lib/db/models.ts instead for user operations.
// Keeping this file temporarily to avoid breaking existing imports during migration.
// Will be removed after all references are updated.

export function getUsers(): Record<string, { password: string; email: string }> {
  console.warn('getUsers is deprecated. Use database models instead.');
  return {};
}

export function addUser(email: string, password: string): void {
  console.warn('addUser is deprecated. Use database models instead.');
}

export function getUser(email: string) {
  console.warn('getUser is deprecated. Use database models instead.');
  return null;
}