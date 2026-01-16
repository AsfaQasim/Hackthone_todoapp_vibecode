import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

// Initialize Better Auth
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "your-secret-key-change-in-production",
  database: {
    provider: "sqlite", // You can change this to postgres, mysql, etc.
    url: process.env.DATABASE_URL || "./db.sqlite",
  },
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    // Add social providers if needed
  },
});

export default auth;