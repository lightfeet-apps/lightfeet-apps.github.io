# Lightfeet Apps GitHub Pages

Unified support, FAQ, marketing, and privacy policy website published at `https://lightfeetapps.com/`.

## Repository Structure

```text
/
├── index.html                      # Lightfeet Apps landing page (EN)
├── fi/index.html                   # Lightfeet Apps landing page (FI)
├── plusminus/                      # PlusMinus pages (EN + fi/, generated)
│   ├── index.html                  # Support
│   ├── faq.html                    # Frequently Asked Questions
│   ├── marketing.html              # App overview / marketing page
│   ├── privacy.html                # Privacy Policy
│   └── fi/                         # Finnish translations
├── wakeup/                         # WakeUp pages (EN + fi, sv, de, es, fr)
├── scripts/build_site.py           # Generates root, PlusMinus, and sitemap.xml
├── robots.txt
├── sitemap.xml
└── CNAME                           # Custom domain configuration (lightfeetapps.com)
```

## Regenerating Pages

To regenerate the root landing pages (`index.html`, `fi/index.html`), all 8 PlusMinus pages under `plusminus/`, and `sitemap.xml`:

```bash
python3 scripts/build_site.py
```

Note that `wakeup/` pages are maintained directly in this repository and are not overwritten by `build_site.py`.
