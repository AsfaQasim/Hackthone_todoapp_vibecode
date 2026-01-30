/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable any features that might rely on platform-specific binaries
  trailingSlash: false,

  // Disable filesystem cache to prevent cache corruption issues
  webpack: (config, { dev, isServer }) => {
    if (dev) {
      config.devtool = 'cheap-module-source-map'; // Less intensive source maps in development
    }

    // Disable webpack cache in development to prevent cache corruption
    if (dev) {
      config.cache = false;
    }

    return config;
  },

  // Experimental settings to improve stability
  experimental: {
    // Disable webpack cache in development
    // turbo: false,  // Commenting out as it expects an object, not boolean
  },

  // Disable Next.js cache in development
  // cacheLife: process.env.NODE_ENV === 'development' ? 0 : undefined,  // Removing as it's not a valid option
};

module.exports = nextConfig;