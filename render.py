#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page (1024x1024 PNG).

Composes four AI-generated editorial illustrations with crisp
programmatic text (DejaVu fonts) into a newspaper front page.
Run: python3 render.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (18, 18, 18)          # near-black text
NAVY = (16, 42, 92)         # masthead / kicker blue
RED = (178, 34, 34)         # accent red
GREY = (90, 90, 90)
RULE = (120, 120, 120)
TICKER_BG = (16, 42, 92)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_image(path, tw, th):
    """Center-crop an illustration to the target box."""
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im = im.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)),
                   Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))


def draw_text_block(draw, x, y, max_w, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def story_panel(draw, img, x, y, w, ih, kicker, headline, deck,
                head_size=24, deck_size=16):
    """Image on top, kicker + headline + deck below. Returns bottom y."""
    img = fit_image(img, w, ih)
    draw._image.paste(img, (x, y))
    y += ih + 10
    kf = font(SANS_B, 15)
    draw.text((x, y), kicker, font=kf, fill=RED)
    y += 22
    hf = font(SERIF_B, head_size)
    lines = wrap(draw, headline, hf, w)
    y = draw_text_block(draw, x, y, w, lines, hf, INK, head_size + 6)
    y += 4
    df = font(SANS, deck_size)
    lines = wrap(draw, deck, df, w)
    y = draw_text_block(draw, x, y, w, lines, df, GREY, deck_size + 5)
    return y


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    d._image = page  # helper so story_panel can paste

    # ---- masthead ----
    d.rectangle([0, 0, W, 8], fill=NAVY)
    d.text((24, 22), "THE WORLD IN ONE PICTURE",
           font=font(SANS_B, 20), fill=NAVY)
    d.text((W - 24, 22), "WORLD NEWS", font=font(SANS_B, 20),
           fill=NAVY, anchor="ra")
    d.text((24, 48), "MONDAY, 23 NOVEMBER 2026",
           font=font(SERIF_B, 46), fill=INK)
    d.text((24, 100), "The day's world news, in one image",
           font=font(SANS, 19), fill=GREY)
    d.line([24, 126, W - 24, 126], fill=RULE, width=2)

    # ---- lead story: EU Big Tech tax (left, wide) ----
    lx, ly, lw = 24, 140, 620
    lead_img = fit_image(
        os.path.join(ASSETS,
                     "media-generation-lead-eu-tax-0-d8564f05-406a-4dd6-9316-f7ae2002835b.png"),
        lw, 252)
    page.paste(lead_img, (lx, ly))
    y = ly + 252 + 12
    d.text((lx, y), "BRUSSELS  ·  EUROPE", font=font(SANS_B, 16), fill=RED)
    y += 24
    hf = font(SERIF_B, 36)
    lines = wrap(d, "EU unveils 3% tax on Big Tech to fund its next budget",
                 hf, lw)
    y = draw_text_block(d, lx, y, lw, lines, hf, INK, 42)
    y += 6
    df = font(SANS, 19)
    deck = ("Council chief António Costa's draft cuts €204bn from the "
            "plan and taxes digital giants — as EU leaders prepare for a "
            "summit next week.")
    lines = wrap(d, deck, df, lw)
    y = draw_text_block(d, lx, y, lw, lines, df, GREY, 24)

    # ---- right column: Bangladesh + Lisbon ----
    rx, rw = 668, 332
    story_panel(
        d,
        os.path.join(ASSETS,
                     "media-generation-bangladesh-fire-0-2b4f734b-89ff-4087-9de9-8ce4a001ec73.png"),
        rx, 140, rw, 140,
        "NARAIL  ·  BANGLADESH",
        "Nearly 30 homes torched in political violence",
        "Awami League leaders' homes set ablaze.",
        head_size=22, deck_size=15)
    story_panel(
        d,
        os.path.join(ASSETS,
                     "media-generation-lisbon-march-0-a1927bfc-d285-45a3-9fd3-ef0da4771aa9.png"),
        rx, 402, rw, 140,
        "LISBON  ·  PORTUGAL",
        "Thousands march in rain over living costs",
        "Higher wages, cheaper housing demanded.",
        head_size=22, deck_size=15)

    d.line([24, 672, W - 24, 672], fill=RULE, width=2)

    # ---- bottom story: Baltic ship (image left, text right) ----
    bx, by = 24, 688
    ship_img = fit_image(
        os.path.join(ASSETS,
                     "media-generation-baltic-ship-0-9aee48c9-209a-4112-905a-e294d5f0635a.png"),
        430, 208)
    page.paste(ship_img, (bx, by))
    tx = 478
    d.text((tx, by + 2), "BALTIC SEA  ·  FINLAND",
           font=font(SANS_B, 16), fill=RED)
    hf = font(SERIF_B, 30)
    lines = wrap(d, "Russian cargo ship still burning off Finland after drone strike",
                 hf, W - 24 - tx)
    y = draw_text_block(d, tx, by + 28, W - 24 - tx, lines, hf, INK, 36)
    y += 8
    df = font(SANS, 18)
    deck = ("The Sparta II was hit on Saturday; its 16 crew took to "
            "lifeboats as it drifted into Finnish waters. Finland says "
            "Ukraine was likely behind the attack.")
    lines = wrap(d, deck, df, W - 24 - tx)
    draw_text_block(d, tx, y, W - 24 - tx, lines, df, GREY, 23)

    # ---- ticker strip (auto-fit so nothing runs off the edge) ----
    ty = 924
    d.rectangle([0, ty, W, ty + 56], fill=TICKER_BG)
    ticker = ("ALSO TODAY:   Indonesia fire toll rises: 7 found, 50 missing  ·  "
              "Myanmar: ASEAN move 'unfair'  ·  "
              "Seoul minister quits in AI scandal")
    tsize = 18
    while tsize > 12 and d.textlength(ticker, font=font(SANS_B, tsize)) > W - 48:
        tsize -= 1
    while d.textlength(ticker, font=font(SANS_B, tsize)) > W - 48:
        ticker = ticker.rsplit("  ·  ", 1)[0] + "  …"
    tf = font(SANS_B, tsize)
    d.text((24, ty + (56 - tsize) // 2 - 2), ticker, font=tf,
           fill=(255, 255, 255))

    # ---- footer ----
    d.text((24, 990),
           "The day's world news, as reported on Monday 23 November 2026  ·  "
           "Sources: Reuters, AFP, AP, The Wall Street Journal",
           font=font(SANS, 14), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes",
          page.size)


if __name__ == "__main__":
    main()
