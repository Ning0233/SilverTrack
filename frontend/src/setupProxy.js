const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function setupProxy(app) {
  const target = process.env.REACT_APP_API_PROXY_TARGET || 'http://localhost:5001';

  app.use(
    '/api',
    createProxyMiddleware({
      target,
      changeOrigin: true,
      // app.use('/api', ...) strips '/api' before forwarding; add it back for Flask routes.
      pathRewrite: (path) => `/api${path}`,
    })
  );
};
