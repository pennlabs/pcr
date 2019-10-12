const proxy = require('http-proxy-middleware');


module.exports = function(app) {
    app.get('/api/display/token', function(req, res) {
        res.redirect(req.query.redirect);
    });
    const proxy_url = process.env.PROXY_URL || 'https://penncoursereview.com';
    app.use(proxy('/api', {
        logLevel: 'debug',
        target: proxy_url,
        changeOrigin: true,
        secure: false
    }));
};
