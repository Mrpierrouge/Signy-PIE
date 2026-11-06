import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import { VitePWA } from "vite-plugin-pwa"

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // Makes the app installable on mobile (manifest + service worker)
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "Signy",
        short_name: "Signy",
        description: "Apprendre la langue des signes française",
        lang: "fr",
        start_url: "/",
        display: "standalone",
        background_color: "#110003",
        theme_color: "#110003",
        icons: [
          { src: "icons/icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "icons/icon-512.png", sizes: "512x512", type: "image/png" },
          {
            src: "icons/icon-maskable-512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
      workbox: {
        // MediaPipe files are too large to pre-download at install:
        // they are cached the first time they are used instead.
        globIgnores: ["mediapipe/**"],
        runtimeCaching: [
          {
            urlPattern: /\/mediapipe\//,
            handler: "CacheFirst",
            options: { cacheName: "mediapipe" },
          },
        ],
      },
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  // Also applies to `vite preview`: when `preview.proxy` / `preview.allowedHosts` are not set,
  // Vite reuses the `server` values (see https://vite.dev/config/preview-options#preview-proxy)
  server: {
    // With VITE_API_URL=/api the front reaches the backend through this proxy (same origin),
    // so only the front has to be exposed when testing on a phone through an HTTPS tunnel
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
    // HTTPS tunnel domains allowed to reach the dev/preview server
    allowedHosts: [".trycloudflare.com", ".ngrok-free.app", ".ngrok-free.dev"],
  },
})
