import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const auth = betterAuth({
    database: prismaAdapter(prisma, {
        provider: "postgresql", // Explicitly set for Neon
    }),
    emailAndPassword: {
        enabled: true,
    },
    // CORS/Trusted Origin settings for Next.js 16
    trustedOrigins: ["http://localhost:3000"],
});
