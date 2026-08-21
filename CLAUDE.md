# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the script

```bash
python3 crop.py --input /path/to/source --output /path/to/output --start 1
```

Install the only dependency before first use:

```bash
pip3 install Pillow
```

## What this script does

`crop.py` center-crops batches of high-resolution JPEGs into 6 print aspect ratios plus 1 downscaled mockup image, for an Etsy print shop. Print crops never resize — output pixel dimensions are exact crop dimensions only. Every print output file is explicitly saved at 300 DPI.

## Accepted source dimensions (5px tolerance)

Two target sizes are recognized, each with a ±5px tolerance per side:

- Landscape: `10630 × 7087` px
- Portrait: `7087 × 10630` px

A source within tolerance but not an exact match is non-proportionally resized to the exact target dimensions before any cropping happens (logged as `{filename} was {w}x{h} – image normalized`). Anything outside tolerance for both orientations is skipped with a warning and does not consume a counter slot.

## Crop dimension constants

All valid output dimensions are hardcoded in `LANDSCAPE_CROPS` and `PORTRAIT_CROPS` at the top of `crop.py`. Landscape crops always preserve the full height (7087); portrait crops always preserve the full width (7087). The trimmed dimension is always center-offset using integer division.

## Output structure

Each source image produces one subfolder named with a 4-digit zero-padded number (e.g. `0042/`), containing two subfolders:

- `print/` — the 6 aspect-ratio crops, prefixed with the folder number: `0042_Ratio_1x1.jpg`, `0042_Ratio_2x3.jpg`, etc. Saved at 300 DPI, quality 100.
- `mockup/` — one file, `0042_Ratio_2x3_small.jpg`: the full-source (2x3) image proportionally downscaled to 2000px on its longest edge, saved at 72 DPI, quality 100, for manual mockup creation.

The counter starts at `--start` and increments only for successfully processed images.

The output folder must not exist before running — the script exits cleanly if it does.
