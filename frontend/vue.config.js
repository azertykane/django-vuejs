// à la racine de /frontend
module.exports = {
  devServer: {
    port: 8080,                 // par défaut
    proxy: {
      '/auth':  { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/api':   { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/media': { target: 'http://127.0.0.1:8000', changeOrigin: true },
    },
  },
};
