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
  // 1. SERVICES INTERACTIVE TABS
  // ==========================================
  const servicesData = [
    {
      title: 'Branding',
      description: 'We create impactful brand identities that differentiate your business and connect with your audience.',
      image: './assets/images/T5XSyGg3skqWFq4gynSvi2wGqHU.jpg'
    },
    {
      title: 'Development',
      description: 'From front-end interactions to back-end functionality, we deliver robust solutions that grow with your business.',
      image: './assets/images/SVNjJOBLJO0tL5qGNY8CExU1fA.jpg'
    },
    {
      title: 'Websites',
      description: 'We build custom websites that go beyond aesthetics, balancing design and functionality to captivate your audience and drive engagement.',
      image: './assets/images/F5zSpVx8lP6Sy03URQXBu2RRUbg.jpg'
    },
    {
      title: 'Design support',
      description: 'We’re here to help with everything from small updates to full-scale redesigns, tailored to your evolving needs.',
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
  // 2. PRICING MONTHLY / ANNUAL TOGGLE
  // ==========================================
  const pricingSection = document.querySelector('[data-framer-name="Pricing"]');
  if (pricingSection) {
    const togglePeriods = pricingSection.querySelectorAll('[data-framer-name="Period"]');
    let isAnnual = false;

    const prices = {
      monthly: {
        basic: '$999',
        pro: '$2,999',
        max: '$4,999'
      },
      annual: {
        basic: '$699',
        pro: '$2,099',
        max: '$3,499'
      }
    };

    const updatePricingDisplay = () => {
      const mode = isAnnual ? 'annual' : 'monthly';
      
      // Update toggle indicator
      pricingSection.querySelectorAll('[data-framer-name="Left"]').forEach(sw => {
        const ellipse = sw.querySelector('[data-framer-name="Ellipse"]');
        if (isAnnual) {
          sw.style.justifyContent = 'flex-end';
          if (ellipse) ellipse.style.transform = 'translateX(24px)';
        } else {
          sw.style.justifyContent = 'flex-start';
          if (ellipse) ellipse.style.transform = 'translateX(0px)';
        }
      });

      // Update text opacities on toggle labels
      pricingSection.querySelectorAll('[data-framer-name="Monthly"]').forEach(el => {
        el.style.opacity = isAnnual ? '0.5' : '1';
      });
      pricingSection.querySelectorAll('[data-framer-name="Annual"]').forEach(el => {
        el.style.opacity = isAnnual ? '1' : '0.5';
      });

      // Update card prices
      const cardTexts = pricingSection.querySelectorAll('p.framer-text');
      cardTexts.forEach(p => {
        const text = p.textContent.trim();
        if (text === '$999' || text === '$699') {
          p.textContent = prices[mode].basic;
        } else if (text === '$2,999' || text === '$2,099') {
          p.textContent = prices[mode].pro;
        } else if (text === '$4,999' || text === '$3,499') {
          p.textContent = prices[mode].max;
        }
      });
    };

    togglePeriods.forEach(period => {
      period.style.cursor = 'pointer';
      period.addEventListener('click', () => {
        isAnnual = !isAnnual;
        updatePricingDisplay();
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
        alert('Thank you! Your inquiry has been sent to Lyniq Studio. We will contact you within 24 hours.');
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
      'section:not([data-framer-name="Hero"]) [data-framer-name="Title"], ' +
      'section:not([data-framer-name="Hero"]) [data-framer-name="Top"], ' +
      'section:not([data-framer-name="Hero"]) [data-framer-name="Category"], ' +
      '[data-framer-name="Numbers"], ' +
      '[data-framer-name="Quote"], ' +
      '[data-framer-name="Pricing"] [data-framer-name="Container"], ' +
      '.servicesListRoot, ' +
      '[data-framer-name="FAQ"] [data-framer-name="Container"]'
    );

    revealTargets.forEach(el => {
      gsap.fromTo(el,
        { opacity: 0.05, y: 35 },
        {
          opacity: 1,
          y: 0,
          duration: 0.85,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 88%',
            toggleActions: 'play none none none',
            once: true
          }
        }
      );
    });

    // ------------------------------------------
    // C. PROJECT CARDS STAGGERED PARALLAX
    // ------------------------------------------
    const projectCards = document.querySelectorAll('.framer-lux5qc, [data-framer-name*="Project"]');
    projectCards.forEach((card, i) => {
      const speed = (i % 2 === 0) ? -35 : -70;
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
      ScrollTrigger.create({
        trigger: numbersSection,
        start: 'top 85%',
        once: true,
        onEnter: () => {
          const stats = [
            { label: 'Websites launched', target: 17, decimals: 0 },
            { label: 'Users reached', target: 1.5, decimals: 1 },
            { label: 'Client satisfaction rate', target: 98, decimals: 0 },
            { label: 'Years of expertise', target: 10, decimals: 0 }
          ];

          stats.forEach(stat => {
            const labels = Array.from(numbersSection.querySelectorAll('*')).filter(el => 
              el.children.length === 0 && el.innerText && el.innerText.trim() === stat.label
            );
            labels.forEach(label => {
              const itemRoot = label.closest('.framer-11g5wz4')?.parentElement || label.parentElement?.parentElement?.parentElement?.parentElement;
              if (itemRoot) {
                const numSpans = Array.from(itemRoot.querySelectorAll('span')).filter(s => /^\d+(\.\d+)?$/.test(s.innerText.trim()));
                numSpans.forEach(span => {
                  const obj = { val: 0 };
                  gsap.to(obj, {
                    val: stat.target,
                    duration: 1.8,
                    ease: 'power2.out',
                    onUpdate: () => {
                      span.innerText = stat.decimals === 1 ? obj.val.toFixed(1) : Math.round(obj.val).toString();
                    }
                  });
                });
              }
            });
          });
        }
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
