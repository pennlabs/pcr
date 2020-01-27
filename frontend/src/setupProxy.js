const proxy = require('http-proxy-middleware')

module.exports = function(app) {
  const proxy_url = process.env.PROXY_URL || 'http://localhost:8000'
  app.use(proxy('/api', {
    logLevel: 'debug',
    target: proxy_url,
    changeOrigin: true,
    secure: false,
  }))
  app.use(proxy('/accounts', {
    logLevel: 'debug',
    target: proxy_url,
    changeOrigin: true,
    secure: false,
  }))
}
