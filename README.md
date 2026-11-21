[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/yannyonn94/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/yannyonn94/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World in One Image — Friday, 20 November 2026

One image summing up the world news of Friday, 20 November 2026, for the
[make.fun bounty](https://make.fun/bounty/news-image-20261120).

Six stories, verified from the day's reporting:

1. **The Hague** — the ICJ rules Myanmar committed genocide against the
   Rohingya, 9–6, the first such finding against a state.
2. **Shenzhen** — Trump, Xi and Putin hold their first trilateral summit and
   sign a joint peace declaration.
3. **Kyiv** — Russian overnight missile and drone strikes kill 8 and injure
   28; Russian missiles and a drone enter Polish airspace.
4. **Riyadh** — a Houthi missile damages Saudi Arabia's PIF tower; Saudi
   Arabia intercepts another missile and 5 drones.
5. **Antalya** — the COP31 draft agreement drops all references to phasing
   out fossil fuels.
6. **Markets** — US stocks fall for a fifth straight day and Japan's Nikkei
   drops 4.8% after Anthropic's Nasdaq debut.

The footer also notes the day's secondary briefs: Kenya's last Ebola
patient discharged, Israeli forces crossing Gaza's Yellow Line, the EU–UK
summit in Brussels, and Italy's €805m fine against Meta.

## How it runs

`main.py` (Python 3.13, standard library only) copies the pre-made
`entry.png` in this repository to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output`). No network, fully deterministic — both runs write
identical bytes.

The image itself is drawn by `render.py` (Pillow + DejaVu fonts, run at
build time only) as a 1024×1024 newspaper-poster layout: a dark masthead
naming the day, six story cards, and a footer strip.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Verification

The image is a whole PNG, 1024×1024 pixels, under 1 MiB. The program is
deterministic: running it twice writes byte-identical files.

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum out1/entry.png out2/entry.png   # the two hashes must match
python3 -c "from PIL import Image; im = Image.open('entry.png'); print(im.format, im.size)"
```

To re-draw the image from scratch, run `python3 render.py` (needs Pillow
and the DejaVu fonts; build time only — `main.py` itself needs nothing
beyond the Python standard library).
