// Theme management
function getThemePreference() {
    return localStorage.getItem('theme') || 'system';
}

function setThemePreference(theme) {
    localStorage.setItem('theme', theme);
    applyTheme(theme);
}

function applyTheme(theme) {
    const isDark = theme === 'dark' || 
        (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

    document.documentElement.classList.toggle('dark', isDark);
}

// Initialize theme
const currentTheme = getThemePreference();
applyTheme(currentTheme);

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (getThemePreference() === 'system') {
        applyTheme('system');
    }
});