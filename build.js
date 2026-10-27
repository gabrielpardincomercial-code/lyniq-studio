const fs = require('fs');
const path = require('path');

const srcDir = '/tmp/lyniq_pages';
const outDir = __dirname;
const imgMap = JSON.parse(fs.readFileSync(path.join(outDir, 'image_map.json'), 'utf8'));
const fontMap = JSON.parse(fs.readFileSync(path.join(outDir, 'font_map.json'), 'utf8'));

// Route mapping
const routeMap = {
  'index.html': 'index.html',
  'about.html': 'about.html',
  'projects.html': 'projects.html',
  'blog.html': 'blog.html',
  'contact.html': 'contact.html',
  'terms.html': 'terms.html',
  'privacy.html': 'privacy.html',
  'projects_vero-app-development.html': 'projects/vero-app-development.html',
  'projects_stoyo-branding.html': 'projects/stoyo-branding.html',
  'projects_radiant-skincare-branding.html': 'projects/radiant-skincare-branding.html',
  'blog_how-to-balance-aesthetics-and-functionality-in-web-design.html': 'blog/how-to-balance-aesthetics-and-functionality-in-web-design.html',
  'blog_why-responsive-design-is-more-important-today-than-ever-before.html': 'blog/why-responsive-design-is-more-important-today-than-ever-before.html',
  'blog_why-mobile-first-design-is-crucial-for-modern-websites.html': 'blog/why-mobile-first-design-is-crucial-for-modern-websites.html',
  'blog_the-ultimate-checklist-for-launching-a-successful-website.html': 'blog/the-ultimate-checklist-for-launching-a-successful-website.html',
  'blog_the-secret-to-designing-high-converting-landing-pages.html': 'blog/the-secret-to-designing-high-converting-landing-pages.html',
  'blog_boosting-site-speed-key-tips-for-faster-load-times.html': 'blog/boosting-site-speed-key-tips-for-faster-load-times.html',
  'blog_building-trust-online-the-importance-of-testimonials.html': 'blog/building-trust-online-the-importance-of-testimonials.html',
  'blog_top-web-design-trends-to-watch-in-2024.html': 'blog/top-web-design-trends-to-watch-in-2024.html',
  'blog_how-to-create-a-website-that-truly-connects-with-your-audience.html': 'blog/how-to-create-a-website-that-truly-connects-with-your-audience.html',
  'blog_why-your-website-s-user-experience-is-its-greatest-asset.html': 'blog/why-your-website-s-user-experience-is-its-greatest-asset.html'
};

