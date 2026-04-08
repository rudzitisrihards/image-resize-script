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

`crop.py` center-crops batches of high-resolution JPEGs into 6 aspect ratios for an Etsy print shop. It never resizes — output pixel dimensions are exact crop dimensions only. Every output file is explicitly saved at 300 DPI.

## Accepted source dimensions (strict)

Only two exact sizes are accepted. Anything else is skipped with a warning and does not consume a counter slot:

- Landscape: `10630 × 7087` px
- Portrait: `7087 × 10630` px

## Crop dimension constants

All valid output dimensions are hardcoded in `LANDSCAPE_CROPS` and `PORTRAIT_CROPS` at the top of `crop.py`. Landscape crops always preserve the full height (7087); portrait crops always preserve the full width (7087). The trimmed dimension is always center-offset using integer division.

## Output structure

Each source image produces one subfolder named with a 4-digit zero-padded number (e.g. `0042/`), containing exactly 6 files prefixed with that same number: `0042_Ratio_1x1.jpg`, `0042_Ratio_2x3.jpg`, etc. The counter starts at `--start` and increments only for successfully processed images.

The output folder must not exist before running — the script exits cleanly if it does.
