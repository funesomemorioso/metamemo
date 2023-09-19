import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: "./build/",
    assetsDir: "static",
    chunkSizeWarningLimit: 1500,
  },
  server: {
    proxy: {
      "/api": {
        ws: true,
        changeOrigin: true,
        secure: false,
        target: "http://localhost:5000",
      },
    },
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
