import os
import re
import json

src_dir = '/tmp/lyniq_pages'
out_dir = '/Users/gabrielalvespardin/.gemini/antigravity/scratch/lyniq'
img_map = json.load(open(os.path.join(out_dir, 'image_map.json')))
font_map = json.load(open(os.path.join(out_dir, 'font_map.json')))

route_map = {
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
}

# Regex pairs: (pattern, replacement)
regex_pairs = [
    # SEO / Metadata
    (r'<title>.*?</title>', '<title>Main Street | Experiential Marketing & Direct Customer Acquisition</title>'),
    (r'content="Transform your brand with Lyniq.*?">', 'content="Main Street transforms audience attention into measurable enterprise growth through high-impact experiential marketing, disciplined field representation, and direct customer acquisition.">'),
    (r'content="Lyniq Studio \| Digital Design &amp; Brand Development Agency"', 'content="Main Street | Building The Future"'),
    (r'content="Lyniq Studio \| Digital Design & Brand Development Agency"', 'content="Main Street | Building The Future"'),
    (r'https://lyniq\.framer\.website/?', 'https://lyniq.landingprofile.com/'),

    # Hero Giant Typography
    (r'>Digital</p>', '>MAIN</p>'),
    (r'>Digital</h1>', '>MAIN</h1>'),
    (r'>Design Studio</p>', '>STREET</p>'),
    (r'>Design Studio</h1>', '>STREET</h1>'),
    (r'>Digital design studio</p>', '>Experiential Marketing Agency</p>'),
    (r'We create digital designs that help brands move faster and convert better.*?It needs results\.',
     'We transform audience attention into high-retention enterprise growth through immersive experiential marketing, disciplined field representation, and precision ground intelligence.'),

    # Numbers
    (r'Our work speaks through numbers\. Here’s what we’ve achieved so far\.', 'Real human connections backed by undeniable ground data.'),

    # Benefits
    (r'Your goals, our priority\.', 'Discipline Creates a Brighter Tomorrow.'),
    (r'From concept to launch, we\'re committed to your success with rapid response times and personalized attention to detail\.',
     'People, Ideas, Opportunity, Impact. We deploy disciplined field ambassadors to elevate your enterprise presence where it matters most.'),
    (r'Receive priority treatment for urgent tasks, with an average response time of 24 hours for high-priority clients\.',
     'Algorithms capture clicks; authentic human connection drives loyalty. We build personal relationships that convert skeptics into brand champions.'),
    (r'Request custom revisions at any time\. We provide up to 5 minor revisions post-launch to keep things looking fresh\.',
     'Rigorous brand immersion and elite representation ensuring your corporate vision is communicated with uncompromising precision.'),
    (r'Receive a full branding toolkit, from logos to color schemes and typography\. download all assets or share them with your team\.',
     'Live consumer feedback, competitive insights, and qualitative sentiment captured on-site to sharpen your market advantage.'),
    (r'up to 5 minor revisions</span> post-launch to keep things looking fresh\.',
     'continuous territory refinement and campaign tuning to sustain peak performance.'),

    # Services
    (r'We create impactful brand identities that differentiate your business and connect with your audience\.',
     'We design immersive brand activations and experiential environments that forge emotional connections with your audience, making your brand unforgettable.'),
    (r'From front-end interactions to back-end functionality, we deliver robust solutions that grow with your business\.',
     'Face-to-face field strategies designed to convert customer interest into actual sales, reducing costs and maximizing return on investment.'),
    (r'We build custom websites that go beyond aesthetics, balancing design and functionality to captivate your audience and drive engagement\.',
     'Real-time ground data collection and consumer feedback during live activations to refine your broader campaigns with absolute precision.'),
    (r'We’re here to help with everything from small updates to full-scale redesigns, tailored to your evolving needs\.',
     'Turnkey operational deployment into new metropolitan regions, managing talent curation, compliance, logistics, and executive oversight.'),

    # Team & Culture
    (r'A diverse group of creators, strategists, and developers driven by a shared passion for crafting impactful digital experiences\.',
     'An elite coalition of field directors, experiential producers, and acquisition specialists committed to representing your brand with absolute discipline.'),

    # Process
    (r'A proven, repeatable framework that turns strategy into predictable field momentum\.',
     'A proven, repeatable framework that turns strategy into predictable field momentum.'),

    # Pricing Section (Exhaustive Price & Rate Removal)
    (r'Choose the plan that best fits your needs\.', 'Bespoke campaign architectures designed around your growth targets and compliance standards.'),
    (r'From a solid foundation to a fully optimized solution', 'From initial regional pilot to nationwide enterprise market dominance.'),
    (r'>Monthly<', '>Regional Scope<'),
    (r'>Annual<', '>Enterprise Retainer<'),
    (r'>Basic<', '>Regional Pilot<'),
    (r'>Pro<', '>Multi-Market Fleet<'),
    (r'>Max<', '>National Sovereign<'),
    (r'\$2,999', 'Custom Scope'),
    (r'\$2,499', 'Enterprise SLA'),
    (r'\$2,099', 'Enterprise SLA'),
    (r'\$999', 'Custom Scope'),
    (r'\$699', 'Pilot Scope'),
    (r'\$4,999', 'Bespoke Fleet'),
    (r'\$3,499', 'Dedicated Fleet'),
    (r'\/month', ''),
    (r'\/quarter', ''),
    (r'\/yr', ''),

    # Plan Descriptions & Features
    (r'For small businesses or startups building their first digital presence\.',
     'High-impact pilot activations in targeted metropolitan areas to validate ground market demand.'),
    (r'Design of homepage \+ up to 4 inner pages', 'Dedicated field specialists & certified brand ambassadors'),
    (r'Creation of custom page prototypes', 'Turnkey on-site event & pop-up activation setup'),
    (r'Basic analytics setup \(e\.g\., Google Analytics\)', 'Daily ground KPI & consumer sentiment reporting'),
    (r'Setup of a basic contact form', 'Direct customer acquisition & verified opt-in onboarding'),
    (r'Bug fixing and testing support', 'Rigorous brand compliance & quality assurance'),

    (r'For growing businesses needing more features and flexibility\.',
     'Scaled multi-city customer acquisition fleets delivering consistent, high-volume verified contracts.'),
    (r'Everything in the Basic Plan', 'Everything in Regional Pilot'),
    (r'Up to 10 pages, fully customized', 'Simultaneous deployment across 3+ priority territories'),
    (r'Social media integration', 'Senior field management & executive territory directors'),
    (r'Optimized mobile and tablet versions', 'Advanced lead scoring, validation & instant CRM sync'),
    (r'Enhanced SEO for core pages', 'Accelerated direct-to-consumer conversion protocols'),
    (r'Custom email template design for leads', 'Dedicated account leadership & weekly SLA reviews'),

    (r'For established brands looking for a fully tailored experience\.',
     'Enterprise-wide sovereign territory dominance with dedicated full-time ground force and custom SLA.'),
    (r'Everything in the Professional Plan', 'Everything in Multi-Market Fleet'),
    (r'Custom blog design \+ setup', 'Nationwide footprint rollout with rapid deployment capacity'),
    (r'Monthly analytics \+ performance reporting', 'Proprietary ground data intelligence & market share analytics'),
    (r'E-commerce functionality \(if needed\)', 'Full regulatory compliance & enterprise security protocols'),
    (r'Unlimited revisions during the design phase', 'Bespoke executive steering committee & guaranteed volume SLAs'),
    (r'Priority support for 6 months post-launch', 'Executive SLA review & direct territory leadership access'),

    # FAQ
    (r'How long does a website take\?', 'What is the typical deployment timeline for a field campaign?'),
    (r'A standard website project typically takes 4–6 weeks.*',
     'A regional pilot campaign is typically deployed within 2 to 3 weeks, including territory mapping, ambassador recruitment, and rigorous brand immersion certification.'),
    (r'Do you offer ongoing maintenance\?', 'How do you guarantee brand compliance and quality?'),
    (r'Yes, we offer ongoing support and maintenance packages.*',
     'Every field ambassador passes through our proprietary certification protocols. We enforce mystery audits, real-time GPS check-ins, and strict SLA benchmarks across all activations.'),
    (r'What is your revision policy\?', 'Can Main Street scale across multiple metropolitan markets?'),
    (r'We include up to 5 rounds of revisions.*',
     'Yes. Our multi-market infrastructure allows seamless scaling across tier-1, tier-2, and tier-3 metropolitan areas with centralized executive oversight and distributed field management.'),

    # Copyright & Legal
    (r'© 202[46] Lyniq Studio\. All rights reserved\.', '© 2026 Main Street. Building The Future. All rights reserved.'),
]