function processHtml(html, destRelPath) {
  const depth = destRelPath.split('/').length - 1;
  const assetPrefix = depth === 0 ? './assets/' : '../'.repeat(depth) + 'assets/';
  const rootPrefix = depth === 0 ? './' : '../'.repeat(depth);

  // 1. Decouple runtime safely (match individual scripts only)
  html = html.replace(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi, (fullMatch, attrs, content) => {
    if (attrs.includes('events.framer.com') ||
        attrs.includes('script_main') ||
        attrs.includes('type="module"') ||
        attrs.includes('framer/appear') ||
        attrs.includes('framer/handover') ||
        attrs.includes('data-framer-appear-animation') ||
        content.includes('var animator') ||
        content.includes('framer-appear-start') ||
        content.includes('Date.prototype.toLocaleString')) {
      return '';
    }
    return fullMatch;
  });

  // 2. Asset localization: Images
  html = html.replace(/\s*srcset="https:\/\/framerusercontent\.com\/images\/[^"]*"/gi, '');
  html = html.replace(/https:\/\/(?:framerusercontent\.com\/images|images\.unsplash\.com)\/([a-zA-Z0-9_\-\.]+)(?:\?[^"'\)\s,]+)?/g, (match, filename) => {
    return assetPrefix + 'images/' + filename;
  });

  // 3. Asset localization: Fonts
  html = html.replace(/https:\/\/(?:framerusercontent\.com\/assets|fonts\.gstatic\.com\/s\/[^\/]+\/[^\/]+)\/([a-zA-Z0-9_\-\.]+\.woff2?)/g, (match, filename) => {
    return assetPrefix + 'fonts/' + filename;
  });
  for (const [remote, local] of Object.entries(fontMap)) {
    const filename = path.basename(local);
    html = html.split(remote).join(assetPrefix + 'fonts/' + filename);
  }

  // 4. SSR Visibility & Animation Unlocking (The Framer SSR Trap)
  html = html.replace(/opacity:\s*0(?:\.001)?(?=[;\"'\s])/g, 'opacity: 1');
  html = html.replace(/filter:\s*blur\([^)]+\)/g, 'filter: none');
  html = html.replace(/translateY\([0-9\.\-]+px\)/g, 'translateY(0px)');

  // 5. Hide Framer badge container
  html = html.replace(/id="__framer-badge-container"/g, 'id="__framer-badge-container" style="display:none !important;"');

  // 6. Fix internal links
  html = html.replace(/href="https:\/\/lyniq\.framer\.website\/?"/g, `href="${rootPrefix}index.html"`);
  html = html.replace(/href="https:\/\/lyniq\.framer\.website\/about\/?/g, `href="${rootPrefix}about.html"`);
  html = html.replace(/href="https:\/\/lyniq\.framer\.website\/projects\/?/g, `href="${rootPrefix}projects.html"`);
  html = html.replace(/href="https:\/\/lyniq\.framer\.website\/blog\/?/g, `href="${rootPrefix}blog.html"`);
  html = html.replace(/href="https:\/\/lyniq\.framer\.website\/contact\/?/g, `href="${rootPrefix}contact.html"`);
  html = html.replace(/href="https:\/\/lyniq\.framer\.website\/terms\/?/g, `href="${rootPrefix}terms.html"`);
  html = html.replace(/href="https:\/\/lyniq\.framer\.website\/privacy\/?/g, `href="${rootPrefix}privacy.html"`);
  html = html.replace(/href="\/(about|projects|blog|contact|terms|privacy)\/?"/g, `href="${rootPrefix}$1.html"`);
  html = html.replace(/href="\/"/g, `href="${rootPrefix}index.html"`);

  // 7. Custom CSS and JS
  const customCss = `
<style id="lyniq-custom-fixes">
  /* Lyniq Native Interactions & Visual Fixes */
  #__framer-badge-container { display: none !important; }
  .framer-143iyx0-container { display: none !important; }
  a[href*="templifica"], .framer-PdQjD, #template-overlay { display: none !important; }

  /* Lenis smooth scroll styles */
  html.lenis, html.lenis body {
    height: auto;
  }
  .lenis.lenis-smooth {
    scroll-behavior: auto !important;
  }
  .lenis.lenis-smooth [data-lenis-prevent] {
    overscroll-behavior: contain;
  }
  .lenis.lenis-stopped {
    overflow: hidden;
  }
  .lenis.lenis-smooth iframe {
    pointer-events: none;
  }

  /* Smooth scroll behavior fallback */
  html {
    scroll-behavior: smooth;
  }
  
  /* Interactive cursor for clickable elements */
  [data-framer-name="Header / Burger menu"],
  [data-framer-name="MENU"],
  .servicesListRow,
  [data-framer-name="Question"],
  button,
  a {
    cursor: pointer !important;
  }

  /* Subtle card hover transitions */
  a[data-framer-name], .framer-1s0bcvz, .framer-140z0b6 {
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  /* FAQ Accordion Transitions */
  .faq-answer-wrap {
    transition: max-height 0.35s ease, opacity 0.3s ease, margin-top 0.3s ease;
    overflow: hidden;
  }

  /* Services detail image transition */
  .servicesListDetailSwap {
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
</style>
`;

  const customJs = `
<script src="${assetPrefix}js/lenis.min.js"></script>
<script src="${assetPrefix}js/interactions.js"></script>
`;

  html = html.replace('</head>', `${customCss}\n</head>`);
  html = html.replace('</body>', `${customJs}\n</body>`);

  return html;
}

// Process all files
for (const [srcFile, destRel] of Object.entries(routeMap)) {
  const fullSrc = path.join(srcDir, srcFile);
  if (!fs.existsSync(fullSrc)) continue;
  const fullDest = path.join(outDir, destRel);
  fs.mkdirSync(path.dirname(fullDest), { recursive: true });

  const raw = fs.readFileSync(fullSrc, 'utf8');
  const clean = processHtml(raw, destRel);
  fs.writeFileSync(fullDest, clean, 'utf8');
  console.log('Built:', destRel, 'size:', clean.length);
}
console.log('All pages built with clean runtime!');
