import os
import argparse
from PIL import Image, ImageEnhance

# Sketches Order
SKETCHES = {
    'Malenia2': "2026_07_02_malenia_pencil_2.jpeg",
    "Xenomorph": "2026_02_20_xenomorph_pencil_2.jpeg",
    "Maliketh": "2026_06_29_maliketh_pencil_1.jpeg",
    "Pantheon": "2026_02_19_pantheon_pencil_1.jpeg",
    "Bela Dimitrescu": "2026_02_27_bella_dimitrescu_pencil_1.jpeg",
    "Kindred": "2026_02_21_kindred_pencil_1.jpeg",
    "Sukuna, Gojo & Mahoraga": "2026_02_27_sukuna_gojo_mahoraga_pencil_1.jpeg",
    "Jinx, Warwick & Silco": "2026_02_21_jinx_warwick_silco_pencil_1.jpeg",
    "Jinx & Death": "2026_02_19_jinx_wolf_pencil_1.jpeg",
    "Guts": "2026_02_17_berserk_pencil_1.jpeg",
    "Griffith": "2026_02_18_berserk_pencil_2.jpeg",
}

def clean_and_build(contrast_val, brightness_val, sharpness_val, use_grey):
    print(
        f"Cleaning up images (Contrast: {contrast_val}, Brightness: {brightness_val}, Sharpness: {sharpness_val}, Greyscale: {use_grey}) and building README..."
    )

    os.makedirs("pencil_sketches/original", exist_ok=True)

    processed_count = 0
    valid_sketches = []

    for title, img_name in SKETCHES.items():
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
                valid_sketches.append((title, img_name))
        else:
            print(f"Skipping: {img_name} not found in pencil_sketches/original/")

    def cell(title, img_name):
        return (
            '    <td width="50%" align="center">\n'
            f'      <img src="pencil_sketches/{img_name}" alt="{title}" width="100%">\n'
            f"      <br><sub>{title}</sub>\n"
            "    </td>\n"
        )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Personal Sketchbook\n\n")
        f.write("## Pencil on paper\n\n")
        f.write("<table>\n")

        for i in range(0, len(valid_sketches), 2):
            f.write("  <tr>\n")
            for title, img_name in valid_sketches[i:i + 2]:
                f.write(cell(title, img_name))
            f.write("  </tr>\n\n")

        f.write("</table>\n\n")
        f.write("## Usage\n\n")
        f.write("```bash\n")
        f.write(
            "python pencil_sketch_processor.py "
            "--contrast 3.0 --brightness 1.0 --sharpness 1.0\n"
        )
        f.write("```\n")

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