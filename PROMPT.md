# crop.py - Batch JPEG Aspect Ratio Cropper

Before writing any code, plan the implementation out loud and confirm the logic with me first. Only start coding after I approve the plan.

## Overview

A Python 3 script that batch-crops JPEG images into multiple aspect ratios for an Etsy print shop.

## Source images

- All source JPEGs are either `10630×7087` px (landscape) or `7087×10630` px (portrait)
- Resolution is 300 DPI
- They can be named anything - the script processes them in alphabetical order

## Crop logic

- Always center crop - trim only from the longer dimension, never the shorter one
- Landscape: width is trimmed, height (7087) is always preserved
- Portrait: height is trimmed, width (7087) is always preserved
- No resizing ever - only cropping. Output pixel dimensions must be exact crop dimensions, nothing else
- Landscape and portrait sources each produce only their own orientation outputs - never cross-orientation

## Output ratios and exact crop dimensions

**Landscape `10630×7087`:**

- 2x3: 10630×7087 (full source, no trim)
- 3x4: 9449×7087
- 4x5: 8859×7087
- 5x7: 9922×7087
- 1x1: 7087×7087
- A-size-EU: 10023×7087

**Portrait `7087×10630`:**

- 2x3: 7087×10630 (full source, no trim)
- 3x4: 7087×9449
- 4x5: 7087×8859
- 5x7: 7087×9922
- 1x1: 7087×7087
- A-size-EU: 7087×10023

## Folder and file naming

- Output directory is user-specified
- Each source image gets its own numbered subfolder: `0001`, `0002`, etc.
- Subfolder numbering starts at a user-specified number
- Numbers are always 4 digits, zero-padded where needed: `1` → `0001`, `100` → `0100`, `3258` → `3258`
- Each subfolder contains exactly 6 files named: `0001_Ratio_1x1.jpg`, `0001_Ratio_2x3.jpg`, `0001_Ratio_3x4.jpg`, `0001_Ratio_4x5.jpg`, `0001_Ratio_5x7.jpg`, `0001_Ratio_A-size-EU.jpg`
- The folder number and filename prefix always match

## DPI metadata

- Every output file must have 300 DPI written into its JPEG metadata explicitly, regardless of what the source file contains
- This is critical - do not skip or assume it is inherited

## CLI interface

```
python3 crop.py --input /full/path/to/input --output /full/path/to/output --start 1
```

- `--input`: folder containing source JPEGs
- `--output`: folder where numbered subfolders will be created
- `--start`: starting folder number as integer
- Print progress to terminal per image processed: which source file, which subfolder, confirmation when done
- If the output folder already exists, warn the user and exit cleanly - do not overwrite
- If a source image does not match expected dimensions, skip it with a clear warning message

## Dependencies

Python 3 standard library plus Pillow only.
