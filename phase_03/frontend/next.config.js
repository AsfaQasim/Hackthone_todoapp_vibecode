/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: false,

  // Configure external packages for server components
  experimental: {
    serverComponentsExternalPackages: ["better-sqlite3", "pg", "bcrypt"],
  },

  // Ensure webpack uses the correct resolution
  webpack: (config, { isServer }) => {
    if (!isServer) {
      // Client-side specific config
    }
    return config;
  },
};

module.exports = nextConfig;