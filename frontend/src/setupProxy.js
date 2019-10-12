const proxy = require('http-proxy-middleware');


module.exports = function(app) {
    app.get('/api/display/token', function(req, res) {
        res.redirect(req.query.redirect);
    });
    app.use(proxy('/api', {
        target: 'https://penncoursereview.com',
        changeOrigin: true,
        secure: false
    }));
};
