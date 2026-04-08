# crop.py — Batch JPEG Aspect Ratio Cropper

A Python 3 script that batch-crops JPEG images into multiple aspect ratios based on specific source dimensions.

## What it does

Given a folder of source JPEGs, the script center-crops each image into 6 standard aspect ratios and saves the results into numbered subfolders. No resizing is ever performed — output files are pure crops at exact pixel dimensions.

**Supported source dimensions:**

| Orientation | Dimensions |
|-------------|------------|
| Landscape   | 10630 × 7087 px |
| Portrait    | 7087 × 10630 px |

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
│   ├── 0001_Ratio_1x1.jpg
│   ├── 0001_Ratio_2x3.jpg
│   ├── 0001_Ratio_3x4.jpg
│   ├── 0001_Ratio_4x5.jpg
│   ├── 0001_Ratio_5x7.jpg
│   └── 0001_Ratio_A-size-EU.jpg
├── 0002/
│   └── ...
```

Subfolder numbering starts at a user-specified value and is always zero-padded to 4 digits. The filename prefix always matches the subfolder name.

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
- Images with unexpected dimensions are skipped with a warning and do not consume a subfolder number
- The `2x3` ratio is a full-source copy (no trimming) but is still re-saved with explicit 300 DPI metadata
