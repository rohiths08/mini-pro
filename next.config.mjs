/** @type {import('next').NextConfig} */
const nextConfig = {
  turbopack: {
    resolve: {
      // Mermaid will be handled as external in build process
    },
  },
  webpack: (config) => {
    config.externals = [...(config.externals || []), 'mermaid']
    return config
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
}

export default nextConfig
