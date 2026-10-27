# Lyniq Studio — Clean Clone & Production Deployment

Modern, high-performance static clone of [Lyniq Studio](https://lyniq.framer.website/).

## 🚀 Features

- **Decoupled Runtime**: 100% decoupled from Framer cloud dependencies, tracking scripts, and hydration traps.
- **Localized Assets**: All 65 images and 89 typography font files served locally from `/assets`.
- **Smooth Interactions**: Native vanilla JavaScript engine powering interactive service tabs, pricing switches, FAQ accordions, burger menus, and forms.
- **Lenis Smooth Scrolling**: Inertial smooth scrolling integrated via Lenis.
- **Production Ready**: Clean `.htaccess` configured for Apache/LiteSpeed web servers with caching, compression, and clean URLs.

## 📁 Project Structure

```
├── .htaccess             # Apache / LiteSpeed rewrite and caching rules
├── assets/
│   ├── fonts/            # Localized web fonts (.woff2)
│   ├── images/           # Localized images and media
│   └── js/               # Lenis & native interactions engine
├── index.html            # Homepage
├── about.html            # About page
├── projects.html         # Projects catalog
├── projects/             # Case studies
├── blog.html             # Blog catalog
├── blog/                 # Blog articles
├── contact.html          # Contact page
├── terms.html            # Terms of service
├── privacy.html          # Privacy policy
└── server.js             # Local development server
```

## 🛠 Local Development

Start local preview server:
```bash
node server.js
```
Open `http://localhost:3005` in your browser.
