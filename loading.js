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
                    <p>⚠️ ${message}</p>
                </div>
            `;
        }
    }
}

// Add CSS for loading spinner (inject into page)
const loadingStyles = document.createElement('style');
loadingStyles.textContent = `
    .loading-spinner {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
        min-height: 300px;
    }
    
    .spinner {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(255, 255, 255, 0.1);
        border-top-color: #fff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .loading-spinner p {
        margin-top: 20px;
        color: rgba(255, 255, 255, 0.7);
        font-size: 14px;
    }
    
    .error-message {
        text-align: center;
        padding: 40px 20px;
        color: #ff6b6b;
    }
    
    .nav-active {
        border-bottom: 2px solid #fff;
        font-weight: bold;
    }
`;
document.head.appendChild(loadingStyles);
