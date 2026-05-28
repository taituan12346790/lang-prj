import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",   // tối ưu Docker production
  async rewrites() {
    return [
      {
        source: "/backend/:path*",
        destination: "http://localhost:8000/api/:path*",   // gọi sang FastAPI
      },
    ];
  },
};

export default nextConfig;
