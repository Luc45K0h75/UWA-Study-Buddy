( function() {  
    const current = window.location.pathname; // Get URL path to current page
    const navLinks = document.querySelectorAll('.nav-link');
    console.log('Current path:', current);

    // Check each link to see whether it is the active page
    navLinks.forEach(link => {
        const href = link.getAttribute('href'); // Get the href attribute of the link

        //Checks if the href matches the current path or the current path is the root and hrf is the index page
        if (href === current || (current === '/' && href === '/index')) {
            link.classList.add('active');
        }
    });

})();