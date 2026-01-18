import { auth } from '../../../../lib/auth';

// The handler is a function that handles both GET and POST requests
export const GET = auth.handler;
export const POST = auth.handler;