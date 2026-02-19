import os
import argparse
from PIL import Image, ImageEnhance

# Sketches Order
SKETCHES = [
    "2026_02_19_pantheon_pencil_1.jpeg",
    "2026_02_17_berserk_pencil_1.jpeg",
    "2018_12_30_gun_pencil_1.jpeg",
    "2026_02_17_jinx_pencil_1.jpeg",
    "2026_02_18_berserk_pencil_2.jpeg",
    "2026_02_18_jinx_pencil_3.jpeg",
    "2026_02_16_jinx_pencil_4.jpeg",
    "2026_02_18_skull_pencil_1.jpeg",
    "2026_02_17_reptile_pencil_1.jpeg",
    "2026_02_17_jinx_pencil_2.jpeg",
]


def clean_and_build(contrast_val, brightness_val, sharpness_val, use_grey):
    print(
        f"Cleaning up images (Contrast: {contrast_val}, Brightness: {brightness_val}, Sharpness: {sharpness_val}, Greyscale: {use_grey}) and building README..."
    )

    os.makedirs("pencil_sketches/original", exist_ok=True)

    processed_count = 0
    for img_name in SKETCHES:
        src_path = f"pencil_sketches/original/{img_name}"
        dst_path = f"pencil_sketches/{img_name}"

        if os.path.exists(src_path):
            with Image.open(src_path) as img:
                if use_grey:
                    img = img.convert("L")  # Greyscale

                img = ImageEnhance.Brightness(img).enhance(brightness_val)
                img = ImageEnhance.Sharpness(img).enhance(sharpness_val)
                img = ImageEnhance.Contrast(img).enhance(contrast_val)
                img.save(dst_path)
                processed_count += 1
        else:
            print(f"Skipping: {img_name} not found in pencil_sketches/original/")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Personal Sketchbook\n\n")
        f.write("## Pencil on paper\n\n")

        for i, img_name in enumerate(SKETCHES):
            f.write(f"![](pencil_sketches/{img_name})\n\n")
            if i < len(SKETCHES) - 1:
                f.write("---\n\n")

    print(f"\nDone! Processed {processed_count} images. :)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process pencil sketches.")
    parser.add_argument(
        "--contrast",
        "-c",
        type=float,
        default=3.0,
        help="Contrast boost level",
    )
    parser.add_argument(
        "--brightness",
        "-b",
        type=float,
        default=1.0,
        help="Brightness adjustment level",
    )
    parser.add_argument(
        "--sharpness",
        "-s",
        type=float,
        default=1.0,
        help="Sharpness adjustment level",
    )
    parser.add_argument(
        "--no-grey",
        action="store_false",
        dest="grey",
        help="Disable greyscale conversion",
    )
    parser.set_defaults(grey=True)

    args = parser.parse_args()
    clean_and_build(args.contrast, args.brightness, args.sharpness, args.grey)
