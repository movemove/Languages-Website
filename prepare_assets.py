#!/usr/bin/env python3
"""Prepare 5-app icons, composite OG banner, resized WebP screenshots, and studio MP3 audio clips for languages.appengine.fun."""
from __future__ import annotations

import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
SCRATCH = Path("/Users/kevin/.gemini/antigravity/scratch")
DESKTOP = Path("/Users/kevin/Desktop")

PUB_IMG = BASE_DIR / "public" / "images"
PUB_AUD = BASE_DIR / "public" / "audio"

ICONS = {
    "nihongo": DESKTOP / "Nihongo Hub" / "AppIcon" / "NihonGo_AppIcon_1024x1024.png",
    "englishgo": DESKTOP / "EnglishGo Hub" / "AppIcon" / "EnglishGo_AppIcon_1024x1024.png",
    "espanolgo": DESKTOP / "EspanolGo Hub" / "AppIcon" / "EspanolGo_AppIcon_1024x1024.png",
    "koreango": DESKTOP / "KoreanGo Hub" / "AppIcon" / "KoreanGo_AppIcon_1024x1024.png",
    "mandaringo": DESKTOP / "MandarinGo Hub" / "AppIcon" / "MandarinGo_AppIcon_1024x1024.png",
}

SCREENSHOTS = {
    "nihongo": [
        SCRATCH / "NihonGo-Website" / "public" / "images" / "en_s01.webp",
        SCRATCH / "NihonGo-Website" / "public" / "images" / "en_s04.webp",
        SCRATCH / "NihonGo-Website" / "public" / "images" / "en_s03.webp",
    ],
    "englishgo": [
        SCRATCH / "EnglishGo-Website" / "public" / "images" / "es_s01.webp",
        SCRATCH / "EnglishGo-Website" / "public" / "images" / "es_s04.webp",
        SCRATCH / "EnglishGo-Website" / "public" / "images" / "es_s03.webp",
    ],
    "espanolgo": [
        SCRATCH / "EspanolGo-Website" / "public" / "images" / "en_s01.webp",
        SCRATCH / "EspanolGo-Website" / "public" / "images" / "en_s04.webp",
        SCRATCH / "EspanolGo-Website" / "public" / "images" / "en_s03.webp",
    ],
    "koreango": [
        SCRATCH / "KoreanGo-Website" / "public" / "images" / "en_s01.webp",
        SCRATCH / "KoreanGo-Website" / "public" / "images" / "en_s04.webp",
        SCRATCH / "KoreanGo-Website" / "public" / "images" / "en_s03.webp",
    ],
    "mandaringo": [
        SCRATCH / "MandarinGo-Website" / "public" / "images" / "en_s01.webp",
        SCRATCH / "MandarinGo-Website" / "public" / "images" / "en_s04.webp",
        SCRATCH / "MandarinGo-Website" / "public" / "images" / "en_s03.webp",
    ],
}

AUDIOS = {
    "jp_split.mp3": SCRATCH / "NihonGo-Website" / "public" / "audio" / "split.mp3",
    "jp_wait.mp3": SCRATCH / "NihonGo-Website" / "public" / "audio" / "wait.mp3",
    "en_bill.mp3": SCRATCH / "EnglishGo-Website" / "public" / "audio" / "check_bill.mp3",
    "en_card.mp3": SCRATCH / "EnglishGo-Website" / "public" / "audio" / "credit_card.mp3",
    "es_split.mp3": SCRATCH / "EspanolGo-Website" / "public" / "audio" / "split.mp3",
    "es_card.mp3": SCRATCH / "EspanolGo-Website" / "public" / "audio" / "card.mp3",
    "ko_split.mp3": SCRATCH / "KoreanGo-Website" / "public" / "audio" / "split.mp3",
    "ko_slowly.mp3": SCRATCH / "KoreanGo-Website" / "public" / "audio" / "slowly.mp3",
    "zh_boba_tw.mp3": SCRATCH / "MandarinGo-Website" / "public" / "audio" / "boba_tw.mp3",
    "zh_pay_tw.mp3": SCRATCH / "MandarinGo-Website" / "public" / "audio" / "pay_tw.mp3",
    "zh_pay_cn.mp3": SCRATCH / "MandarinGo-Website" / "public" / "audio" / "pay_cn.mp3",
}


def round_icon(im: Image.Image, radius_ratio: float = 0.225) -> Image.Image:
    size = im.size[0]
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    r = int(size * radius_ratio)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def build_gradient_bg(w: int, h: int) -> Image.Image:
    bg = Image.new("RGB", (w, h), (7, 9, 19))
    px = bg.load()
    for y in range(h):
        ty = y / max(1, h - 1)
        for x in range(w):
            tx = x / max(1, w - 1)
            r = int(10 + 36 * (1 - tx) * 0.5 + 28 * tx * (1 - ty))
            g = int(14 + 34 * ty + 38 * tx * 0.45)
            b = int(34 + 62 * (1 - ty * 0.4) + 36 * (1 - tx) * 0.3)
            px[x, y] = (min(255, r), min(255, g), min(255, b))
    return bg


