"""One-off: turn the raw WhatsApp photos into web-optimised, semantically named assets."""
import glob
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path("C:/Users/hp/Downloads/Bro J")
FOLDERS = {
    "A": "WhatsApp Unknown 2026-09-30 at 11.40.53 AM",
    "B": "WhatsApp Unknown 2026-09-30 at 11.40.05 AM",
    "C": "WhatsApp Unknown 2026-09-30 at 11.40.39 AM",
}
files = {k: sorted(glob.glob(str(SRC / f / "*.jpeg"))) for k, f in FOLDERS.items()}

# key -> (folder letter, index in sorted list)
PROJECTS = {
    "residential": [("B", i) for i in (0, 2, 51, 55, 56, 57, 31, 32, 36, 54)],
    "estates": [("B", i) for i in (53, 9, 10, 11, 19, 22, 23, 25, 26, 27, 34, 37, 38, 33)]
    + [("A", i) for i in range(4)] + [("C", 0)],
    "civil": [("B", i) for i in (1, 3, 4, 52, 41, 42, 30, 43, 48, 49, 13, 6, 7)]
    + [("C", i) for i in (1, 2, 3)],
    "supervision": [("B", i) for i in (5, 12, 14, 15, 16, 17, 18, 21, 24, 35, 39)],
}
PEOPLE = {"founder": ("B", 47), "founder_alt": ("B", 46), "founder_field": ("B", 45), "founder_desk": ("B", 50)}


def save(src, dst, max_side, q):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((max_side, max_side))
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)


for cat, items in PROJECTS.items():
    for n, (k, i) in enumerate(items, 1):
        save(files[k][i], f"assets/projects/{cat}_{n:02d}.jpg", 1000, 78)
for name, (k, i) in PEOPLE.items():
    save(files[k][i], f"assets/people/{name}.jpg", 1000, 85)
save(files["B"][53], "assets/hero.jpg", 1800, 72)
print("done")
