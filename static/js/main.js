/* ═══════════════════════════════════════════════════════════════
   ASD STUDIO 2026 — AURORA FLUX INTERACTIVE ENGINE
   Cursor glow, floating orbs, card tilt, parallax,
   magnetic buttons, scroll animations, particles.
   ═══════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

    // ═══ 1. CURSOR GLOW — spotlight follows the mouse ═══
    const cursorGlow = document.getElementById('cursorGlow');
    const cursorDot  = document.getElementById('cursorDot');
    let mouseX = 0, mouseY = 0;
    let glowX = 0, glowY = 0;
    let dotX = 0, dotY = 0;

    document.addEventListener('mousemove', e => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animateCursor() {
        // Smooth follow for big glow
        glowX += (mouseX - glowX) * 0.06;
        glowY += (mouseY - glowY) * 0.06;
        if (cursorGlow) {
            cursorGlow.style.left = glowX + 'px';
            cursorGlow.style.top  = glowY + 'px';
        }
        // Snappy follow for small dot
        dotX += (mouseX - dotX) * 0.25;
        dotY += (mouseY - dotY) * 0.25;
        if (cursorDot) {
            cursorDot.style.left = dotX + 'px';
            cursorDot.style.top  = dotY + 'px';
        }
        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Scale glow when hovering over interactive elements
    document.querySelectorAll('a, button, .card, .review-card, .stat-card, .glass-card, .btn, input, textarea, select').forEach(el => {
        el.addEventListener('mouseenter', () => {
            if (cursorGlow) cursorGlow.classList.add('cursor-glow--active');
            if (cursorDot)  cursorDot.classList.add('cursor-dot--active');
        });
        el.addEventListener('mouseleave', () => {
            if (cursorGlow) cursorGlow.classList.remove('cursor-glow--active');
            if (cursorDot)  cursorDot.classList.remove('cursor-dot--active');
        });
    });


    // ═══ 2. PARALLAX TILT ON CARDS ═══
    const tiltCards = document.querySelectorAll('.card, .review-card, .stat-card, .glass-card, .auth-card');

    tiltCards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -4;
            const rotateY = ((x - centerX) / centerX) * 4;

            // Shine position as percentage
            const shineX = (x / rect.width) * 100;
            const shineY = (y / rect.height) * 100;

            card.style.transform = `translateY(-8px) perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            card.style.setProperty('--shine-x', shineX + '%');
            card.style.setProperty('--shine-y', shineY + '%');
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.setProperty('--shine-x', '50%');
            card.style.setProperty('--shine-y', '50%');
        });
    });


    // ═══ 3. MAGNETIC BUTTONS ═══
    document.querySelectorAll('.btn--primary, .btn--ghost').forEach(btn => {
        btn.addEventListener('mousemove', e => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });


    // ═══ 4. FLOATING ORBS — living background ═══
    function createOrbs() {
        const orbContainer = document.getElementById('floatingOrbs');
        if (!orbContainer) return;

        const orbData = [
            { size: 350, color: 'rgba(124,58,237,0.12)',  x: '15%', y: '20%', dur: 18 },
            { size: 280, color: 'rgba(6,182,212,0.10)',   x: '75%', y: '15%', dur: 22 },
            { size: 200, color: 'rgba(168,85,247,0.08)',  x: '50%', y: '60%', dur: 25 },
            { size: 160, color: 'rgba(34,211,238,0.07)',  x: '85%', y: '70%', dur: 20 },
            { size: 120, color: 'rgba(124,58,237,0.06)',  x: '10%', y: '80%', dur: 15 },
        ];

        orbData.forEach((orb, i) => {
            const el = document.createElement('div');
            el.classList.add('floating-orb');
            el.style.cssText = `
                width: ${orb.size}px;
                height: ${orb.size}px;
                background: radial-gradient(circle, ${orb.color}, transparent 70%);
                left: ${orb.x};
                top: ${orb.y};
                animation: orbFloat${i % 3} ${orb.dur}s ease-in-out infinite;
                animation-delay: ${-i * 3}s;
            `;
            orbContainer.appendChild(el);
        });
    }
    createOrbs();


    // ═══ 5. SCROLL-TRIGGERED PARALLAX BACKGROUND ═══
    const hero = document.querySelector('.hero');
    const heroAurora = document.querySelector('.hero__aurora');

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        if (heroAurora && scrollY < window.innerHeight) {
            heroAurora.style.transform = `translateX(-50%) rotate(${scrollY * 0.05}deg) scale(${1 + scrollY * 0.0003})`;
            heroAurora.style.opacity = Math.max(0.2, 0.5 - scrollY * 0.0004);
        }
    });


    // ═══ 6. INTERACTIVE MESH GRADIENT ON HERO ═══
    if (hero) {
        hero.addEventListener('mousemove', e => {
            const rect = hero.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;

            hero.style.setProperty('--mouse-x', x + '%');
            hero.style.setProperty('--mouse-y', y + '%');
        });
    }


    // ═══ 7. SCROLL REVEAL ANIMATIONS ═══
    const animElements = document.querySelectorAll('[data-animate]');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = parseInt(entry.target.dataset.delay) || 0;
                setTimeout(() => {
                    entry.target.classList.add('animated');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, delay);
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    animElements.forEach(el => revealObserver.observe(el));


    // ═══ 8. COUNTER ANIMATION ═══
    const counters = document.querySelectorAll('[data-count]');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.dataset.count);
                const duration = 2000;
                const start = performance.now();

                function tick(now) {
                    const p = Math.min((now - start) / duration, 1);
                    const eased = 1 - Math.pow(1 - p, 4);
                    el.textContent = Math.round(eased * target);
                    if (p < 1) requestAnimationFrame(tick);
                    else el.textContent = target;
                }
                requestAnimationFrame(tick);
                counterObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });
    counters.forEach(el => counterObserver.observe(el));


    // ═══ 9. NAVBAR ═══
    const nav = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (nav) nav.classList.toggle('scrolled', window.scrollY > 40);
    });


    // ═══ 10. MOBILE MENU ═══
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
            document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
        });
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }


    // ═══ 11. SMOOTH ANCHOR SCROLL ═══
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const target = document.querySelector(a.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });


    // ═══ 12. FLASH AUTO-DISMISS ═══
    document.querySelectorAll('[data-flash]').forEach((flash, i) => {
        setTimeout(() => {
            flash.style.transition = 'opacity .4s ease, transform .4s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(30px)';
            setTimeout(() => flash.remove(), 400);
        }, 4000 + i * 600);
    });


    // ═══ 13. TEXT TYPING EFFECT ON HERO BADGE ═══
    const badge = document.querySelector('.hero__badge');
    if (badge) {
        badge.style.opacity = '0';
        badge.style.transform = 'translateY(10px)';
        setTimeout(() => {
            badge.style.transition = 'all .6s cubic-bezier(.34,1.56,.64,1)';
            badge.style.opacity = '1';
            badge.style.transform = 'translateY(0)';
        }, 300);
    }


    // ═══ 14. RIPPLE EFFECT ON BUTTONS ═══
    document.querySelectorAll('.btn--primary').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.classList.add('btn-ripple');
            const rect = this.getBoundingClientRect();
            ripple.style.left = (e.clientX - rect.left) + 'px';
            ripple.style.top = (e.clientY - rect.top) + 'px';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

});
