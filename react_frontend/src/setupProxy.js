import { createProxyMiddleware } from 'http-proxy-middleware';

export default function(app) {
  app.use(
    createProxyMiddleware('/galaxy-api', {
      target: 'http://localhost:5000',
      changeOrigin: true,
    })
  );

  app.use(
    createProxyMiddleware('/send-bounty-hunters-api', {
      target: 'http://localhost:5000',
      changeOrigin: true,
    })
  );
};