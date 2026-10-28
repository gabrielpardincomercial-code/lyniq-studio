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
      description: 'We design and produce immersive brand experiences, pop-ups, and experiential environments that forge emotional connections with your audience.',
      image: './assets/images/T5XSyGg3skqWFq4gynSvi2wGqHU.jpg'
    },
    {
      title: 'Customer Acquisition',
      description: 'Elite face-to-face field teams that engage consumers directly in high-traffic commercial hubs, qualifying and converting with high retention.',
      image: './assets/images/SVNjJOBLJO0tL5qGNY8CExU1fA.jpg'
    },
    {
      title: 'Market Intelligence',
      description: 'Real-time ground data collection and consumer feedback during live activations to refine your broader campaigns with absolute precision.',
      image: './assets/images/F5zSpVx8lP6Sy03URQXBu2RRUbg.jpg'
    },
    {
      title: 'Territory Expansion',
      description: 'Turnkey operational deployment into new metropolitan regions, managing talent curation, compliance, logistics, and executive oversight.',
      image: './assets/images/AlJTmhoexT1QmxuwZ7OiLjeKtUM.jpg'
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
      project: {
        basic: 'Custom Scope',
        pro: 'Tailored SLA',
        max: 'Dedicated Fleet'
      },
      retainer: {
        basic: 'Bespoke Scope',
        pro: 'Executive SLA',
        max: 'Sovereign Fleet'
      }
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
        const text = p.textContent.trim();
        if (text.includes('$') || text.includes('Custom') || text.includes('Bespoke') || text.includes('Tailored') || text.includes('Dedicated') || text.includes('SLA') || text.includes('Fleet')) {
          if (text.includes('999') || text.includes('699') || text.includes('Custom Scope') || text.includes('Bespoke Scope')) {
            p.textContent = deliverables[mode].basic;
          } else if (text.includes('2,999') || text.includes('2,499') || text.includes('2,099') || text.includes('Tailored SLA') || text.includes('Executive SLA')) {
            p.textContent = deliverables[mode].pro;
          } else if (text.includes('4,999') || text.includes('3,499') || text.includes('Dedicated Fleet') || text.includes('Sovereign Fleet')) {
            p.textContent = deliverables[mode].max;
          }
        }
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
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]') || form.querySelector('input[type="submit"]');
      const origText = submitBtn ? submitBtn.innerText : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Sending...';
      }

      setTimeout(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = 'Sent Successfully!';
        }
        alert('Thank you! Your inquiry has been received by Main Street. Our executive team in Culver City will contact you within 24 hours.');
        form.reset();
        setTimeout(() => {
          if (submitBtn) submitBtn.innerText = origText || 'Submit';
        }, 3000);
      }, 600);
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
    const projectCards = document.querySelectorAll('.framer-lux5qc, [data-framer-name*="Project"]');
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
    // D. NUMBERS ANIMATED COUNTERS
    // ------------------------------------------
    const numbersSection = document.querySelector('[data-framer-name="Numbers"]');
    if (numbersSection) {
      const stats = [
        { labels: ['Retention Increase', 'Websites launched', 'Retention'], target: 45, decimals: 0 },
        { labels: ['Consumers Engaged', 'Users reached', 'Consumers'], target: 2.5, decimals: 1 },
        { labels: ['Client Retention Rate', 'Client satisfaction rate', 'Satisfaction'], target: 98, decimals: 0 },
        { labels: ['Expansion Markets', 'Years of expertise', 'Markets'], target: 12, decimals: 0 }
      ];

      // Set initial numbers immediately so they never display 0
      stats.forEach(stat => {
        const labels = Array.from(numbersSection.querySelectorAll('*')).filter(el => 
          el.children.length === 0 && el.innerText && stat.labels.some(l => el.innerText.trim().includes(l))
        );
        labels.forEach(label => {
          const itemRoot = label.closest('.framer-11g5wz4')?.parentElement || label.parentElement?.parentElement?.parentElement?.parentElement;
          if (itemRoot) {
            const numSpans = Array.from(itemRoot.querySelectorAll('span')).filter(s => /^\d+(\.\d+)?$/.test(s.innerText.trim()));
            numSpans.forEach(span => {
              span.innerText = stat.decimals === 1 ? stat.target.toFixed(1) : Math.round(stat.target).toString();
            });
          }
        });
      });
    }

    // ------------------------------------------
    // E. REFRESH SCROLLTRIGGER AFTER INITIAL LOAD
    // ------------------------------------------
    setTimeout(() => {
      ScrollTrigger.refresh();
      console.log('ScrollTrigger refreshed & active.');
    }, 400);
  }

});