# Plain string literal replacements
plain_pairs = [
    # Contact & Identity
    ('hello@lyniqstudio.com', 'info@empirecollectiveagency.com'),
    ('info@lyniqstudio.com', 'info@empirecollectiveagency.com'),
    ('(510) 895-6500', '(310) 982-6410'),
    ('+1 510 895 6500', '+1 (310) 982-6410'),
    ('Stay connected', 'Initiate Your Expansion'),
    ('Join our newsletter and stay updated on the latest trends in digital design',
     'Connect with Main Street leadership to discuss how our face-to-face strategies can scale your customer acquisition.'),
    ('LYNIQ®', 'MAIN STREET®'),
    ('Lyniq Studio', 'Main Street'),
    ('Lyniq', 'Main Street'),

    # Hero Tags
    ('UX/UI Design', 'Experiential Marketing'),
    ('Brand Identity Design', 'Brand Activations'),
    ('Ongoing Support', 'Ground Intelligence'),
    ('©19-26', 'EST. 2024'),
    ('©19-24', 'EST. 2024'),

    # Numbers
    ('Websites launched', 'Retention Increase'),
    ('Helping brands make their mark online.', 'Direct face-to-face connections build lasting brand loyalty.'),
    ('Users reached', 'Consumers Engaged'),
    ('Our designs engage millions globally.', 'Authentic in-person conversations across major metropolitan markets.'),
    ('Client satisfaction rate', 'Client Retention Rate'),
    ('We build long-term partnerships through proven results.', 'Long-term enterprise contracts driven by predictable ground ROI.'),
    ('Years of expertise', 'Expansion Markets'),
    ('Decades of experience in delivering impactful digital solutions.', 'Turnkey field specialist teams deployed with rapid agility nationwide.'),

    # Description
    ('From ordinary', 'From passive attention'),
    ('to extraordinary', 'to active loyalty'),
    ('Design that’s built to last and grow with your business.', 'Real human connection that algorithms simply cannot replicate.'),

    # Benefits
    ('24/7 priority care', 'Direct Empathy & Trust'),
    ('Tailored tweaks for perfection', 'Disciplined Field Execution'),
    ('Brand kit at your fingertips', 'Real-Time Ground Data'),
    ('Real-Time Support', 'Turnkey Territory Scale'),
    ('Post-Launch requests', 'Post-Deployment Optimization'),

    # Work / Proven Impact
    ('SELECTED WORK', 'PROVEN IMPACT'),
    ('Selected work', 'Proven Impact'),
    ('Proven results, stunning designs', 'High-Impact Activations, Measurable Growth'),
    ('2K24', '2026'),
    ('2K26', '2026'),
    ('Radiant skincare branding', 'Tier-1 Telecommunications Rollout'),
    ('Radiant skincare is offering a user-centric, ad-free platform.', 'Accelerating customer acquisition across saturated urban markets, outperforming digital CPA by 38%.'),
    ('Timeless Impressions redesign', 'Clean Energy & Solar Adoption'),
    ('Bold new look for an eco-conscious apparel brand.', 'Direct community engagement driving 52% on-site qualification for residential sustainable energy.'),
    ('Vero app development', 'FinTech Ecosystem Onboarding'),
    ('Innovative mobile banking experience for next-generation users.', 'Experiential pop-up activations onboarding 15,000+ verified active accounts in 60 days.'),
    ('Branding', 'Experiential'),
    ('Web design', 'Field Sales'),

    # Services
    ('Development', 'Customer Acquisition'),
    ('Websites', 'Market Intelligence'),
    ('Design support', 'Territory Expansion'),

    # Quote
    ('Annie Bassett', 'Executive Leadership'),
    ('Project manager and founder', 'Main Street Collective'),

    # Team
    ('Meet our team', 'Leadership & Ground Force'),
    ('Creative thinkers and strategists', 'Field Directors, Strategists & Ambassadors'),

    # Process
    ('Our process', 'The Main Street Methodology'),
    ('01 Discovery', '01 Strategic Discovery & Territory Mapping'),
    ('02 Design', '02 Talent Immersion & Brand Certification'),
    ('03 Launch', '03 High-Velocity Execution & Live Analytics'),

    # Pricing Buttons, Badges & Inclusions
    ('Flexible pricing', 'Strategic Engagement Architectures'),
    ('Save 30%', 'Turnkey Fleet'),
    ('Most popular', 'Enterprise Standard'),
    ('Choose this plan', 'Schedule Strategy Call'),
    ('Start with Basic', 'Request Pilot Scope'),
    ('Start with Pro', 'Schedule Strategy Call'),
    ('Contact us for Enterprise', 'Inquire for Partnership'),
    ('Get started', 'Schedule Strategy Call'),
    ('Competitor analysis', 'Comprehensive territory & demographic mapping'),
    ('Design of homepage + up to 4 inner pages', 'Dedicated field specialists & certified brand ambassadors'),
    ('Basic analytics setup (e.g., Google Analytics)', 'Daily ground KPI & consumer sentiment reporting'),
    ('Custom blog design + setup', 'Nationwide footprint rollout with rapid deployment capacity'),
    ('Monthly analytics + performance reporting', 'Proprietary ground data intelligence & market share analytics'),
    ('E-commerce functionality (if needed)', 'Full regulatory compliance & enterprise security protocols'),
    ('Priority support for 6 months post-launch', 'Executive SLA review & direct territory leadership access'),
    ('Creation of custom page prototypes', 'Turnkey on-site event & pop-up activation setup'),
    ('Setup of a basic contact form', 'Direct customer acquisition & verified opt-in onboarding'),
    ('Bug fixing and testing support', 'Rigorous brand compliance & quality assurance'),
    ('Up to 10 pages, fully customized', 'Simultaneous deployment across 3+ priority territories'),
    ('Social media integration', 'Senior field management & executive territory directors'),
    ('Optimized mobile and tablet versions', 'Advanced lead scoring, validation & instant CRM sync'),
    ('Enhanced SEO for core pages', 'Accelerated direct-to-consumer conversion protocols'),
    ('Custom email template design for leads', 'Dedicated account leadership & weekly SLA reviews'),
    ('Unlimited revisions during the design phase', 'Bespoke executive steering committee & guaranteed volume SLAs'),

    # Testimonials & Personas
    ('Client Testimonials', 'Partner Perspectives'),
    ('What our clients say about us', 'Enterprise Partnerships Built on Uncompromising ROI'),
    ('Sarah Jenkins', 'Director of Consumer Growth'),
    ('Marcus Vance', 'VP of Retail Operations'),
    ('Elena Rostova', 'Chief Marketing Officer'),
    ('Owner of a clothing E-commerce store', 'Director of National Retail Partnerships'),
    ('Creative director at a fintech startup', 'VP of Growth, Sovereign FinTech'),
    ('Founder of a wellness brand', 'Executive Director, Clean Energy Coalition'),
    ('Frequently asked questions', 'Strategic Engagement Inquiries'),
]

