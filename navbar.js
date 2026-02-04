// Shared navbar component - loaded by all pages
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
            <div class="nav_opt">
                <div class="${activePage === 'dashboard' ? 'nav-active' : ''}">
                    <a href="Dashboard.html">
                        <p>Dashboard</p>
                    </a>
                </div>
            </div>
            <div class="nav_opt">
                <div class="${activePage === 'fields' ? 'nav-active' : ''}">
                    <a href="Fields.html">
                        <p>Fields</p>
                    </a>
                </div>
            </div>
            <div class="nav_opt">
                <div class="${activePage === 'daily' ? 'nav-active' : ''}">
                    <a href="Daily.html">
                        <p>Daily</p>
                    </a>
                </div>
            </div>
            <div class="nav_opt">
                <div class="${activePage === 'about' ? 'nav-active' : ''}">
                    <a href="About Me.html">
                        <p>About Me</p>
                    </a>
                </div>
            </div>
        </nav>
    `;
    
    // Insert navbar into the header
    const header = document.querySelector('header');
    if (header) {
        header.insertAdjacentHTML('beforeend', navHTML);
    }
    
    // Add scroll behavior
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

// Auto-detect which page we're on based on URL
function getActivePage() {
    const path = window.location.pathname;
    if (path.includes('Dashboard')) return 'dashboard';
    if (path.includes('Fields')) return 'fields';
    if (path.includes('Daily')) return 'daily';
    if (path.includes('About')) return 'about';
    return '';
}

// Initialize navbar when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    createNavbar(getActivePage());
});
