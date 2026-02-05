// Shared navbar component with hamburger menu for mobile
function createNavbar(activePage) {
    const navHTML = `
        <nav class="navbar">
            <a class="brand" href="index.html">
                <div class="brand_box">
                    <img src="assets/images/common/logo-white.png" alt="LOGO">
                    <div class="brand_text">
                        <div>
                            <p class="title">Log 🪵</p>
                        </div>
                        <div>
                            <p class="tagline">Raymond Fong How</p>
                        </div>
                    </div>
                </div>
            </a>
            <div class="nav_blank"></div>
            
            <!-- Desktop nav -->
            <div class="nav_desktop">
                <div class="nav_opt ${activePage === 'dashboard' ? 'nav-active' : ''}">
                    <a href="Dashboard.html"><p>Dashboard</p></a>
                </div>
                <div class="nav_opt ${activePage === 'fields' ? 'nav-active' : ''}">
                    <a href="Fields.html"><p>Fields</p></a>
                </div>
                <div class="nav_opt ${activePage === 'daily' ? 'nav-active' : ''}">
                    <a href="Daily.html"><p>Daily</p></a>
                </div>
                <div class="nav_opt ${activePage === 'about' ? 'nav-active' : ''}">
                    <a href="About Me.html"><p>About Me</p></a>
                </div>
            </div>
            
            <!-- Mobile hamburger -->
            <div class="nav_hamburger">
                <button class="hamburger-btn" aria-label="Menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </nav>
        
        <!-- Mobile menu overlay -->
        <div class="mobile-menu">
            <div class="mobile-menu-content">
                <a href="Dashboard.html" class="${activePage === 'dashboard' ? 'active' : ''}">Dashboard</a>
                <a href="Fields.html" class="${activePage === 'fields' ? 'active' : ''}">Fields</a>
                <a href="Daily.html" class="${activePage === 'daily' ? 'active' : ''}">Daily</a>
                <a href="About Me.html" class="${activePage === 'about' ? 'active' : ''}">About Me</a>
            </div>
        </div>
    `;

    let header = document.querySelector('header');
    if (!header) {
        header = document.createElement('header');
        document.body.prepend(header);
    }

    header.insertAdjacentHTML('beforeend', navHTML);
    
    // Hamburger menu toggle
    const hamburger = document.querySelector('.hamburger-btn');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });
        
        // Close menu when clicking a link
        const menuLinks = mobileMenu.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
            });
        });
        
        // Close menu when clicking overlay
        mobileMenu.addEventListener('click', (e) => {
            if (e.target === mobileMenu) {
                hamburger.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });
    }
    
    // Scroll behavior
    const navEl = document.querySelector('.navbar');
    if (navEl) {
        window.addEventListener('scroll', () => {
            if (window.scrollY >= 200) {
                navEl.classList.add("navbar-scrolled");
            } else {
                navEl.classList.remove("navbar-scrolled");
            }
        });
    }
}

function getActivePage() {
    const path = window.location.pathname;
    if (path.includes('Dashboard')) return 'dashboard';
    if (path.includes('Fields')) return 'fields';
    if (path.includes('Daily')) return 'daily';
    if (path.includes('About')) return 'about';
    return '';
}

document.addEventListener('DOMContentLoaded', () => {
    createNavbar(getActivePage());
});