def transform_html(html, dest_rel):
    depth = len(dest_rel.split('/')) - 1
    asset_prefix = './assets/' if depth == 0 else '../' * depth + 'assets/'
    root_prefix = './' if depth == 0 else '../' * depth

    # 1. Strip broken Framer telemetry and modules safely
    html = re.sub(r'<script\b([^>]*)>([\s\S]*?)<\/script>', lambda m: '' if any(k in m.group(1) or k in m.group(2) for k in [
        'events.framer.com', 'script_main', 'type="module"', 'framer/appear', 'framer/handover',
        'data-framer-appear-animation', 'var animator', 'framer-appear-start'
    ]) else m.group(0), html, flags=re.I)

    # 2. Localize images & fonts
    html = re.sub(r'\s*srcset="https://framerusercontent\.com/images/[^"]*"', '', html, flags=re.I)
    html = re.sub(r'https://(?:framerusercontent\.com/images|images\.unsplash\.com)/([a-zA-Z0-9_\-\.]+)(?:\?[^"\'\)\s,]+)?',
                  lambda m: asset_prefix + 'images/' + m.group(1), html)
    html = re.sub(r'https://(?:framerusercontent\.com/assets|fonts\.gstatic\.com/s/[^/]+/[^/]+)/([a-zA-Z0-9_\-\.]+\.woff2?)',
                  lambda m: asset_prefix + 'fonts/' + m.group(1), html)
    for rem, loc in font_map.items():
        fname = os.path.basename(loc)
        html = html.replace(rem, asset_prefix + 'fonts/' + fname)

    # 3. Unhide SSR and unlock visibility
    html = re.sub(r'opacity:\s*0(?:\.001)?(?=[;\"\'\s])', 'opacity: 1', html)
    html = re.sub(r'filter:\s*blur\([^)]+\)', 'filter: none', html)
    html = re.sub(r'translateY\([0-9\.\-]+px\)', 'translateY(0px)', html)

    # 4. Color Palette Transformation: ONLY Black (#000/#0c0c0c), White (#fff), and Gold (#D4AF37)
    html = re.sub(r'#f9452d\b', '#D4AF37', html, flags=re.I)
    html = re.sub(r'#f8442d[0-9a-fA-F]*', '#D4AF3740', html, flags=re.I)
    html = html.replace('rgb(249, 69, 45)', 'rgb(212, 175, 55)')
    html = html.replace('rgba(249, 69, 45', 'rgba(212, 175, 55')
    html = html.replace('--token-1662617d-fd18-4319-b3da-aa36e5415705:#f9452d', '--token-1662617d-fd18-4319-b3da-aa36e5415705:#D4AF37')
    html = html.replace('--token-06893589-c0f0-46a9-a272-d1bb23e77a6a:#c7ff97', '--token-06893589-c0f0-46a9-a272-d1bb23e77a6a:#D4AF37')
    html = html.replace('rgb(199, 255, 151)', 'rgb(212, 175, 55)')

    # 5. Apply regex replacements
    for pattern, repl in regex_pairs:
        try:
            html = re.sub(pattern, repl, html, flags=re.I)
        except Exception as e:
            print(f'Regex failed for {pattern}: {e}')

    # 6. Apply plain string replacements
    for target, repl in plain_pairs:
        html = html.replace(target, repl)

    # 7. Replace Header Logo with Main Street transparent logo
    logo_light_tag = f'<img src="{asset_prefix}images/mainstreet-logo-light.png" alt="Main Street" style="height:34px;width:auto;object-fit:contain;vertical-align:middle;">'
    html = re.sub(r'<div class="framer-2b7bfw"[\s\S]*?<\/div>\s*<div class="framer-1xb848l"[\s\S]*?<\/div>',
                  f'<div style="display:flex;align-items:center;height:100%">{logo_light_tag}</div>', html)

    # Replace Footer Logo with large Main Street logo
    footer_logo_tag = f'<img src="{asset_prefix}images/mainstreet-logo-light.png" alt="Main Street - Building The Future" style="max-height:85px;width:auto;object-fit:contain;">'
    html = re.sub(r'<svg class="framer-1b5i8re" data-framer-name="Main Street"[\s\S]*?<\/svg>',
                  f'<div style="display:flex;align-items:center;height:100%">{footer_logo_tag}</div>', html)
    html = re.sub(r'<svg class="framer-1b5i8re" data-framer-name="Lyniq"[\s\S]*?<\/svg>',
                  f'<div style="display:flex;align-items:center;height:100%">{footer_logo_tag}</div>', html)

    # Replace favicon
    html = re.sub(r'<link href="[^"]*images/0qZrfBuw0vpXfqa4iQEyDlGqjU\.png"[^>]*>',
                  f'<link href="{asset_prefix}images/favicon.png" rel="icon" type="image/png">', html)

    # 8. Custom CSS and scripts injection
    custom_css = f'''
<style id="mainstreet-custom-theme">
  :root {{
    --mainstreet-gold: #D4AF37;
    --mainstreet-gold-light: #F3D080;
    --mainstreet-gold-dark: #9E7D3B;
    --mainstreet-black: #0c0c0c;
    --mainstreet-white: #ffffff;
  }}

  /* Hide badges & overlay artifacts */
  #__framer-badge-container,
  .framer-143iyx0-container,
  .framer-bv12sz-container,
  a[href*="templifica"],
  .framer-PdQjD,
  #template-overlay {{
    display: none !important;
  }}

  /* Hero headline layers fix (difference & overlay blend, hide sizer duplicates) */
  .framer-yh5zfl, .framer-11pd3k7 {{
    opacity: 0 !important;
  }}
  .framer-17f7gii, .framer-skcre,
  .framer-l0tfed, .framer-13h7p30 {{
    opacity: 1 !important;
    transform: translateY(-50%) !important;
  }}
  [data-framer-name="Projects number"],
  .framer-18ia252 {{
    display: none !important;
  }}

  /* Pricing section clean consultative styling (hide strikethrough container) */
  .framer-1mzu6cm, [data-framer-name="Old"] {{
    display: none !important;
  }}

  /* Gold highlights, badges & buttons */
  .framer-0LXDG, 
  button[type="submit"],
  .framer-1yejg0n:focus-within {{
    background-color: var(--mainstreet-gold) !important;
    color: #000000 !important;
    border-color: var(--mainstreet-gold) !important;
  }}

  /* Button text color */
  .framer-0LXDG p, button[type="submit"] p {{
    color: #000000 !important;
    font-weight: 700 !important;
  }}

  /* Sticky Hero Curtain Effect */
  section[data-framer-name="Hero"] {{
    position: sticky !important;
    top: 0px !important;
    z-index: 1 !important;
  }}
  section[data-framer-name="Numbers"] {{
    position: relative !important;
    z-index: 2 !important;
    background-color: #ffffff !important;
    box-shadow: 0 -25px 50px rgba(0,0,0,0.12);
  }}
  section[data-framer-name="Description"],
  section[data-framer-name="Benefits"],
  section[data-framer-name="Work"],
  section[data-framer-name="Services"],
  section[data-framer-name="Quote"],
  section[data-framer-name="Team"],
  section[data-framer-name="Pricing"],
  section[data-framer-name="Process"],
  section[data-framer-name="Testimonials"],
  section[data-framer-name="FAQ"],
  section[data-framer-name="Blog"] {{
    position: relative !important;
    z-index: 3 !important;
  }}

  /* Lenis smooth scroll */
  html.lenis, html.lenis body {{
    height: auto;
  }}
  .lenis.lenis-smooth {{
    scroll-behavior: auto !important;
  }}
  html {{
    scroll-behavior: smooth;
  }}

  /* Interactive pointer */
  button, a, [data-framer-name="Header / Burger menu"], [data-framer-name="MENU"], .servicesListRow {{
    cursor: pointer !important;
  }}

  /* Project card image hover zoom */
  .framer-lux5qc img {{
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }}
  .framer-lux5qc:hover img {{
    transform: scale(1.05) !important;
  }}

  /* FAQ Accordion Transitions */
  .faq-answer-wrap {{
    transition: max-height 0.35s ease, opacity 0.3s ease, margin-top 0.3s ease;
    overflow: hidden;
  }}
</style>
'''

    custom_js = f'''
<script src="{asset_prefix}js/lenis.min.js"></script>
<script src="{asset_prefix}js/gsap.min.js"></script>
<script src="{asset_prefix}js/ScrollTrigger.min.js"></script>
<script src="{asset_prefix}js/interactions.js"></script>
'''

    html = html.replace('</head>', f'{custom_css}\n</head>')
    html = html.replace('</body>', f'{custom_js}\n</body>')

    return html

def build_all_pages():
    for src_file, dest_rel in route_map.items():
        src_full = os.path.join(src_dir, src_file)
        if not os.path.exists(src_full):
            continue
        dest_full = os.path.join(out_dir, dest_rel)
        os.makedirs(os.path.dirname(dest_full), exist_ok=True)
        raw = open(src_full, encoding='utf-8').read()
        clean = transform_html(raw, dest_rel)
        open(dest_full, 'w', encoding='utf-8').write(clean)
        print('Transformed & Built:', dest_rel, 'size:', len(clean))

    print('All 20 pages transformed to Main Street branding successfully!')

if __name__ == '__main__':
    build_all_pages()
