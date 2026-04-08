import argparse
import sys
from pathlib import Path
from PIL import Image

LANDSCAPE = (10630, 7087)
PORTRAIT = (7087, 10630)

LANDSCAPE_CROPS = {
    "2x3":      (10630, 7087),
    "3x4":      (9449,  7087),
    "4x5":      (8859,  7087),
    "5x7":      (9922,  7087),
    "1x1":      (7087,  7087),
    "A-size-EU":(10023, 7087),
}

PORTRAIT_CROPS = {
    "2x3":      (7087, 10630),
    "3x4":      (7087, 9449),
    "4x5":      (7087, 8859),
    "5x7":      (7087, 9922),
    "1x1":      (7087, 7087),
    "A-size-EU":(7087, 10023),
}


def compute_box(crop_w, crop_h, orientation):
    if orientation == "landscape":
        x = (LANDSCAPE[0] - crop_w) // 2
        return (x, 0, x + crop_w, crop_h)
    else:
        y = (PORTRAIT[1] - crop_h) // 2
        return (0, y, crop_w, y + crop_h)


def process_image(src_path, subfolder, prefix, crops, orientation):
    img = Image.open(src_path)
    for ratio_name, (crop_w, crop_h) in crops.items():
        box = compute_box(crop_w, crop_h, orientation)
        cropped = img.crop(box)
        out_name = f"{prefix}_Ratio_{ratio_name}.jpg"
        out_path = subfolder / out_name
        cropped.save(out_path, "JPEG", dpi=(300, 300))


def main():
    parser = argparse.ArgumentParser(description="Batch crop JPEGs into multiple aspect ratios.")
    parser.add_argument("--input",  required=True, help="Folder containing source JPEGs")
    parser.add_argument("--output", required=True, help="Folder where numbered subfolders will be created")
    parser.add_argument("--start",  required=True, type=int, help="Starting folder number")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.is_dir():
        print(f"Error: input folder does not exist: {input_dir}")
        sys.exit(1)

    if output_dir.exists():
        print(f"Error: output folder already exists: {output_dir}")
        print("Remove or rename it before running this script.")
        sys.exit(1)

    sources = sorted(
        [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg")],
        key=lambda p: p.name.lower(),
    )

    if not sources:
        print("No JPEG files found in input folder.")
        sys.exit(0)

    output_dir.mkdir(parents=True)

    counter = args.start
    for src in sources:
        img = Image.open(src)
        dims = (img.width, img.height)

        if dims == LANDSCAPE:
            orientation = "landscape"
            crops = LANDSCAPE_CROPS
        elif dims == PORTRAIT:
            orientation = "portrait"
            crops = PORTRAIT_CROPS
        else:
            print(f"Warning: skipping {src.name} — unexpected dimensions {img.width}×{img.height}")
            continue

        prefix = f"{counter:04d}"
        subfolder = output_dir / prefix
        subfolder.mkdir()

        print(f"Processing {src.name} → {prefix}/ ({orientation})")
        process_image(src, subfolder, prefix, crops, orientation)
        print(f"  Done — 6 files written to {subfolder}")

        counter += 1

    print(f"\nFinished. Processed {counter - args.start} image(s).")


if __name__ == "__main__":
    main()
