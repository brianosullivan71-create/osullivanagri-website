"""Clean up O'Sullivan Agri photos for the website.
Tames glare from shop lights, lifts shadows, neutralises colour cast, sharpens, resizes for web.
Usage: python3 tools/clean_photos.py <in_dir> <out_dir>
"""
import sys, pathlib
import cv2
import numpy as np
from PIL import Image, ImageOps

# per-photo settings: crop_top = fraction of ceiling to trim, glare = strength 0..1
SETTINGS = {
    "osa-fb-08": dict(crop_top=0.00, glare=0.8),
    "osa-fb-09": dict(crop_top=0.06, glare=1.0),
    "osa-fb-10": dict(crop_top=0.06, glare=1.0),
    "osa-fb-12": dict(crop_top=0.05, glare=1.0),
    "osa-fb-19": dict(crop_top=0.06, glare=1.0),
    "osa-fb-20": dict(crop_top=0.06, glare=1.0),
}
DEFAULT = dict(crop_top=0.0, glare=0.5)
MAX_EDGE = 1600


def clean(bgr, glare):
    img = bgr.astype(np.float32) / 255.0

    # 1. neutralise colour cast (half-strength grey-world)
    means = img.reshape(-1, 3).mean(0)
    gain = means.mean() / np.maximum(means, 1e-4)
    img = np.clip(img * (1 + 0.5 * (gain - 1)), 0, 1)

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L = lab[..., 0] / 100.0

    # 2. glare: soften the blown-out light cores, then roll off highlights
    if glare > 0:
        core = (L > 0.97).astype(np.uint8)
        core = cv2.dilate(core, np.ones((5, 5), np.uint8))
        halo = cv2.GaussianBlur(core.astype(np.float32), (0, 0), sigmaX=max(L.shape) / 40)
        halo = halo / (halo.max() + 1e-6)
        L = L - 0.12 * glare * halo  # pull the halo around each light down
        knee = 0.70
        over = np.clip(L - knee, 0, None)
        L = np.where(L > knee, knee + over * (1 - 0.45 * glare), L)

    # 3. lift shadows / local contrast
    L8 = np.clip(L * 255, 0, 255).astype(np.uint8)
    clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
    L2 = clahe.apply(L8).astype(np.float32) / 255.0
    L = 0.6 * L2 + 0.4 * np.clip(L, 0, 1)
    L = np.power(np.clip(L, 0, 1), 0.93)  # slight overall brighten of mid/shadows

    lab[..., 0] = L * 100.0
    # 4. a touch more colour
    lab[..., 1] *= 1.08
    lab[..., 2] *= 1.08
    out = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    out = np.clip(out, 0, 1)

    # 5. gentle sharpen
    blur = cv2.GaussianBlur(out, (0, 0), 1.2)
    out = np.clip(out + 0.45 * (out - blur), 0, 1)
    return (out * 255).astype(np.uint8)


def process(src, dst):
    s = SETTINGS.get(src.stem, DEFAULT)
    pil = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    bgr = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    if s["crop_top"]:
        bgr = bgr[int(bgr.shape[0] * s["crop_top"]):]
    out = clean(bgr, s["glare"])
    im = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)


if __name__ == "__main__":
    src_dir, out_dir = map(pathlib.Path, sys.argv[1:3])
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in sorted(src_dir.glob("*.jpg")):
        process(f, out_dir / f.name)
        print("cleaned", f.name)
