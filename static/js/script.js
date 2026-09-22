const toggleButton = document.querySelector('.theme-toggle');
const body = document.body;
const yearEl = document.getElementById('year');

if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

const isDarkPreferred = window.matchMedia('(prefers-color-scheme: dark)').matches;
const savedTheme = localStorage.getItem('theme');

if (savedTheme === 'light' || (!savedTheme && !isDarkPreferred)) {
  body.classList.add('light-mode');
  if (toggleButton) toggleButton.textContent = '🌙';
}

if (toggleButton) {
  toggleButton.addEventListener('click', () => {
    body.classList.toggle('light-mode');
    const nextTheme = body.classList.contains('light-mode') ? 'light' : 'dark';
    localStorage.setItem('theme', nextTheme);
    toggleButton.textContent = nextTheme === 'light' ? '🌙' : '☀️';
  });
}
