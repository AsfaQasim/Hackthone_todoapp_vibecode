import { betterAuth } from 'better-auth';
import { bearer } from 'better-auth/plugins';

export const auth = betterAuth({
  database: {
    provider: 'sqlite',
    url: process.env.DATABASE_URL || './db.sqlite',
  },
  secret: process.env.BETTER_AUTH_SECRET,
  plugins: [
    bearer({
      enabled: true,
    })
  ],
  // Add email/password authentication
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
});

export default auth;