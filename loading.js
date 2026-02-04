// Loading state manager
class LoadingManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }
    
    show() {
        if (this.container) {
            this.container.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner"></div>
                    <p>Loading...</p>
                </div>
            `;
        }
    }
    
    hide() {
        const spinner = this.container?.querySelector('.loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    }
    
    error(message) {
        if (this.container) {
            this.container.innerHTML = `
                <div class="error-message">
                    <p>${message}</p>
                </div>
            `;
        }
    }
}
