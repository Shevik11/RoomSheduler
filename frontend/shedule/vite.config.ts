import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Components from "unplugin-vue-components/vite";
// import VueDevTools from 'vite-plugin-vue-devtools'
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          devtools: !process.env.NODE_ENV || process.env.NODE_ENV !== 'production'
        }
      }
    }),
    Components({
      dts: true,
      dirs: ["src/components"],
    }),
    // VueDevTools(), // Вимкнено для production
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    target: "esnext",
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router'],
          ui: ['vue-multiselect']
        }
      }
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: false, 
      ignored: /node_modules/
    }
  },
  optimizeDeps: {
    include: ['vue', 'vue-router', 'vue-multiselect']
  }
});
