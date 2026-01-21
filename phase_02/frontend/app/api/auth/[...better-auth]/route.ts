export const runtime = 'nodejs';

import { auth } from '../../../../lib/auth';
import { toNextJsHandler } from 'better-auth/next-js';

// Convert Better Auth handlers to Next.js handlers
export const { GET, POST } = toNextJsHandler(auth);