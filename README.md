# MAIN STREET — Building The Future

Official institutional website for **Main Street** — Experiential Marketing, Brand Activations, Direct Customer Acquisition & Ground Intelligence (Culver City, CA).

## 🚀 Features

- **Bespoke Black, White & Gold Identity**: Custom 3D metallic logo lockups, color-graded photography, and luxury typography.
- **Zero External Dependencies**: 100% self-contained static HTML/CSS/JS with all images, vector graphics, and `.woff2` fonts served locally from `/assets`.
- **Interactive Engine**: Vanilla JavaScript + GSAP ScrollTrigger + Lenis smooth scrolling powering capability tabs, consultative engagement architectures, animated counters, and FAQ accordions.
- **Production Ready**: Configured with `.htaccess` for Apache/LiteSpeed web servers on Hostinger.

## 📁 Project Structure

```
├── .htaccess                  # Apache / LiteSpeed rewrite and caching rules
├── assets/
│   ├── fonts/                 # Localized web fonts (.woff2)
│   ├── images/                # 3D logos & Black/White/Gold graded media
│   └── js/                    # Lenis, GSAP & native interactions engine
├── index.html                 # Homepage
├── about.html                 # About page
├── projects.html              # Proven Impact / Campaigns catalog
├── projects/                  # Campaign case studies
├── blog.html                  # Field Intelligence catalog
├── blog/                      # Executive briefings & articles
├── contact.html               # Executive inquiry page
├── terms.html                 # Terms of service
├── privacy.html               # Privacy policy
├── transform_mainstreet.py    # Automated build & copy transformation script
└── server.js                  # Local development server
```

## 🛠 Local Development

Start local preview server:
```bash
node server.js
```
Open `http://localhost:3005` in your browser.
