---
name: database-skill
description: Design and manage database schemas, tables, and migrations. Use for structured and reliable data storage.
---

# Database Skill – Schema & Migration Management

## Instructions

1. **Schema Design**
   - Design normalized and scalable schemas
   - Define clear relationships (one-to-one, one-to-many, many-to-many)
   - Choose appropriate data types and constraints

2. **Table Creation**
   - Create tables with primary keys and foreign keys
   - Add indexes for frequently queried fields
   - Enforce uniqueness and not-null constraints

3. **Migrations**
   - Write safe, versioned database migrations
   - Support up and down migrations
   - Avoid destructive changes in production
   - Ensure backward compatibility when possible

4. **Data Integrity**
   - Use constraints to enforce data correctness
   - Maintain referential integrity
   - Handle cascading updates and deletes carefully

## Best Practices
- Keep schemas simple and well-documented
- Use migrations for all schema changes
- Never modify production tables directly
- Add indexes only when needed
- Test migrations in staging before production
- Follow PostgreSQL best practices

## Example Structure
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