def build_hub_favicon(icons: dict[str, Image.Image]) -> None:
    """Create a 512x512 composite rounded tile icon featuring the 5 apps at 2x supersampling."""
    size = 1024
    canvas = build_gradient_bg(size, size).convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([28, 28, size - 29, size - 29], radius=216, outline=(45, 212, 191, 130), width=8)

    order = ["nihongo", "englishgo", "koreango", "espanolgo", "mandaringo"]
    coords = [
        (208, 216, 264),
        (552, 216, 264),
        (136, 544, 228),
        (398, 544, 228),
        (660, 544, 228),
    ]
    for slug, (x, y, s) in zip(order, coords):
        tile = round_icon(icons[slug].resize((s, s), Image.Resampling.LANCZOS), 0.22)
        canvas.paste(tile, (x, y), tile)

    rounded = round_icon(canvas.convert("RGB"), 0.225)
    rounded.resize((512, 512), Image.Resampling.LANCZOS).save(PUB_IMG / "icon.png", format="PNG", optimize=True)
    rounded.resize((256, 256), Image.Resampling.LANCZOS).save(PUB_IMG / "icon.webp", format="WEBP", quality=90)


def build_og_image(icons: dict[str, Image.Image]) -> None:
    w, h = 1200, 630
    canvas = build_gradient_bg(w, h).convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    f_badge = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22, index=1)
    f_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 62, index=1)
    f_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 28, index=0)
    f_lbl = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20, index=1)

    badge_text = "AE INTERACTIVE · TRAVEL LANGUAGE GO SERIES"
    draw.text((88, 66), badge_text, font=f_badge, fill=(45, 212, 191, 245))
    draw.text((88, 108), "5 Languages. Zero Accounts.", font=f_title, fill=(255, 255, 255, 255))
    draw.text((88, 186), "Japanese · English · Spanish · Korean · Mandarin", font=f_sub, fill=(196, 214, 236, 240))

    apps = [
        ("nihongo", "NihonGo"),
        ("englishgo", "EnglishGo"),
        ("espanolgo", "EspanolGo"),
        ("koreango", "KoreanGo"),
        ("mandaringo", "MandarinGo"),
    ]
    ic_size = 158
    gap = 46
    start_x = (w - (5 * ic_size + 4 * gap)) // 2
    y_top = 278

    for idx, (slug, label) in enumerate(apps):
        x = start_x + idx * (ic_size + gap)
        tile = round_icon(icons[slug].resize((ic_size, ic_size), Image.Resampling.LANCZOS), 0.22)
        canvas.paste(tile, (x, y_top), tile)
        tw = draw.textlength(label, font=f_lbl)
        draw.text((x + (ic_size - tw) / 2, y_top + ic_size + 14), label, font=f_lbl, fill=(226, 232, 240, 245))

    foot = "iPhone · iPad · iPhone Duo  |  500 Real Travel Videos · Free + $3.99 Lifetime Pro"
    draw.text((88, 548), foot, font=f_badge, fill=(148, 163, 184, 240))

    canvas.convert("RGB").save(PUB_IMG / "og.png", format="PNG", optimize=True)


def main() -> None:
    PUB_IMG.mkdir(parents=True, exist_ok=True)
    PUB_AUD.mkdir(parents=True, exist_ok=True)

    loaded_icons: dict[str, Image.Image] = {}
    for slug, path in ICONS.items():
        assert path.exists(), f"Missing AppIcon: {path}"
        im = Image.open(path).convert("RGB")
        loaded_icons[slug] = im
        round_icon(im.resize((256, 256), Image.Resampling.LANCZOS), 0.22).save(
            PUB_IMG / f"icon_{slug}.webp", format="WEBP", quality=90
        )

    build_hub_favicon(loaded_icons)
    build_og_image(loaded_icons)

    for slug, src_list in SCREENSHOTS.items():
        for idx, src in enumerate(src_list, 1):
            assert src.exists(), f"Missing screenshot: {src}"
            im = Image.open(src).convert("RGB")
            w, h = im.size
            new_w = 420
            new_h = round(h * (new_w / w))
            resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
            resized.save(PUB_IMG / f"{slug}_s{idx}.webp", format="WEBP", quality=82, method=6)

    for dst_name, src in AUDIOS.items():
        assert src.exists(), f"Missing audio: {src}"
        shutil.copy2(src, PUB_AUD / dst_name)

    img_kb = sum(p.stat().st_size for p in PUB_IMG.glob("*")) / 1024
    aud_kb = sum(p.stat().st_size for p in PUB_AUD.glob("*.mp3")) / 1024
    print(f"ASSETS_READY: images={len(list(PUB_IMG.glob('*')))} ({img_kb:.1f} KB), audio={len(list(PUB_AUD.glob('*.mp3')))} ({aud_kb:.1f} KB)")


if __name__ == "__main__":
    main()
