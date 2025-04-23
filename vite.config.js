import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        // 全局变量
        additionalData: '@import "./src/assets/style/global.scss";',
      },
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    open: true,
    host: '0.0.0.0',
    port: 7777,
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:7878',  //本地
        changeOrigin: true,
        // rewrite: path => path.replace(/^\/api/, ''),
        secure: true
      },
    },
  },
})
