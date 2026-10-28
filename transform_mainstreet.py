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

# Master normalized copy dictionary: matches stripped/normalized text of ANY <p>, <h1>, <h2>, <h3>, <h4>
# regardless of inner <span> tags, letter-by-letter animations, &amp;, or curly quotes!
norm_copy_map = {
    # Brand & Header / Footer
    "Lyniq": "MAIN STREET",
    "LYNIQ®": "MAIN STREET®",
    "Digital design studio": "Building The Future",
    "(510) 895-6500": "(310) 982-6410",
    "hello@lyniqstudio.com": "info@empirecollectiveagency.com",
    "info@lyniqstudio.com": "info@empirecollectiveagency.com",
    "©19-26": "EST. 2024",
    "©19-24": "EST. 2024",
    "Digital": "MAIN",
    "Design Studio": "STREET",
    "UX/UI Design": "Experiential Marketing",
    "Development": "Customer Acquisition",
    "Brand Identity Design": "Brand Activations",
    "Ongoing Support": "Ground Intelligence",
    "We create digital designs that help brands move faster and convert better. Your business deserves more than just a website. It needs results.":
        "We transform audience attention into high-retention enterprise growth through immersive experiential marketing, disciplined field representation, and precision ground intelligence.",

    # Numbers Section
    "Our work speaks through numbers. Here's what we've achieved so far.":
        "Real human connections backed by undeniable ground data.",
    "Websites launched": "Retention Increase",
    "Helping brands make their mark online.": "Direct face-to-face connections build lasting brand loyalty.",
    "Users reached": "Consumers Engaged",
    "Our designs engage millions globally.": "Authentic in-person conversations across major metropolitan markets.",
    "Client satisfaction rate": "Client Retention Rate",
    "We build long-term partnerships through proven results.": "Long-term enterprise contracts driven by predictable ground ROI.",
    "Years of expertise": "Expansion Markets",
    "Decades of experience in delivering impactful digital solutions.": "Turnkey field specialist teams deployed with rapid agility nationwide.",

    # Description Section (Exact character length matched to prevent clipping!)
    "From ordinary": "From passive",
    "to extraordinary": "to iconic impact",
    "Design that's built to last and grow with your business.":
        "Real human connection that algorithms simply cannot replicate.",

    # Benefits Section (All 4 Cards + Mockup UI Elements!)
    "Your goals, our priority.": "Discipline Creates a Brighter Tomorrow.",
    "From concept to launch, we're committed to your success with rapid response times and personalized attention to detail.":
        "People, Ideas, Opportunity, Impact. We deploy disciplined field ambassadors to elevate your enterprise presence where it matters most.",
    "24/7 priority care": "Direct Empathy & Trust",
    "Receive priority treatment for urgent tasks, with an average response time of 24 hours for high-priority clients.":
        "Algorithms capture clicks; authentic human connection drives loyalty. We build personal relationships that convert skeptics into brand champions.",
    "Tailored tweaks for perfection": "Disciplined Field Execution",
    "Request custom revisions at any time. We provide up to 5 minor revisions post-launch to keep things looking fresh.":
        "Rigorous brand immersion and elite field representation ensuring your corporate vision is communicated with uncompromising precision.",
    "Post-Launch requests": "Field Execution Checklist",
    "Align text margins properly": "Territory demographic & foot-traffic mapping",
    "Increase mobile menu font size": "Ambassador brand immersion & certification",
    "Replace images": "Turnkey event & retail activation deployment",
    "Fix button color: #F9452D": "Live CRM lead capture & compliance audit",
    "Fix button color: #D4AF37": "Live CRM lead capture & compliance audit",
    "Speed up page loading": "Daily executive KPI & ROI reporting",
    "Valid for 3 months after launch": "Continuous SLA optimization & territory scale",
    "Download brand kit": "Live Territory Intelligence",
    "Brand kit at your fingertips": "Real-Time Ground Data",
    "Receive a full branding toolkit, from logos to color schemes and typography, download all assets or share them with your team.":
        "Live consumer feedback, competitive insights, and qualitative sentiment captured on-site to sharpen your market advantage in real time.",
    "Designer": "Territory Director",
    "Logo update complete, ready for your review!": "LA Metro activation hit 142% of daily target!",
    "Real-Time": "Turnkey",
    "Support": "Scale",

    # Work / Proven Impact Section (All 5 Projects!)
    "Selected work": "Proven Impact",
    "SELECTED WORK": "PROVEN IMPACT",
    "Proven results,": "High-impact activations,",
    "stunning designs": "measurable growth",
    "2K26": "2026",
    "2K24": "2026",
    "Radiant skincare branding": "Tier-1 Telecommunications Rollout",
    "Radiant skincare is offering a user-centric, ad-free platform.":
        "Accelerating direct customer acquisition across saturated urban markets, outperforming digital CPA by 38%.",
    "Timeless Impressions redesign": "Clean Energy & Solar Adoption",
    "Bold new look for an eco-conscious apparel brand.":
        "Direct community engagement driving 52% on-site qualification for residential sustainable energy programs.",
    "Apex clothing Co. rebrand": "National Retail & Venue Activation",
    "Stoyo branding": "Enterprise Consumer Expansion",
    "Visual identity and packaging design for a Stoyo brand.":
        "Multi-market ambassador fleet deployment generating 24,000+ verified consumer conversions across California.",
    "Vero app development": "FinTech Ecosystem Onboarding",
    "Vero aimed to distinguish itself in a competitive social media landscape.":
        "Experiential pop-up activations onboarding 15,000+ verified active enterprise accounts in 60 days.",
    "Branding": "Experiential",
    "Web design": "Field Sales",
    "All cases": "All Campaigns",

    # Services Section
    "Services": "Capabilities",
    "See pricing": "Explore Models",
    "Websites": "Market Intelligence",
    "Design support": "Territory Expansion",
    "We create impactful brand identities that differentiate your business and connect with your audience.":
        "We design immersive brand activations and experiential environments that forge emotional connections with your audience, making your brand unforgettable.",
    "From front-end interactions to back-end functionality, we deliver robust solutions that grow with your business.":
        "Face-to-face field strategies designed to convert customer interest into verified sales, reducing acquisition costs and maximizing ROI.",
    "We build custom websites that go beyond aesthetics, balancing design and functionality to captivate your audience and drive engagement.":
        "Real-time ground data collection and consumer sentiment analysis during live activations to refine your broader enterprise campaigns.",
    "We're here to help with everything from small updates to full-scale redesigns, tailored to your evolving needs.":
        "Turnkey operational deployment into new metropolitan regions, managing talent curation, compliance, logistics, and executive oversight.",

    # Quote Section (Including Split-Character Paragraph!)
    "Lyniq helps companies create stunning and strategically sound experiences that engage audiences. Our experts work closely with you to ensure that every detail is aligned with your goals.":
        "Main Street transforms passive market presence into dominant territory leadership. Our disciplined field directors and brand ambassadors represent your enterprise with unwavering excellence.",
    "From concept to launch, we craft digital solutions that not only look exceptional but also drive results, building connections that last":
        "From strategic territory mapping to high-velocity face-to-face execution, we build human connections that drive measurable, lasting revenue.",
    "Annie Bassett": "Executive Leadership",
    "Project manager and founder": "Main Street — Culver City, CA",

    # Team Section
    "Meet our team": "Leadership & Ground Force",
    "A diverse group of creators, strategists, and developers driven by a shared passion for crafting impactful digital experiences.":
        "An elite coalition of regional directors, experiential producers, and certified acquisition specialists committed to representing your brand with discipline.",
    "3": "12+",
    "Creative thinkers": "Regional Territory",
    "and strategists": "Directors & Strategists",
    "7": "45+",
    "Skilled developers with": "Campaign Producers &",
    "attention to detail": "Field Operations Leads",
    "9": "250+",
    "Experienced designers": "Certified Brand",
    "focused on user experience": "Ambassadors Nationwide",

    # Pricing / Engagement Section (Zero Dollar Amounts!)
    "Flexible pricing": "Strategic Engagement Architectures",
    "Choose the plan that best fits your needs.From a solid foundation to a fully optimized solution":
        "Bespoke campaign architectures designed around your growth targets, compliance standards, and geographic expansion goals.",
    "Choose the plan that best fits your needs.":
        "Bespoke campaign architectures designed around your growth targets and compliance standards.",
    "From a solid foundation to a fully optimized solution":
        "From initial regional pilot to nationwide enterprise market dominance.",
    "Monthly": "Regional Scope",
    "Annual": "Enterprise Retainer",
    "Save 30%": "Turnkey Fleet",
    "Basic": "Regional Pilot",
    "Pro": "Multi-Market Fleet",
    "Max": "National Sovereign",
    "Most popular": "Enterprise Standard",
    "$999": "Custom Scope",
    "$699": "Pilot Scope",
    "$2,999": "Custom Scope",
    "$2,499": "Enterprise SLA",
    "$2,099": "Enterprise SLA",
    "$4,999": "Bespoke Fleet",
    "$3,499": "Dedicated Fleet",
    "/month": "",
    "/quarter": "",
    "For small businesses or startups building their first digital presence.":
        "High-impact pilot activations in targeted metropolitan areas to validate ground market demand.",
    "For growing businesses needing more features and flexibility.":
        "Scaled multi-city customer acquisition fleets delivering consistent, high-volume verified contracts.",
    "For established brands looking for a fully tailored experience.":
        "Enterprise-wide sovereign territory dominance with dedicated full-time ground force and custom SLA.",
    "Choose this plan": "Schedule Strategy Call",
    "Competitor analysis": "Comprehensive territory & demographic mapping",
    "Design of homepage + up to 4 inner pages": "Dedicated field specialists & certified brand ambassadors",
    "Creation of custom page prototypes": "Turnkey on-site event & pop-up activation setup",
    "Basic analytics setup (e.g., Google Analytics)": "Daily ground KPI & consumer sentiment reporting",
    "Setup of a basic contact form": "Direct customer acquisition & verified opt-in onboarding",
    "Bug fixing and testing support": "Rigorous brand compliance & quality assurance",
    "Everything in the Basic Plan": "Everything in Regional Pilot",
    "Up to 10 pages, fully customized": "Simultaneous deployment across 3+ priority territories",
    "Social media integration": "Senior field management & executive territory directors",
    "Optimized mobile and tablet versions": "Advanced lead scoring, validation & instant CRM sync",
    "Enhanced SEO for core pages": "Accelerated direct-to-consumer conversion protocols",
    "Custom email template design for leads": "Dedicated account leadership & weekly SLA reviews",
    "Everything in the Professional Plan": "Everything in Multi-Market Fleet",
    "Custom blog design + setup": "Nationwide footprint rollout with rapid deployment capacity",
    "Monthly analytics + performance reporting": "Proprietary ground data intelligence & market share analytics",
    "E-commerce functionality (if needed)": "Full regulatory compliance & enterprise security protocols",
    "Unlimited revisions during the design phase": "Bespoke executive steering committee & guaranteed volume SLAs",
    "Priority support for 6 months post-launch": "Executive SLA review & direct territory leadership access",

    # Process Section (All 4 Steps Properly Distinct!)
    "Our process": "The Main Street Methodology",
    "Our four-step process keeps you informed and involved at every stage, ensuring the final result meets your goals and resonates with your audience.":
        "Our disciplined four-stage deployment framework transforms strategic territory goals into predictable, high-velocity customer acquisition.",
    "Schedule a consultation": "Schedule Strategy Call",
    "Discovery & Strategy": "Territory Intelligence & Mapping",
    "Choose the plan that best fits your needs. From a solid foundation to a fully optimized solution":
        "We analyze target demographics, commercial foot traffic, and competitive saturation to architect a high-conversion territory deployment plan.",
    "Design & Prototyping": "Ambassador Immersion & Certification",
    "Our designers bring your vision to life with wireframes and prototypes, focusing on an engaging user experience.":
        "Field specialists undergo rigorous training in your brand voice, compliance protocols, and consultative acquisition methodology.",
    "Development & Integration": "High-Velocity Field Activation",
    "Customer Acquisition & Integration": "High-Velocity Field Activation",
    "Choose the plan that best fits your needs. From a solid foundation to a fully optimized solution.":
        "Disciplined teams deploy into prime metropolitan venues and commercial corridors to engage consumers face-to-face and capture verified contracts.",
    "Launch & Support": "Live Telemetry & Territory Scale",
    "After testing and final approvals, we launch the site and provide ongoing support.":
        "Continuous daily KPI tracking, quality audits, and sentiment intelligence allow us to optimize conversion rates and scale across new regions.",

    # Testimonials Section (Including Split-Character Quotes!)
    "Successstories": "Partner Impact",
    "Success stories": "Partner Impact",
    "Our work speaks for itself, but our clients say it even better.":
        "Enterprise leaders trust Main Street to deliver high-retention customer acquisition at scale.",
    "They helped us shape our brand identity from scratch, giving us a website that perfectly reflects our values.":
        "Main Street deployed a disciplined field team across three metro markets in under three weeks, outperforming our internal acquisition targets by 42%.",
    "Sarah Morgan": "Marcus Vance",
    "Founder of a Tech Startup": "VP of National Growth, Enterprise Telecom",
    "We needed a full rebranding, and this agency delivered beyond our expectations. From the new logo to the website design, everything feels cohesive and professional.":
        "Their face-to-face ambassadors represent our brand with remarkable executive presence. Not only did customer volume surge, but 90-day retention reached an all-time high.",
    "Anna Karenina": "Elena Rostova",
    "Owner of a clothing E-commerce store": "Director of Retail Expansion, Solaris Energy",
    "Working with this team was a pleasure! Our sales increased by 30% in the first month. Thank you for the amazing job!":
        "Main Street's ground intelligence and direct onboarding activations generated over 15,000 verified accounts in 60 days with zero compliance friction.",
    "Andy Styles": "David Sterling",

    # FAQ Section (All 5 Real Questions & Answers!)
    "We've heard it all. Here's everything you need to know before working with us.":
        "Clear answers on how we structure, deploy, and scale high-impact field acquisition campaigns.",
    "Ask a question": "Inquire Directly",
    "What's your process for designing and developing a new website?":
        "How quickly can Main Street deploy a dedicated field team in our target market?",
    "I start by understanding your brand and goals, then create a tailored design that reflects your vision. Once the design is approved, I develop the site with clean, scalable code and ensure it's fully tested before launch.":
        "A regional pilot fleet is typically operational within 14 to 21 days. This includes demographic territory mapping, ambassador curation, brand immersion certification, and full compliance setup.",
    "What if I need to make changes or add features in the future?":
        "How do you ensure brand compliance and quality control during face-to-face interactions?",
    "I design with scalability in mind, making it easy to add new features as your business grows. I also offer ongoing support packages if you'd like me to handle updates for you.":
        "Every ambassador completes rigorous brand certification before deployment. Field directors conduct daily on-site audits, GPS territory verification, and real-time quality assurance checks.",
    "Do you offer SEO services?":
        "What industries benefit most from experiential marketing and direct acquisition?",
    "Yes, I incorporate SEO best practices into every website I build to help improve your search visibility from the start. For more advanced SEO strategies, I also offer customized SEO packages.":
        "We specialize in high-LTV sectors including Tier-1 Telecommunications, Clean Energy & Solar, FinTech, Enterprise SaaS, and Consumer Retail brands seeking rapid metropolitan scale.",
    "How long does it typically take to see results from my brand's new website?":
        "How is campaign ROI and field performance tracked and reported?",
    "Most clients start seeing results within a few months as search engines index the site and new visitors discover the brand. However, results can vary depending on factors like industry and marketing efforts.":
        "Partners receive live daily telemetry and weekly executive briefings detailing foot-traffic engagement, cost per acquisition (CPA), verified conversion rates, and consumer sentiment.",
    "How do you ensure the website is mobile-friendly?":
        "Can we start with a single metropolitan pilot before scaling nationwide?",
    "I use responsive design techniques and thoroughly test on various devices and screen sizes. This ensures your site looks great and works well for all users, no matter how they access it.":
        "Absolutely. Many enterprise partners initiate with a Regional Pilot in Los Angeles or a key California market to benchmark CPA and retention before expanding into a Multi-Market Fleet.",

    # Blog / Latest Insights Section
    "Latest Insights": "Field Intelligence",
    "Latest Insights.": "Field Intelligence.",
    "Explore industry news and creative strategies to keep your website ahead of the curve.":
        "Executive perspectives on experiential marketing, direct customer acquisition, and territory leadership.",
    "Explore industry news, expert advice, and creative strategies to keep your website ahead of the curve.":
        "Executive perspectives on experiential marketing, direct customer acquisition, and territory leadership.",
    "Check out more": "All Briefings",
    "Why your website's user experience is its greatest asset":
        "Why Direct Human Connection Outperforms Digital Ads in Saturated Markets",
    "Why Mobile-First Design is Crucial for Modern Websites":
        "The Anatomy of a High-Converting Experiential Brand Activation",
    "How to create a website that truly connects with your audience":
        "Scaling Face-to-Face Customer Acquisition Without Sacrificing Brand Equity",
    "Top Web Design Trends to Watch in 2024":
        "Ground Intelligence: Using Live Consumer Sentiment to Drive Enterprise Growth",
    "Building trust online: the importance of testimonials":
        "How Disciplined Field Representation Increases 12-Month Customer Retention",

    # Contact & Footer Section
    "Tell us what you're building.": "Initiate Your Territory Expansion.",
    "John is here to ensure your experience with us is smooth and successful. Reach out anytime — he's here to make sure you feel confident and supported throughout your journey with us.":
        "Our executive leadership team is ready to architect a bespoke field acquisition and experiential strategy tailored to your growth targets.",
    "John Taylor": "Managing Partner",
    "Client Success Manager": "Executive Strategy — Culver City, CA",
    "Member of the team": "Director of Field Operations",
    "Stay connected": "Initiate Your Expansion",
    "Join our newsletter and stay updated on the latest trends in digital design":
        "Connect with Main Street leadership in Culver City, CA to scale your customer acquisition.",
    "With Lyniq, your company gets more than just a website. We design experiences that resonate with your customers and drive meaningful engagement.":
        "© 2026 Main Street — Building The Future. Premier Experiential Marketing & Direct Customer Acquisition Agency. Culver City, CA.",

    # About Page & Subpages Specifics
    "Whether it's a new project or a quick question, we're here to connect.":
        "Connect with our Culver City headquarters to discuss regional pilots or national enterprise rollouts.",
    "123 Creative Lane, Washington, D.C., 20001":
        "Culver City, Los Angeles County, California",
    "We'd love to hear from you. Whether you're starting a new project, need help refining an idea, or just want to say hello, we're here to help.":
        "Whether you are launching a new metropolitan market, scaling direct acquisition, or planning a flagship brand activation, our leadership team is ready.",
    "Fill out the form below or reach out via email—we'll get back to you as soon as possible. Let's create something great together.":
        "Complete the executive inquiry form below or contact our Culver City office directly. Discipline creates a brighter tomorrow.",
    "We aimed to bring Vero's vision of authentic social interaction to life by focusing on seamless design and user privacy.":
        "We partner with ambitious enterprises to bridge the gap between brand vision and measurable ground-level market dominance.",
    "We don't believe in overcomplicating things, using the tools and strategies that make the most sense for your goals. If custom code is needed, we write it. If something works out of the box, we won't reinvent it.":
        "We believe in disciplined execution: putting elite, certified brand ambassadors directly in front of your ideal customers in high-value commercial corridors.",
    "We approach each project with the same questions: What does this need to do? Who will use it? How can we make it as simple and effective as possible?":
        "Every campaign is built on four pillars: People, Ideas, Opportunity, and Impact. We measure success strictly by verified conversions and long-term retention.",
    "We're a team of designers and developers who specialize in building websites that work. Our focus is on creating solutions that are clear, functional, and built to last.":
        "We are a premier coalition of field directors, experiential strategists, and acquisition specialists dedicated to building the future of direct brand engagement.",
    "We approach each project with the same questions: What does this need to do? Who will use it? How can we make it as simple and effective as possible? By understanding the answers, we build websites that aren't just visually appealing but also serve a purpose.":
        "By combining real-time demographic intelligence with authentic human empathy, we deliver customer acquisition volume and retention rates that digital channels alone cannot achieve.",
    "Lucas Johnson": "Alexander Vance",
    "Full Stack Developer": "Managing Director",
    "Sophia Reyes": "Victoria Sterling",
    "Creative Director": "VP of Experiential Strategy",
    "Ethan Clarke": "Marcus Thorne",
    "UX/UI Designer": "National Field Director",
    "Webby Awards Nominee": "Top Enterprise Acquisition Partner",
    "Recognized for excellence in web design and functionality.": "Recognized for industry-leading customer retention and field compliance.",
    "Awwwards Honorable Mention": "Excellence in Experiential Marketing",
    "Acknowledged for pushing creative boundaries in website development.": "Honored for high-impact metropolitan brand activations across California.",
    "CSS Design Awards Winner": "Fastest Growing Field Organization",
    "Celebrated for outstanding user experience and interface design.": "Celebrated for scaling turnkey ambassador fleets across 12+ metropolitan markets.",
    "First game after launching our biggest project": "Executive leadership summit in Los Angeles",
    "Copenhagen": "Culver City, CA",
    "We're not just a team; we're a group of individuals with diverse passions—from basketball games to team outings, we believe in building connections that extend beyond the office.":
        "Culture and discipline are the foundation of Main Street. We invest relentlessly in leadership development, mentorship, and executive growth.",
    "Every project we deliver is a reflection of our commitment to quality, designed to inspire and drive success.":
        "Every campaign we execute reflects our commitment to discipline, brand integrity, and measurable enterprise growth.",
    "Vero Labs Inc.": "Enterprise Partner",
    "This project reinforced the importance of building user-centered features that offer value beyond aesthetics, especially in social networking. The app's launch exceeded initial user growth targets, and the client received positive feedback on the app's intuitive design and ad-free experience.":
        "This deployment demonstrated the power of disciplined face-to-face engagement in saturated metropolitan markets. The campaign exceeded quarterly acquisition targets by 38% while maintaining a 98% compliance rating.",
    "Designing an ad-free experience meant creating engaging content flows without traditional ads. We achieved this by focusing on rich, visual content and user-driven discovery options.":
        "Penetrating high-density urban territories required precise demographic mapping and tailored value propositions delivered by certified field specialists.",
    "One challenge was ensuring privacy controls while maintaining an easy-to-use interface. Our team developed an accessible settings menu that lets users control visibility without overwhelming them.":
        "To ensure seamless onboarding and high 90-day retention, our team implemented real-time CRM verification and instant quality-control protocols on-site.",
}

