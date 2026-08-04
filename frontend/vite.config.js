import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
  },
  build: {
    // Manual chunking keeps vendor code (react, router, animation libs)
    // in a separate cacheable bundle from application code, per the
    // spec's code-splitting requirement. Vite 8's rolldown bundler
    // requires the function form rather than the classic object form.
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (/react-router|react-dom|\/react\//.test(id)) return 'vendor';
            if (/framer-motion|swiper/.test(id)) return 'animation';
          }
        },
      },
    },
  },
})
