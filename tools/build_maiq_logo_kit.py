from pathlib import Path

from PIL import Image


ROOT = Path(r"C:\Users\mabra\Documents\GitHub\maiq\brand\maiq-logo-kit")
SOURCE = Path(r"C:\Users\mabra\.codex\generated_images\01a049b7-6b17-7392-abaa-d227db99e760")

ASSETS = {
    "symbol/maiq-symbol-color.png": "exec-d8418a08-5ab2-4caf-a969-a63388d68081.png",
    "symbol/maiq-symbol-ivory.png": "exec-e58b0bc8-2a31-4685-8af0-5a81456a0cee.png",
    "monogram/maiq-monogram-mq-violet.png": "exec-466a70aa-ca60-4544-8ddb-4321553ebc8d.png",
    "monogram/maiq-monogram-mq-ivory.png": "exec-6666f6b0-56e3-4421-a3a3-bd4d56b0be5b.png",
    "signature/maiq-signature-color.png": "exec-b2fb2b14-bd85-448f-be76-8c7646a07c41.png",
    "signature/maiq-signature-ivory.png": "exec-75bdaf03-d58f-42e8-8acc-c5080d734d92.png",
}


def clean_alpha(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    red, green, blue, alpha = image.split()
    # Remove low-opacity generation halos while retaining a narrow antialiased edge.
    alpha = alpha.point(lambda value: 0 if value <= 178 else min(255, (value - 178) * 4))
    image = Image.merge("RGBA", (red, green, blue, alpha))
    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)
    padding = max(24, round(max(image.size) * 0.035))
    canvas = Image.new("RGBA", (image.width + padding * 2, image.height + padding * 2))
    canvas.alpha_composite(image, (padding, padding))
    return canvas


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    built = {}
    for relative_path, source_name in ASSETS.items():
        image = clean_alpha(Image.open(SOURCE / source_name))
        destination = ROOT / relative_path
        save_png(image, destination)
        built[relative_path] = image

    symbol = built["symbol/maiq-symbol-color.png"]
    for size in (512, 256, 128, 64, 32):
        resized = symbol.copy()
        resized.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size))
        canvas.alpha_composite(resized, ((size - resized.width) // 2, (size - resized.height) // 2))
        save_png(canvas, ROOT / "icons" / f"maiq-icon-{size}.png")

    # Browser-friendly favicon PNG.
    save_png(Image.open(ROOT / "icons" / "maiq-icon-32.png"), ROOT / "icons" / "favicon-32.png")


if __name__ == "__main__":
    main()
