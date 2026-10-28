# MAIN STREET — Experiential Marketing Agency (Los Angeles)

Static site (HTML/CSS/JS) for https://mainstreet.landingprofile.com — Apache/LiteSpeed (Hostinger) with clean URLs via `.htaccess`.

## Structure

```
index.html  about.html  contact.html  privacy.html  terms.html  404.html
projects/   index.html + 5 case studies   (nav label: "Work")
services/   index.html + 5 service pages
blog/       index.html + 6 articles
api/        contact.php (form handler), config.php (set CONTACT_TO), data/ (blocked from web)
assets/     fonts, images, js (Lenis, GSAP, interactions.js)
sitemap.xml  robots.txt  llms.txt
```

## Before going live — placeholders to replace

- Phone `(000) 000-0000` / `tel:+10000000000`, e-mail `info@xxxxxxxx.com`, street address, hours.
- `api/config.php` → `CONTACT_TO` (inbox that receives form leads). Submissions are always also stored in `api/data/submissions.jsonl`.
- Social links point to generic roots (x.com, linkedin.com, instagram.com, facebook.com) until real profiles exist.
- Numbers shown as `00+`, `0.0M+`, `+00%` are placeholders; replace with real, verifiable metrics.
- Testimonials are role-only (no invented names). Replace with real client quotes when available.
- Team cards use "Name Surname"; portraits and avatars are AI-generated placeholders.
- Case-study dates / durations / results and the "typical launch / reporting" values on service pages are illustrative.
- Privacy Policy and Terms of Service are generic drafts — have them reviewed by counsel.
