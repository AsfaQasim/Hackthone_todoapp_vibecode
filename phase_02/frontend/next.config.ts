import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  // Disable Turbopack due to stability issues
  experimental: {
    // Ensure proper handling of catch-all routes
    serverComponentsExternalPackages: [],
  },
};

export default nextConfig;
