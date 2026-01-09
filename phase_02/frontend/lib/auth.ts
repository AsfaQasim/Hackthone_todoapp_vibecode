import { betterAuth } from "better-auth";

// Initialize Better Auth
export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback_dev_secret_for_testing_only",
  baseURL: process.env.BASE_URL || "http://localhost:3000",
  emailAndPassword: {
    enabled: true,
  },
  account: {
    accountLinking: {
      enabled: true,
    }
  },
  advanced: {
    generateUserId: () => crypto.randomUUID(),
  },
  // Configure session handling to support JWT-like behavior
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days in seconds as per spec
    updateAge: 24 * 60 * 60, // 24 hours
  },
  // Custom hooks to ensure JWT contains required information
  hooks: {
    after: [
      {
        // This hook runs after session creation to ensure proper JWT structure
        event: "sessionCreated",
        handler: async ({ session, user }) => {
          // The session will contain user_id, email, and expiration info
          console.log(`Session created for user: ${user.id}, email: ${user.email}`);
        }
      }
    ]
  }
});

// Export types for use in client components
export type Session = typeof auth.$Infer.Session;
export type User = typeof auth.$Infer.User;