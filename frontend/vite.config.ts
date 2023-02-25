import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: "../metamemoapp/templates",
    assetsDir: "static",
    chunkSizeWarningLimit: 1000,
  },
  server: {
    proxy: {
      "/api": {
        ws: true,
        changeOrigin: true,
        secure: false,
        target: "http://localhost:5000",
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