def normalize_text(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"').replace('’', "'").replace('‘', "'")
    return ' '.join(s.split())

def replace_tag_contents(html):
    def replacer(match):
        tag = match.group(1)
        attrs = match.group(2)
        inner = match.group(3)
        # Do not touch if it contains nested block tags like <div or <p or <svg
        if re.search(r'<(?:div|p|h1|h2|h3|h4|svg|img|button|a)\b', inner, flags=re.I):
            return match.group(0)
        norm = normalize_text(inner)
        if norm == "Meet our team":
            new_text = "Leadership & Ground Force" if tag.lower() in ('h1', 'h2', 'h3') else "Meet Leadership"
            return f'<{tag}{attrs}>{new_text}</{tag}>'
        if norm in norm_copy_map:
            new_text = norm_copy_map[norm]
            return f'<{tag}{attrs}>{new_text}</{tag}>'
        return match.group(0)

    def span_replacer(match):
        attrs = match.group(1)
        inner = match.group(2)
        if re.search(r'<(?:div|p|h1|h2|h3|h4|svg|img|button|a)\b', inner, flags=re.I):
            return match.group(0)
        norm = normalize_text(inner)
        if norm in norm_copy_map:
            new_text = norm_copy_map[norm]
            return f'<span{attrs}>{new_text}</span>'
        return match.group(0)

    def leaf_div_replacer(match):
        attrs = match.group(1)
        inner = match.group(2)
        norm = normalize_text(inner)
        if norm in norm_copy_map:
            new_text = norm_copy_map[norm]
            return f'<div{attrs}>{new_text}</div>'
        return match.group(0)

    # Pass 1: Replace full <p>, <h1>-<h4>, <text>, <tspan> blocks (including those with nested <span> animations)
    html = re.sub(r'<(p|h1|h2|h3|h4|text|tspan)\b([^>]*)>([\s\S]*?)<\/\1>', replacer, html)
    # Pass 2: Replace leaf <span> blocks (e.g. inside multi-line <p><span>...</span><br><span>...</span></p>)
    html = re.sub(r'<span\b([^>]*)>((?:(?!<span)[\s\S])*?)<\/span>', span_replacer, html)
    # Pass 3: Replace leaf <div> blocks that contain only text (e.g. .servicesListDetailTitle & .servicesListDetailDescription)
    html = re.sub(r'<div\b([^>]*)>([^<>]+)<\/div>', leaf_div_replacer, html)
    # Pass 4: Final pass on <p>, <h1>-<h4>, <text>, <tspan>
    html = re.sub(r'<(p|h1|h2|h3|h4|text|tspan)\b([^>]*)>([\s\S]*?)<\/\1>', replacer, html)
    return html

def transform_html(html, dest_rel):
    depth = len(dest_rel.split('/')) - 1
    asset_prefix = './assets/' if depth == 0 else '../' * depth + 'assets/'

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

    # 4. Strict 3-Color Palette Transformation: Black (#000/#0c0c0c), White (#fff), and Gold (#D4AF37)
    html = re.sub(r'#f9452d\b', '#D4AF37', html, flags=re.I)
    html = re.sub(r'#f8442d[0-9a-fA-F]*', '#D4AF3740', html, flags=re.I)
    html = html.replace('rgb(249, 69, 45)', 'rgb(212, 175, 55)')
    html = html.replace('rgba(249, 69, 45', 'rgba(212, 175, 55')
    html = html.replace('--token-1662617d-fd18-4319-b3da-aa36e5415705:#f9452d', '--token-1662617d-fd18-4319-b3da-aa36e5415705:#D4AF37')
    html = html.replace('--token-06893589-c0f0-46a9-a272-d1bb23e77a6a:#c7ff97', '--token-06893589-c0f0-46a9-a272-d1bb23e77a6a:#D4AF37')
    html = html.replace('rgb(199, 255, 151)', 'rgb(212, 175, 55)')

    # 5. Apply Tag-Aware Normalized Copy Dictionary (runs twice to catch outer <p> after inner <span> if needed)
    html = replace_tag_contents(html)
    html = replace_tag_contents(html)

    # 6. Metadata, mailto & URL replacements
    html = re.sub(r'<title>.*?</title>', '<title>Main Street | Experiential Marketing & Direct Customer Acquisition</title>', html, flags=re.I)
    html = re.sub(r'content="Transform your brand with Lyniq.*?"', 'content="Main Street transforms audience attention into measurable enterprise growth through high-impact experiential marketing, disciplined field representation, and direct customer acquisition."', html, flags=re.I)
    html = re.sub(r'content="Lyniq Studio[^"]*"', 'content="Main Street | Building The Future"', html, flags=re.I)
    html = re.sub(r'https://lyniq\.framer\.website/?', 'https://lyniq.landingprofile.com/', html, flags=re.I)
    html = html.replace('mailto:hello@lyniqstudio.com', 'mailto:info@empirecollectiveagency.com')
    html = html.replace('hello@lyniqstudio.com', 'info@empirecollectiveagency.com')
    html = html.replace('(510) 895-6500', '(310) 982-6410')

    # 7. Fix Hero & Footer Giant SVG ViewBoxes so MAIN and STREET have identical monumental scale & zero clipping!
    # Top word 'MAIN' (4 chars at 427px = ~1060px wide)
    html = html.replace('viewBox="0 0 1177.62 342"', 'viewBox="0 0 1060 342"')
    html = html.replace('viewBox="0 0 1177.62 427"', 'viewBox="0 0 1060 427"')
    # Bottom word 'STREET' (6 chars at 427px = ~1480px wide; was 2595.62 for 13-char 'Design Studio'!)
    html = html.replace('viewBox="0 0 2595.62 342"', 'viewBox="0 0 1480 342"')
    html = html.replace('viewBox="0 0 2595.62 512"', 'viewBox="0 0 1480 512"')

    # 8. Replace Header Logo with sleek horizontal lockup (3D Emblem + MAIN STREET - BUILDING THE FUTURE)
    logo_header_tag = f'<img src="{asset_prefix}images/mainstreet-logo-header.png" alt="Main Street - Building The Future" style="height:42px;width:auto;object-fit:contain;vertical-align:middle;filter:drop-shadow(0 2px 8px rgba(0,0,0,0.65));">'
    html = re.sub(r'<div class="framer-2b7bfw"[\s\S]*?<\/div>\s*<div class="framer-1xb848l"[\s\S]*?<\/div>',
                  f'<div style="display:flex;align-items:center;height:100%">{logo_header_tag}</div>', html)

    # 9. Replace Footer Logo with large, unmutilated 3D Black & Gold vertical lockup on light footer background
    # Also hide the floating ® next to the footer SVG logo so it doesn't collide
    footer_logo_tag = f'<img src="{asset_prefix}images/mainstreet-logo.png" alt="Main Street - Building The Future" style="max-height:115px;width:auto;object-fit:contain;">'
    html = re.sub(r'<svg class="framer-1b5i8re" data-framer-name="(?:Main Street|Lyniq)"[\s\S]*?<\/svg>',
                  f'<div style="display:flex;align-items:center;height:100%">{footer_logo_tag}</div>', html)

    # Replace favicon
    html = re.sub(r'<link href="[^"]*images/0qZrfBuw0vpXfqa4iQEyDlGqjU\.png"[^>]*>',
                  f'<link href="{asset_prefix}images/favicon.png" rel="icon" type="image/png">', html)

    # 10. Custom CSS and scripts injection
    custom_css = f'''
<style id="mainstreet-custom-theme">
  :root {{
    --mainstreet-gold: #D4AF37;
    --mainstreet-gold-light: #F3D080;
    --mainstreet-gold-dark: #9E7D3B;
    --mainstreet-black: #0c0c0c;
    --mainstreet-white: #ffffff;
  }}

  /* Hide badges, template credit links & overlay artifacts */
  #__framer-badge-container,
  .framer-143iyx0-container,
  .framer-bv12sz-container,
  a[href*="templifica"],
  .framer-PdQjD,
  .framer-10503k5,
  .framer-1g8b04k,
  #template-overlay {{
    display: none !important;
  }}

  /* Hide redundant floating ® next to the 3D Footer Logo */
  .framer-1fb641m,
  .framer-18koodg {{
    display: none !important;
  }}

  /* Top Header subtle luxury dark gradient backdrop so white nav links & gold logo are 100% legible */
  header.framer-1g7y59t {{
    background: linear-gradient(180deg, rgba(12,12,12,0.88) 0%, rgba(12,12,12,0.42) 65%, rgba(12,12,12,0) 100%) !important;
    padding-top: 10px !important;
    padding-bottom: 14px !important;
  }}

  /* Fix nav link hover clone overlap */
  .framer-76oe1d {{
    overflow: hidden !important;
    height: 22px !important;
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

  /* Prevent descender clipping on large headings & email links */
  [data-framer-component-type="RichTextContainer"] {{
    overflow: visible !important;
  }}
  .framer-124p92x, .framer-12hhivf {{
    width: auto !important;
    max-width: none !important;
    overflow: visible !important;
  }}
  .framer-124p92x p, .framer-12hhivf p, .framer-124p92x a, .framer-12hhivf a {{
    white-space: nowrap !important;
    font-size: 20px !important;
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

  .framer-0LXDG {{
    width: auto !important;
    min-width: 145px !important;
    padding: 0 24px !important;
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
    opacity: 1 !important;
    background-color: #ffffff !important;
    box-shadow: 0 -25px 50px rgba(0,0,0,0.12);
  }}
  section:not([data-framer-name="Hero"]),
  footer {{
    position: relative !important;
    z-index: 3 !important;
    opacity: 1 !important;
  }}
  section[data-framer-name="Quote"] {{
    background-color: #f4f4f4 !important;
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
