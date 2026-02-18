import os
from PIL import Image, ImageEnhance

# Sketches Order
SKETCHES = [
    "2026_02_17_berserk_pencil_1.jpeg",
    "2026_02_18_berserk_pencil_2.jpeg",
    "2026_02_17_jinx_pencil_1.jpeg",
    "2026_02_18_jinx_pencil_3.jpeg",
    "2026_02_18_skull_pencil_1.jpeg",
    "2026_02_17_reptile_pencil_1.jpeg",
    "2026_02_16_jinx_pencil_4.jpeg",
    "2026_02_17_jinx_pencil_2.jpeg",
]


def clean_and_build():
    print("Cleaning up images and building README...")

    for img_name in SKETCHES:
        src_path = f"pencil_sketches/original/{img_name}"
        dst_path = f"pencil_sketches/{img_name}"

        if os.path.exists(src_path):
            with Image.open(src_path) as img:
                print(f"Processing: {src_path}...")
                img = img.convert("L")  # Greyscale
                img = ImageEnhance.Contrast(img).enhance(3)  # Contrast boost
                img.save(dst_path)

    # README.md generator based on SKETCHES order
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Personal Sketchbook\n\n")
        f.write("## Pencil on paper\n\n")

        for i, img_name in enumerate(SKETCHES):
            f.write(f"![](pencil_sketches/{img_name})\n\n")
            if i < len(SKETCHES) - 1:
                f.write("---\n\n")

    print("Done! :)")


if __name__ == "__main__":
    clean_and_build()
