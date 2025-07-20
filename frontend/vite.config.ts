import { defineConfig } from 'vite'
import { consoleForwardPlugin } from 'vite-console-forward-plugin'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    // Forward browser console logs to backend for centralized logging
    consoleForwardPlugin({
      enabled: process.env.NODE_ENV === 'development',
      endpoint: '/api/debug/client-logs',
      levels: ['log', 'warn', 'error', 'info', 'debug'],
      // Add timestamp and source metadata
      metadata: {
        source: 'frontend',
        timestamp: true
      }
    }),
    // Add your other plugins here
  ],
  
  // Development server configuration
  server: {
    port: 5173,
    // Proxy API requests to backend (adjust port as needed)
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})