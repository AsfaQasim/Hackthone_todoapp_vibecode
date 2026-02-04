import { betterAuth } from "better-auth";

// Minimal Better Auth configuration to avoid database issues
// We're primarily using our custom auth system, so Better Auth is just for compatibility
export const auth = betterAuth({
  // Skip database configuration to avoid initialization errors
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: "http://localhost:3000",
  emailAndPassword: {
    enabled: false, // Disable email/password since we're using custom auth
  },
  // Skip social providers
  socialProviders: {},
});
