/** @type {import('next').NextConfig} */
const path = require('path'); // ← ye line missing thi

const nextConfig = {
  turbopack: {
    root: path.resolve(__dirname), // absolute path required
  },
  serverExternalPackages: [], // remove experimental.serverComponentsExternalPackages
}

module.exports = nextConfig;
