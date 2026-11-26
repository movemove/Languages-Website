# AE Interactive — Travel Language Go Portal (`languages.appengine.fun`)

Unified 6-language interactive portal introducing all 5 native Apple apps in the **AE Interactive Travel Language Series**:

- **NihonGo** (Japanese) — `com.chiangkevin.kanamaster` · [App Store `6836279889`](https://apps.apple.com/app/id6836279889) · https://nihongo.appengine.fun
- **EnglishGo** (English) — `com.chiangkevin.englishgo` · [App Store `6837609680`](https://apps.apple.com/app/id6837609680) · https://englishgo.appengine.fun
- **EspanolGo** (Spanish) — `com.chiangkevin.espanolgo` · [App Store `6837611917`](https://apps.apple.com/app/id6837611917) · https://espanolgo.appengine.fun
- **KoreanGo** (Korean) — `com.chiangkevin.koreango` · [App Store `6838241626`](https://apps.apple.com/app/id6838241626) · https://koreango.appengine.fun
- **MandarinGo** (Mandarin Chinese) — `com.chiangkevin.mandaringo` · [App Store `6838245896`](https://apps.apple.com/app/id6838245896) · https://mandaringo.appengine.fun

## Features
- **6 UI Languages:** English (`en`), Traditional Chinese (`zh-Hant`), Simplified Chinese (`zh-Hans`), Japanese (`ja`), Korean (`ko`), and Spanish (`es`) via `?lang=` or `Accept-Language`.
- **Interactive Destination Switcher:** Instant spotlight switching across all 5 apps with real studio MP3 previews, AppIcons, iPhone 6.9" previews, and App Store + official website CTAs.
- **Cross-Language Phrase Comparison Board:** Hear authentic checkout/payment phrases across Japanese, English, Spanish, Korean, and Taiwan/Mainland Mandarin side-by-side.
- **Zero Trackers & Cloudflare Worker Edge Hosting:** Self-contained single-file Worker (`languages-site`) serving HTML, WebP assets, and MP3s with zero cookies or third-party scripts.

## Build & Deploy
```bash
python3 prepare_assets.py
python3 build_and_deploy.py
```
