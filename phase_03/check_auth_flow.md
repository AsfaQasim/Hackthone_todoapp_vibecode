# Check Authentication Flow

## Step 1: Check if Token Exists

Open browser console (F12) and run:

```javascript
// Check cookies
console.log('All cookies:', document.cookie);

// Check specifically for auth_token
const authToken = document.cookie.split('; ').find(row => row.startsWith('auth_token='));
console.log('Auth token:', authToken);

// If token exists, decode it
if (authToken) {
    const token = authToken.split('=')[1];
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        console.log('Token payload:', payload);
        console.log('User ID:', payload.sub || payload.userId);
        console.log('Email:', payload.email);
        console.log('Expires:', new Date(payload.exp * 1000));
    } catch (e) {
        console.error('Failed to decode token:', e);
    }
} else {
    console.error('❌ NO AUTH TOKEN FOUND!');
    console.log('You need to login again');
}
```

## Step 2: Check Auth Context

```javascript
// Check if user is logged in according to React context
// This will be visible in React DevTools
```

## Step 3: Manual Test

If no token found, you need to:
1. Logout completely
2. Clear all cookies
3. Login again
4. Token should be set

## Step 4: Check Frontend API Route

The 401 is coming from `frontend/app/api/chat/[userId]/route.ts`

It checks:
1. Does auth_token cookie exist? ❌ If no → 401
2. Can token be decoded? ❌ If no → 401
3. Does token have user ID? ❌ If no → 401

Run the JavaScript above to see which check is failing.
