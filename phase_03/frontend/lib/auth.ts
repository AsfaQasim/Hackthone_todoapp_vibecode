import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  // Use a simple configuration that doesn't require database initialization
  // This will use JWT-based auth without database persistence
  database: {
    provider: "sqlite",
    url: "file:./dev.db", // Use local file for dev instead of memory
  },
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: "http://localhost:3000",
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt()
  ],
});
