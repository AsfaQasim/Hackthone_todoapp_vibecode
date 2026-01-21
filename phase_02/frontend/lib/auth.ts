import { betterAuth } from "better-auth";

export const auth = betterAuth({
    // Using in-memory database for development
    // In production, you should use a proper database adapter
    database: {
        type: "memory",
    },
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false, // Disable email verification for faster signup
        // Reduce password complexity for development (strengthen in production)
        passwordValidation: {
            // Minimal password requirements for faster processing
            minLength: 6,
            requireSpecialChar: false,
            requireNumbers: false,
            requireUppercase: false,
        },
    },
    account: {
        accountLockout: {
            maxAttempts: 10, // Higher attempts to reduce lockout processing
            duration: 60 * 1000, // 1 minute lockout
        },
    },
    session: {
        expiresIn: 7 * 24 * 60 * 60 * 1000, // 7 days
        updateAge: 24 * 60 * 60 * 1000, // Update once per day
    },
    socialProviders: {}, // Disable social providers if not needed
    // Reduce security measures for development (increase in production)
    rateLimiter: {
        windowMs: 10 * 60 * 1000, // 10 minutes
        max: 100, // Allow more requests in dev
    },
    // CORS/Trusted Origin settings for Next.js 16
    trustedOrigins: ["http://localhost:3000"],
});
