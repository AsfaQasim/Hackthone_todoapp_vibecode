/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configure Turbopack for Next.js 16
  // Since webpack config is not compatible with Turbopack, we'll use Turbopack defaults
  turbopack: {},
  // Handle dynamic routes properly
  experimental: {
    // Ensure proper handling of catch-all routes
    serverComponentsExternalPackages: [],
  },
};

module.exports = nextConfig;