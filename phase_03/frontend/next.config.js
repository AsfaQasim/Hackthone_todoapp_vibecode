/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: false,

  // Simplified webpack configuration to address ChunkLoadError
  webpack: (config, { dev, isServer }) => {
    if (dev) {
      // Disable webpack cache in development to prevent cache corruption
      config.cache = false;

      // Use a more reliable devtool setting
      config.devtool = 'eval-source-map';
    }

    // Ensure consistent chunk naming to prevent loading issues
    if (!isServer) {
      config.output.chunkFilename = 'static/chunks/[name].[contenthash:8].js';
    }

    return config;
  },
};

module.exports = nextConfig;