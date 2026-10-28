/**
 * Lyniq Studio - Native Interactions & Behavior Engine
 * Standalone, lightweight, and performant vanilla JS.
 */

document.addEventListener('DOMContentLoaded', () => {

  // ==========================================
  // 0. LENIS + GSAP SCROLLTRIGGER ENGINE
  // ==========================================
  let lenis = null;
  if (typeof Lenis !== 'undefined') {
    try {
      lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
        wheelMultiplier: 1.0,
        touchMultiplier: 1.5,
      });

      window.lenisInstance = lenis;

      if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add((time) => {
          lenis.raf(time * 1000);
        });
        gsap.ticker.lagSmoothing(0);
      } else {
        function raf(time) {
          lenis.raf(time);
          requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);
      }
      console.log('Lenis & GSAP ScrollTrigger synchronized successfully.');
    } catch (e) {
      console.warn('Lenis/GSAP initialization failed:', e);
    }
  }

  // ==========================================
  // 1. SERVICES INTERACTIVE TABS (MAIN STREET)
  // ==========================================
  const servicesData = [
    {
      title: 'Experiential Marketing',
      description: 'Immersive brand experiences, pop-ups and activations that create emotional connections and make your brand unforgettable.',
      image: '/assets/images/photos/service-experiential-tab.jpg',
      href: '/services/experiential-marketing'
    },
    {
      title: 'Customer Acquisition',
      description: 'Trained, face-to-face field teams that meet customers where they are and turn real conversations into loyal customers.',
      image: '/assets/images/photos/service-acquisition-tab.jpg',
      href: '/services/customer-acquisition'
    },
    {
      title: 'Market Intelligence',
      description: 'Live ground data and direct consumer feedback captured during every activation, to sharpen your strategy in real time.',
      image: '/assets/images/photos/service-intelligence-tab.jpg',
      href: '/services/market-intelligence'
    },
    {
      title: 'Territory Expansion',
      description: 'Turnkey field deployment into new cities, with talent, logistics and quality control handled by one team.',
      image: '/assets/images/photos/service-territory-tab.jpg',
      href: '/services/territory-expansion'
    }
  ];

  const serviceContainers = document.querySelectorAll('.servicesListRoot');
  serviceContainers.forEach(container => {
    const rows = container.querySelectorAll('.servicesListRow');
    const detailInner = container.querySelector('.servicesListDetailInner');
    const detailSwap = container.querySelector('.servicesListDetailSwap');
    const detailImg = container.querySelector('.servicesListDetailImage');
    const detailTitle = container.querySelector('.servicesListDetailTitle');
    const detailDesc = container.querySelector('.servicesListDetailDescription');
    const detailText = container.querySelector('.servicesListDetailText');
    let detailLink = null;
    if (detailText) {
      detailLink = document.createElement('a');
      detailLink.className = 'servicesListDetailLink';
      detailLink.textContent = 'Learn more';
      detailLink.setAttribute('aria-label', 'Learn more about this service');
      detailText.appendChild(detailLink);
      const initial = (detailTitle && servicesData.find(d => d.title === detailTitle.textContent.trim())) || servicesData[0];
      detailLink.href = initial.href;
    }

    rows.forEach((row, index) => {
      row.addEventListener('click', (e) => {
        e.preventDefault();
        const data = servicesData[index];
        if (!data) return;

        // Update active class
        rows.forEach(r => {
          r.classList.remove('isActive');
          r.setAttribute('aria-pressed', 'false');
          r.removeAttribute('aria-current');
        });
        row.classList.add('isActive');
        row.setAttribute('aria-pressed', 'true');
        row.setAttribute('aria-current', 'true');

        // Animate offset
        if (detailInner) {
          detailInner.style.setProperty('--detail-offset', String(index * 50));
        }

        // Animate swap with fade
        if (detailSwap) {
          detailSwap.style.opacity = '0';
          detailSwap.style.transform = 'translateY(10px)';
          setTimeout(() => {
            if (detailImg) detailImg.src = data.image;
            if (detailTitle) detailTitle.textContent = data.title;
            if (detailDesc) detailDesc.textContent = data.description;
            if (detailLink) detailLink.href = data.href;
            detailSwap.style.opacity = '1';
            detailSwap.style.transform = 'translateY(0)';
          }, 150);
        }
      });
    });
  });

  // ==========================================
  // 2. ENGAGEMENT MODELS & CONSULTATIVE PLANS (NO PRICES)
  // ==========================================
  const pricingSection = document.querySelector('[data-framer-name="Pricing"]');
  if (pricingSection) {
    const togglePeriods = pricingSection.querySelectorAll('[data-framer-name="Period"]');
    let isRetainer = false;

    const deliverables = {
      project: { basic: 'Pilot Scope', pro: 'Growth Scope', max: 'Scale Scope' },
      retainer: { basic: 'Monthly Pilot', pro: 'Monthly Growth', max: 'Monthly Scale' }
    };
    const planKeyOf = (text) => {
      for (const mode of ['project', 'retainer']) {
        for (const key of ['basic', 'pro', 'max']) {
          if (deliverables[mode][key] === text) return key;
        }
      }
      return null;
    };

    const updatePricingDisplay = () => {
      const mode = isRetainer ? 'retainer' : 'project';
      
      // Update toggle indicator
      pricingSection.querySelectorAll('[data-framer-name="Left"]').forEach(sw => {
        const ellipse = sw.querySelector('[data-framer-name="Ellipse"]');
        if (isRetainer) {
          sw.style.justifyContent = 'flex-end';
          if (ellipse) ellipse.style.transform = 'translateX(24px)';
        } else {
          sw.style.justifyContent = 'flex-start';
          if (ellipse) ellipse.style.transform = 'translateX(0px)';
        }
      });

      // Update text opacities on toggle labels
      pricingSection.querySelectorAll('[data-framer-name="Monthly"]').forEach(el => {
        el.style.opacity = isRetainer ? '0.5' : '1';
      });
      pricingSection.querySelectorAll('[data-framer-name="Annual"]').forEach(el => {
        el.style.opacity = isRetainer ? '1' : '0.5';
      });

      // Update card deliverables (NO dollar prices!)
      const cardTexts = pricingSection.querySelectorAll('p.framer-text');
      cardTexts.forEach(p => {
        const key = planKeyOf(p.textContent.trim());
        if (key) p.textContent = deliverables[mode][key];
      });
    };

    togglePeriods.forEach(period => {
      period.style.cursor = 'pointer';
      period.addEventListener('click', () => {
        isRetainer = !isRetainer;
        updatePricingDisplay();
      });
    });

    // Make all pricing buttons smoothly scroll to contact form
    pricingSection.querySelectorAll('button, a[data-framer-name*="Start"], a[data-framer-name*="Button"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const contactSec = document.querySelector('[data-framer-name="Contact"]') || document.querySelector('#contact') || document.querySelector('footer');
        if (contactSec) {
          if (window.lenisInstance) {
            window.lenisInstance.scrollTo(contactSec, { offset: -50, duration: 1.2 });
          } else {
            contactSec.scrollIntoView({ behavior: 'smooth' });
          }
        }
      });
    });
  }

  // ==========================================
  // 3. FAQ ACCORDION (Expand / Collapse)
  // ==========================================
  const faqSection = document.querySelector('[data-framer-name="FAQ"]');
  if (faqSection) {
    const questions = faqSection.querySelectorAll('[data-framer-name="Question"]');
    
    questions.forEach((q, idx) => {
      const answer = q.parentElement.querySelector('[data-framer-name="answer"]');
      if (!answer) return;

      // Add wrapper styles for clean animation
      answer.classList.add('faq-answer-wrap');
      
      // First item can be open, remaining closed initially
      if (idx === 0) {
        answer.style.maxHeight = answer.scrollHeight + 40 + 'px';
        answer.style.opacity = '1';
        answer.style.marginTop = '16px';
        q.setAttribute('data-faq-open', 'true');
      } else {
        answer.style.maxHeight = '0px';
        answer.style.opacity = '0';
        answer.style.marginTop = '0px';
        q.setAttribute('data-faq-open', 'false');
      }

      q.addEventListener('click', () => {
        const isOpen = q.getAttribute('data-faq-open') === 'true';
        
        // Close siblings
        questions.forEach(otherQ => {
          if (otherQ !== q) {
            otherQ.setAttribute('data-faq-open', 'false');
            const otherA = otherQ.parentElement.querySelector('[data-framer-name="answer"]');
            if (otherA) {
              otherA.style.maxHeight = '0px';
              otherA.style.opacity = '0';
              otherA.style.marginTop = '0px';
            }
          }
        });

        // Toggle current
        if (isOpen) {
          q.setAttribute('data-faq-open', 'false');
          answer.style.maxHeight = '0px';
          answer.style.opacity = '0';
          answer.style.marginTop = '0px';
        } else {
          q.setAttribute('data-faq-open', 'true');
          answer.style.maxHeight = answer.scrollHeight + 40 + 'px';
          answer.style.opacity = '1';
          answer.style.marginTop = '16px';
        }
      });
    });
  }

  // ==========================================
  // 4. HEADER / BURGER MENU
  // ==========================================
  const menuButtons = document.querySelectorAll('[data-framer-name="Header / Burger menu"], [data-framer-name="MENU"]');
  menuButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      // nested menu elements both listen: handle each click once
      if (e.__msMenuHandled) return;
      e.__msMenuHandled = true;
      const header = btn.closest('header');
      if (!header) return;

      const isDesktopClosed = header.classList.contains('framer-v-m5ha19');
      const isPhoneClosed = header.classList.contains('framer-v-19vil5u');

      if (isDesktopClosed) {
        header.classList.remove('framer-v-m5ha19');
        header.style.height = 'auto';
      } else if (header.classList.contains('framer-185cz0f') && !isPhoneClosed) {
        header.classList.add('framer-v-m5ha19');
        header.style.height = '50px';
      }

      if (isPhoneClosed) {
        header.classList.remove('framer-v-19vil5u');
        header.classList.add('framer-v-7tbwy4');
        header.style.height = 'auto';
      } else if (header.classList.contains('framer-v-7tbwy4')) {
        header.classList.remove('framer-v-7tbwy4');
        header.classList.add('framer-v-19vil5u');
        header.style.height = '70px';
      }
    });
  });

  // ==========================================
  // 5. CONTACT & NEWSLETTER FORMS
  // ==========================================
  const forms = document.querySelectorAll('form[data-framer-form]');
  forms.forEach(form => {
    // status line shown under the form (no browser alerts)
    const status = document.createElement('p');
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.style.cssText = 'margin:14px 0 0;font:500 14px/1.5 Inter,sans-serif;color:#d4af37;display:none';
    form.appendChild(status);
    const say = (msg, ok) => {
      status.textContent = msg;
      status.style.display = 'block';
      status.style.color = ok ? '#d4af37' : '#ff8a80';
    };

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]') || form.querySelector('input[type="submit"]');
      const label = submitBtn ? submitBtn.querySelector('p') : null;
      const origText = label ? label.textContent : '';
      const setLabel = (txt) => { if (label) label.textContent = txt; };
      if (submitBtn) submitBtn.disabled = true;
      setLabel('Sending...');

      const data = new FormData(form);
      data.append('page', location.pathname);

      fetch('/api/contact.php', { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
        .then(r => r.json().then(j => ({ ok: r.ok && j.ok, j })))
        .then(res => {
          if (res.ok) {
            form.reset();
            setLabel('Sent');
            say('Thank you! Your message has been received. The Main Street team will get back to you shortly.', true);
          } else {
            setLabel(origText || 'Submit');
            say((res.j && res.j.error) || 'Something went wrong. Please check your details and try again.', false);
          }
        })
        .catch(() => {
          setLabel(origText || 'Submit');
          say('We could not send your message right now. Please try again in a moment or email us directly.', false);
        })
        .finally(() => {
          if (submitBtn) submitBtn.disabled = false;
          setTimeout(() => setLabel(origText || 'Submit'), 4000);
        });
    });
  });

  // ==========================================
  // 6. SMOOTH SCROLL FOR HASH LINKS
  // ==========================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href').slice(1);
      if (!targetId) return;
      const targetEl = document.getElementById(targetId) || document.querySelector(`[data-framer-name="${targetId}"]`);
      if (targetEl) {
        e.preventDefault();
        if (window.lenisInstance) {
          window.lenisInstance.scrollTo(targetEl, { offset: -60, duration: 1.2 });
        } else {
          targetEl.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });

  // ==========================================
  // 7. GSAP CINEMATIC SCROLL EFFECTS
  // ==========================================
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    // ------------------------------------------
    // A. HERO ZOOM-OUT & PARALLAX
    // ------------------------------------------
    const heroBg = document.querySelector('[data-framer-name="Hero"] [data-framer-name="BG"], [data-framer-name="BG"]');
    if (heroBg) {
      gsap.fromTo(heroBg,
        { scale: 1.15, y: 0 },
        {
          scale: 1.0,
          y: 70,
          ease: 'none',
          scrollTrigger: {
            trigger: heroBg.closest('section') || heroBg,
            start: 'top top',
            end: 'bottom top',
            scrub: 0.5,
          }
        }
      );
    }

    const heroSection = document.querySelector('[data-framer-name="Hero"]');
    if (heroSection) {
      const heroText = heroSection.querySelectorAll('h1, [data-framer-name="Lyniq"], [data-framer-name="©19-24"]');
      heroText.forEach(el => {
        gsap.to(el, {
          y: -50,
          opacity: 0.7,
          ease: 'none',
          scrollTrigger: {
            trigger: heroSection,
            start: 'top top',
            end: 'bottom top',
            scrub: 0.5,
          }
        });
      });
    }

    // ------------------------------------------
    // B. SECTION REVEALS (FADE-UP & STAGGER)
    // ------------------------------------------
    const revealTargets = document.querySelectorAll(
      'section:not([data-framer-name="Hero"]) [data-framer-name="Heading"], ' +
      'section:not([data-framer-name="Hero"]) [data-framer-name="Top"], ' +
      '[data-framer-name="Pricing"] [data-framer-name="Container"], ' +
      '.servicesListRoot, ' +
      '[data-framer-name="FAQ"] [data-framer-name="Container"]'
    );

    revealTargets.forEach(el => {
      gsap.fromTo(el,
        { opacity: 0.85, y: 20 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 92%',
            toggleActions: 'play none none none',
            once: true
          }
        }
      );
    });

    // ------------------------------------------
    // C. DESCRIPTION ZOOM SCRUB ("From ordinary to extraordinary")
    // ------------------------------------------
    const descSvg = document.querySelector('[data-framer-name="Description"] svg');
    if (descSvg) {
      gsap.fromTo(descSvg,
        { scale: 1.12 },
        {
          scale: 1.0,
          ease: 'none',
          scrollTrigger: {
            trigger: descSvg.closest('section'),
            start: 'top 85%',
            end: 'center center',
            scrub: true
          }
        }
      );
    }

    // ------------------------------------------
    // D. BENEFITS CARDS STAGGERED ENTRANCE
    // ------------------------------------------
    const benefitCards = document.querySelectorAll('[data-framer-name="Benefits"] [data-framer-name="Grid"] > div, [data-framer-name="Benefits"] [data-framer-name="Content"]');
    if (benefitCards.length) {
      gsap.fromTo(benefitCards,
        { opacity: 0.9, y: 15 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          stagger: 0.1,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: '[data-framer-name="Benefits"]',
            start: 'top 85%',
            toggleActions: 'play none none none',
            once: true
          }
        }
      );
    }

    // ------------------------------------------
    // E. PROJECT CARDS STAGGERED 2-COLUMN PARALLAX
    // ------------------------------------------
    const projectCards = document.querySelectorAll('.ms-project-parallax');
    projectCards.forEach((card, i) => {
      const speed = (i % 2 === 0) ? -40 : -90;
      gsap.to(card, {
        y: speed,
        ease: 'none',
        scrollTrigger: {
          trigger: card,
          start: 'top bottom',
          end: 'bottom top',
          scrub: 0.8,
        }
      });
    });

    // ------------------------------------------
    // E. REFRESH SCROLLTRIGGER AFTER INITIAL LOAD
    // ------------------------------------------
    setTimeout(() => {
      ScrollTrigger.refresh();
      console.log('ScrollTrigger refreshed & active.');
    }, 400);
  }

});

