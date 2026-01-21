export const runtime = 'nodejs';
export const dynamic = 'force-dynamic'; // Ensure dynamic rendering for auth routes

import { auth } from '../../../../lib/auth';
import { toNextJsHandler } from 'better-auth/next-js';

// Convert Better Auth handlers to Next.js handlers
const handler = toNextJsHandler(auth);

export { handler as GET, handler as POST };