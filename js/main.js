// ==========================================
// Minhas Cartas - Silvano Correa
// JavaScript Principal
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });

        // Close menu when clicking on a link
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    }

    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Header scroll effect
    const header = document.querySelector('.main-header');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            header.style.boxShadow = '0 4px 30px rgba(0,0,0,0.12)';
        } else {
            header.style.boxShadow = '0 2px 20px rgba(0,0,0,0.08)';
        }

        lastScroll = currentScroll;
    });

    // Animate elements on scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.volume-card, .timeline-item, .decade-card');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add animate-in class styles
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    // JFK Letter Language Toggle
    const toggleBtns = document.querySelectorAll('.carta-toggle .toggle-btn');
    const jfkEn = document.getElementById('jfk-en');
    const jfkPt = document.getElementById('jfk-pt');

    if (toggleBtns.length && jfkEn && jfkPt) {
        toggleBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const lang = this.dataset.lang;

                // Update buttons
                toggleBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                // Show/hide content
                if (lang === 'en') {
                    jfkEn.style.display = 'block';
                    jfkPt.style.display = 'none';
                } else {
                    jfkEn.style.display = 'none';
                    jfkPt.style.display = 'block';
                }
            });
        });
    }

    // Language Selector
    const langSelector = document.getElementById('language-selector');
    if (langSelector) {
        const langBtn = langSelector.querySelector('.language-selector-btn');
        const langOptions = langSelector.querySelectorAll('.language-option');
        const langFlag = langBtn.querySelector('.lang-flag');
        const langCode = langBtn.querySelector('.lang-code');

        const languages = {
            pt: { flag: '🇧🇷', code: 'PT', name: 'Português' },
            en: { flag: '🇺🇸', code: 'EN', name: 'English' },
            es: { flag: '🇪🇸', code: 'ES', name: 'Español' }
        };

        // Load saved language
        const savedLang = localStorage.getItem('site-language') || 'pt';
        if (savedLang !== 'pt') {
            langFlag.textContent = languages[savedLang].flag;
            langCode.textContent = languages[savedLang].code;
            langOptions.forEach(opt => {
                opt.classList.toggle('active', opt.dataset.lang === savedLang);
            });
        }

        // Toggle dropdown
        langBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            langSelector.classList.toggle('open');
        });

        // Select language
        langOptions.forEach(option => {
            option.addEventListener('click', function() {
                const lang = this.dataset.lang;
                const url = this.dataset.url;

                // Save preference
                localStorage.setItem('site-language', lang);

                // Redirect to the corresponding page if URL is provided
                if (url) {
                    window.location.href = url;
                } else {
                    // Update button
                    langFlag.textContent = languages[lang].flag;
                    langCode.textContent = languages[lang].code;

                    // Update active state
                    langOptions.forEach(opt => opt.classList.remove('active'));
                    this.classList.add('active');

                    // Close dropdown
                    langSelector.classList.remove('open');

                    // Show notification
                    showLanguageNotification(languages[lang].name);
                }
            });
        });

        // Close when clicking outside
        document.addEventListener('click', function(e) {
            if (!langSelector.contains(e.target)) {
                langSelector.classList.remove('open');
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                langSelector.classList.remove('open');
            }
        });
    }

    // Language notification
    function showLanguageNotification(langName) {
        // Remove existing notification
        const existing = document.querySelector('.lang-notification');
        if (existing) existing.remove();

        // Create notification
        const notification = document.createElement('div');
        notification.className = 'lang-notification';
        notification.innerHTML = `
            <span>Idioma selecionado: <strong>${langName}</strong></span>
            <small>Tradução em breve disponível</small>
        `;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--vol2-primary, #1E3A5F);
            color: white;
            padding: 16px 24px;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            z-index: 9999;
            animation: slideIn 0.3s ease;
            display: flex;
            flex-direction: column;
            gap: 4px;
        `;

        // Add animation styles
        const animStyle = document.createElement('style');
        animStyle.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(animStyle);

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
});
