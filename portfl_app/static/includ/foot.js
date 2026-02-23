/* =========================
   THEME GLOBAL
========================= */
const themeBtn = document.getElementById('themeToggle');
const html = document.documentElement;

// Charger le thème sauvegardé
const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', savedTheme);
updateThemeText();

themeBtn.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeText();
});

function updateThemeText() {
    themeBtn.textContent =
        html.getAttribute('data-theme') === 'dark'
            ? 'Mode clair'
            : 'Mode sombre';
}
/* =========================
   LANGUE VIA NAVIGATEUR
========================= */

// Détection langue navigateur
const browserLang = navigator.language || navigator.userLanguage;
const defaultLang = browserLang.startsWith('fr') ? 'fr' : 'en';

// Langue sauvegardée ou navigateur
const savedLang = localStorage.getItem('lang') || defaultLang;

// Appliquer la langue au document
document.documentElement.lang = savedLang;

// Mettre à jour le select
const langSelect = document.getElementById('languageSelect');
if (langSelect) {
    langSelect.value = savedLang;

    langSelect.addEventListener('change', () => {
        const lang = langSelect.value;
        localStorage.setItem('lang', lang);
        document.documentElement.lang = lang;

        // IMPORTANT : recharge pour que le navigateur traduise
        location.reload();
    });
}

