import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* 
  TODO: set reactStrictMode to false as otherwise the page 
  will be pushed twice in development mode, means AI APIs will 
  be balled twice.
  We need to delete it later, since other problems will occur, 
  but for now in local, we open it to save tokens.
  */
  reactStrictMode: false, 
};

export default nextConfig;
