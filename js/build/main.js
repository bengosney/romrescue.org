$('body').on('click','a[rel="external"]', function(e) {
    window.open($(this).attr('href'));
    e.preventDefault();
});
