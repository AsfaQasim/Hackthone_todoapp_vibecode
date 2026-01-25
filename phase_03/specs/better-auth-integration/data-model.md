# Data Model: Better Auth Integration

## User Entity
- **id**: string (unique identifier from Better Auth)
- **email**: string (user's email address, unique)
- **name**: string (optional user display name)
- **created_at**: datetime (account creation timestamp)
- **updated_at**: datetime (last update timestamp)
- **email_verified**: boolean (whether email has been verified)

## Session Entity
- **id**: string (session identifier from Better Auth)
- **user_id**: string (foreign key to User)
- **expires_at**: datetime (session expiration time)
- **created_at**: datetime (session creation time)
- **updated_at**: datetime (last activity time)
- **device_info**: string (information about the device used)

## Token Entity
- **id**: string (token identifier)
- **session_id**: string (foreign key to Session)
- **token_type**: enum ('access', 'refresh') (type of token)
- **token_value**: string (hashed token value)
- **expires_at**: datetime (token expiration time)
- **created_at**: datetime (token creation time)

## Validation Rules
- User email must be unique and valid email format
- Session must be linked to an existing user
- Session expiration must be in the future
- Token expiration must be in the future
- User must verify email before full account activation

## Relationships
- User (1) → (Many) Session (one-to-many)
- Session (1) → (Many) Token (one-to-many)

## State Transitions
- User Registration → Email Verification Required → Active Account
- Session Creation → Active → Expired/Inactive
- Token Generation → Active → Expired/Revoked

## Indexes
- User.email (unique index for fast lookup)
- Session.expires_at (index for cleanup jobs)
- Token.expires_at (index for cleanup jobs)