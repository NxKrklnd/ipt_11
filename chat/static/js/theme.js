// Check for system dark mode preference
function getSystemThemePreference() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Get theme from localStorage or system preference
function getThemePreference() {
    return localStorage.getItem('theme') || getSystemThemePreference();
}

// Set theme preference and update UI
function setThemePreference(theme) {
    // Update localStorage
    localStorage.setItem('theme', theme);
    
    // Update UI
    if (theme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    
    // Update button icons visibility (handled by Tailwind classes)
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
    // Apply initial theme
    setThemePreference(getThemePreference());
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            setThemePreference(e.matches ? 'dark' : 'light');
        }
    });
});