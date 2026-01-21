import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  // Configure Turbopack for Next.js 16
  // Since webpack config is not compatible with Turbopack, we'll use Turbopack defaults
  // and remove the webpack-specific configuration
  turbopack: {},
  // Handle dynamic routes properly
  experimental: {
    // Ensure proper handling of catch-all routes
    serverComponentsExternalPackages: ["better-auth"],
  },
};

export default nextConfig;
