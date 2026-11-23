# Lightfeet Apps GitHub Pages

Unified support, FAQ, marketing, and privacy policy website published at `https://lightfeet-apps.github.io/`.

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
└── googlee2f775c6e1b89cb7.html     # Google Search Console verification
```

## Regenerating Pages

To regenerate the root landing pages (`index.html`, `fi/index.html`), all 8 PlusMinus pages under `plusminus/`, and `sitemap.xml`:

```bash
python3 scripts/build_site.py
```

Note that `wakeup/` is mirrored from `wakeup-support` and is not overwritten by `build_site.py`.

## Migrating Away from Legacy `wakeup-support`

While the separate `lightfeet-apps/wakeup-support` repository still has GitHub Pages enabled, **do not create a `wakeup-support/` directory in this repository**, because GitHub Pages routes project sites at `/wakeup-support/` separately from the organization root site.

Once all App Store Connect, Search Console, and in-app WakeUp links are updated to point to `https://lightfeet-apps.github.io/wakeup/...`:

1. Keep `wakeup/` in this repository as the active location.
2. Disable GitHub Pages in `lightfeet-apps/wakeup-support` (Repository Settings → Pages) or archive that repository when ready.
