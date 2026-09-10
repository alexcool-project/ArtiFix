/* ============================================
   ARTIFIX LANDING — SCRIPT.JS
   ============================================ */

(function () {
    'use strict';

    /* === MENU MOBILE === */
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function () {
            const isOpen = mainNav.classList.toggle('open');
            menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });

        // Chiudi il menu al click su un link (mobile)
        mainNav.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                if (window.innerWidth <= 768) {
                    mainNav.classList.remove('open');
                    menuToggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    /* === HEADER SHADOW ON SCROLL === */
    const header = document.querySelector('.site-header');
    if (header) {
        const onScroll = function () {
            if (window.scrollY > 10) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* === SMOOTH SCROLL PER ANCORE INTERNE === */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href === '') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    /* === ANIMAZIONE FADE-IN ALLO SCROLL (IntersectionObserver) === */
    if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const animatedElements = document.querySelectorAll(
            '.feature-card, .why-card, .format-category, .contact-card, .sponsor-banner-large'
        );

        // Imposta opacità 0 iniziale per elementi fuori viewport
        animatedElements.forEach(function (el) {
            const rect = el.getBoundingClientRect();
            if (rect.top > window.innerHeight) {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            }
        });

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animatedElements.forEach(function (el) {
            observer.observe(el);
        });
    }

    /* === EVITA LO SCROLL ORIZZONTALE SU MOBILE === */
    document.documentElement.style.overflowX = 'hidden';

    /* === CONSOLE MESSAGE === */
    console.log(
        '%c🛠️ ArtiFix%c — Convert. Fix. Deliver.\\n%cSito: https://www.artifix.it\\nApp:  https://artifix.streamlit.app',
        'font-size: 20px; font-weight: 700; color: #1f77b4;',
        'font-size: 14px; color: #555;',
        'font-size: 12px; color: #888;'
    );
})();