/* ---------- Work / Services category filter ---------- */
(function () {
  function init() {
    var bar = document.querySelector('.framer-1utq7j3[data-border]');
    var cards = [].slice.call(document.querySelectorAll('a.framer-dmnnwu[data-tags]'));
    if (!bar || !cards.length) return;
    var chips = [].slice.call(bar.querySelectorAll('.framer-FxY2X'));
    function label(c) { return (c.textContent || '').replace(/\s+/g, ' ').trim(); }
    function apply(l) {
      chips.forEach(function (c) {
        var p = c.querySelector('p');
        if (p) p.style.color = label(c) === l ? 'rgb(12, 12, 12)' : 'rgba(0, 0, 0, 0.4)';
        c.setAttribute('aria-pressed', label(c) === l ? 'true' : 'false');
      });
      cards.forEach(function (card) {
        var tags = (card.getAttribute('data-tags') || '').split('|');
        card.style.display = (l === 'All' || tags.indexOf(l) > -1) ? '' : 'none';
      });
      if (window.ScrollTrigger && window.ScrollTrigger.refresh) window.ScrollTrigger.refresh();
    }
    chips.forEach(function (c) {
      c.style.cursor = 'pointer';
      c.setAttribute('role', 'button');
      c.addEventListener('click', function (e) { e.preventDefault(); apply(label(c)); });
      c.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); apply(label(c)); }
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
