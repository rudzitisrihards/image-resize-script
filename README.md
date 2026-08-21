# crop.py — Batch JPEG Aspect Ratio Cropper

A Python 3 script that batch-crops JPEG images into multiple aspect ratios based on specific source dimensions.

## What it does

Given a folder of source JPEGs, the script center-crops each image into 6 standard print aspect ratios, plus generates 1 downscaled mockup image, saving the results into numbered subfolders. Print crops are never resized — output files are pure crops at exact pixel dimensions.

**Supported source dimensions (±5px tolerance):**

| Orientation | Dimensions |
|-------------|------------|
| Landscape   | 10630 × 7087 px |
| Portrait    | 7087 × 10630 px |

A source within 5px of a target size on either side is non-proportionally resized to the exact target dimensions before cropping, and the console logs a normalization note. Sources outside tolerance are skipped.

**Output crops per image:**

| Ratio | Landscape (W × H) | Portrait (W × H) |
|-------|-------------------|------------------|
| 2x3 | 10630 × 7087 | 7087 × 10630 |
| 3x4 | 9449 × 7087 | 7087 × 9449 |
| 4x5 | 8859 × 7087 | 7087 × 8859 |
| 5x7 | 9922 × 7087 | 7087 × 9922 |
| 1x1 | 7087 × 7087 | 7087 × 7087 |
| A-size-EU | 10023 × 7087 | 7087 × 10023 |

All output files are saved at 300 DPI regardless of what the source file contains.

## Output structure

```
output/
├── 0001/
│   ├── print/
│   │   ├── 0001_Ratio_1x1.jpg
│   │   ├── 0001_Ratio_2x3.jpg
│   │   ├── 0001_Ratio_3x4.jpg
│   │   ├── 0001_Ratio_4x5.jpg
│   │   ├── 0001_Ratio_5x7.jpg
│   │   └── 0001_Ratio_A-size-EU.jpg
│   └── mockup/
│       └── 0001_Ratio_2x3_small.jpg
├── 0002/
│   └── ...
```

Subfolder numbering starts at a user-specified value and is always zero-padded to 4 digits. The filename prefix always matches the numbered subfolder name.

The `mockup/0001_Ratio_2x3_small.jpg` file is the full-source (2x3) image, proportionally downscaled to 2000px on its longest edge, saved at 72 DPI and full JPEG quality for use in manual mockup creation.

## Requirements

- Python 3
- [Pillow](https://python-pillow.org/)

## Installation

```bash
pip3 install Pillow
```

## Usage

```bash
python3 crop.py --input /path/to/source --output /path/to/output --start 1
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `--input` | Folder containing source JPEGs |
| `--output` | Folder where numbered subfolders will be created |
| `--start` | Starting folder number (integer) |

**Example:**

```bash
python3 crop.py --input ~/Photos/originals --output ~/Photos/cropped --start 42
```

This processes all JPEGs in `originals/` alphabetically, creating subfolders starting at `0042/`.

## Behavior notes

- Source files are processed in alphabetical order
- Both `.jpg` and `.jpeg` extensions are accepted
- The output folder is created automatically — do not create it yourself
- If the output folder already exists, the script exits without making any changes
- Images outside the ±5px tolerance for both orientations are skipped with a warning and do not consume a subfolder number
- Images within tolerance but not an exact pixel match are non-proportionally resized to the exact target dimensions, logged as a normalization note, before any cropping happens
- The `2x3` ratio is a full-source copy (no trimming) but is still re-saved with explicit 300 DPI metadata
- The `mockup/*_small.jpg` file is a proportional (not stretched) downscale of the full source, capped at 2000px on the longest edge
