// Auto-load CSS files - Place in <head> to prevent FOUC
(function() {
    const cssFiles = [
        'static/css/style-general.css',
        'static/css/style-fonts.css',
        'static/css/style-nav.css',
        'static/css/style-intro.css',
        'static/css/style-coming_soon.css',
        'static/css/style-dashboard.css',
        'static/css/style-update.css',
        'static/css/style-category_update.css',
        'static/css/style-cat_list.css',
        'mobile.css'
    ];
    
    cssFiles.forEach(file => {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = file;
        document.head.appendChild(link);
    });
})();
