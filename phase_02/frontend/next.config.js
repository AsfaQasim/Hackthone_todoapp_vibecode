/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    // Disable Turbopack initially to ensure stable SWC compilation
    turbo: {
      // Temporarily disable Turbopack until SWC issues are resolved
      enabled: false,
    },
  },
  // Configure webpack for better Windows compatibility
  webpack: (config, { isServer }) => {
    // Ensure compatibility with Windows file paths
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false, // Disable fs polyfills on client
      };
    }

    // Handle WASM modules properly
    config.experiments = {
      ...config.experiments,
      asyncWebAssembly: true,
      layers: true,
    };

    return config;
  },
  // Increase the maximum content length to handle large bundles during development
  httpAgentOptions: {
    maxSockets: 50,
  },
};

module.exports = nextConfig;