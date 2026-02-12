---
name: auth-skill
description: Implement secure authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Auth Skill – Secure Authentication Handling

## Instructions

1. **User Signup**
   - Validate user input (email, password, username)
   - Hash passwords using bcrypt or argon2
   - Prevent duplicate accounts
   - Store only hashed credentials

2. **User Signin**
   - Verify credentials securely
   - Compare hashed passwords
   - Handle invalid login attempts safely
   - Return minimal, non-sensitive error messages

3. **Password Security**
   - Never store plain-text passwords
   - Use strong hashing algorithms (bcrypt / argon2)
   - Apply proper salt rounds
   - Support password reset flows securely

4. **JWT Tokens**
   - Generate signed JWT access tokens
   - Set appropriate expiration times
   - Verify tokens on protected routes
   - Avoid storing sensitive data inside tokens

5. **Better Auth Integration**
   - Configure Better Auth providers correctly
   - Handle session management securely
   - Protect API routes and pages
   - Follow Better Auth best practices

6. **Validation**
   - Use schema validation (Zod / Yup / Pydantic)
   - Enforce strong password rules
   - Sanitize all inputs
   - Validate request bodies and headers

## Best Practices
- Always hash passwords before storage
- Use HTTPS-only secure cookies for auth tokens
- Never expose internal auth errors
- Rotate JWT secrets periodically
- Keep auth logic centralized
- Follow OWASP authentication guidelines
- Fail securely and log safely

## Example Structure
```ts
// Signup example
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

const hashedPassword = await bcrypt.hash(password, 12);

const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET!,
  { expiresIn: "1h" }
);
