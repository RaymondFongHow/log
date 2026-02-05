// Shared footer component
function createFooter() {
    const version = '2.0.6';
    const lastUpdated = new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
    
    const footerHTML = `
        <footer class="site-footer">
            <div class="footer-line"></div>
            <div class="footer-content">
                <p>Log © ${new Date().getFullYear()} Raymond Fong How</p>
                <p class="footer-version">Version ${version} · Last updated ${lastUpdated}</p>
            </div>
        </footer>
    `;
    
    // Find main or body and append after it
    const main = document.querySelector('main');
    if (main) {
        main.insertAdjacentHTML('afterend', footerHTML);
    } else {
        document.body.insertAdjacentHTML('beforeend', footerHTML);
    }
}

document.addEventListener('DOMContentLoaded', createFooter);
