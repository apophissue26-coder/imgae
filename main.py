#!/usr/bin/env python3
"""curtain-tiff-tool: Convert JPG/PNG files to LZW-compressed TIFF files for curtain printing."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image

CM_PER_INCH = 2.54
SUPPORTED_DPI = {150, 300}
SUPPORTED_INPUT_EXTS = {".jpg", ".jpeg", ".png"}


def cm_to_pixels(cm: float, dpi: int) -> int:
    """Convert centimeters to pixels at the given DPI."""
    inches = cm / CM_PER_INCH
    return max(1, int(round(inches * dpi)))


def collect_input_images(input_dir: Path) -> Iterable[Path]:
    """Return supported image files from input directory."""
    for path in sorted(input_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED_INPUT_EXTS:
            yield path


def ensure_mode_for_tiff(img: Image.Image) -> Image.Image:
    """Normalize image mode for TIFF export while preserving alpha when possible."""
    if img.mode in {"RGB", "RGBA", "L", "LA"}:
        return img
    if "A" in img.getbands():
        return img.convert("RGBA")
    return img.convert("RGB")


def make_seamless_tile(base_img: Image.Image) -> Image.Image:
    """Create a 2x2 mirrored tile block to soften visible seams."""
    w, h = base_img.size
    canvas = Image.new(base_img.mode, (w * 2, h * 2))

    top_left = base_img
    top_right = base_img.transpose(Image.FLIP_LEFT_RIGHT)
    bottom_left = base_img.transpose(Image.FLIP_TOP_BOTTOM)
    bottom_right = base_img.transpose(Image.ROTATE_180)

    canvas.paste(top_left, (0, 0))
    canvas.paste(top_right, (w, 0))
    canvas.paste(bottom_left, (0, h))
    canvas.paste(bottom_right, (w, h))
    return canvas


def tile_to_size(tile: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """Repeat tile image until target size is filled, then crop."""
    tw, th = tile.size
    out = Image.new(tile.mode, (target_width, target_height))

    for y in range(0, target_height, th):
        for x in range(0, target_width, tw):
            out.paste(tile, (x, y))

    return out


def export_tiff(
    source_path: Path,
    output_dir: Path,
    curtain_width_cm: float,
    curtain_height_cm: float,
    dpi: int,
    seamless: bool,
) -> Path:
    """Convert one source image to a TIFF sized for curtain dimensions."""
    target_width = cm_to_pixels(curtain_width_cm, dpi)
    target_height = cm_to_pixels(curtain_height_cm, dpi)

    with Image.open(source_path) as img:
        img = ensure_mode_for_tiff(img)

        if seamless:
            tile = make_seamless_tile(img)
            final_img = tile_to_size(tile, target_width, target_height)
        else:
            final_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        output_file = output_dir / f"{source_path.stem}_{dpi}dpi.tiff"
        final_img.save(output_file, format="TIFF", compression="tiff_lzw", dpi=(dpi, dpi))

    return output_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert JPG/PNG images into LZW-compressed TIFF files for curtain production.",
    )
    parser.add_argument("--input-dir", default="input", type=Path, help="Input folder containing JPG/PNG files")
    parser.add_argument("--output-dir", default="output", type=Path, help="Output folder for TIFF files")
    parser.add_argument("--width-cm", required=True, type=float, help="Curtain width in centimeters")
    parser.add_argument("--height-cm", required=True, type=float, help="Curtain height in centimeters")
    parser.add_argument("--dpi", required=True, type=int, choices=sorted(SUPPORTED_DPI), help="Target DPI (150 or 300)")
    parser.add_argument(
        "--seamless",
        action="store_true",
        help="Generate a seamless-style repeated pattern from each source image",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.width_cm <= 0 or args.height_cm <= 0:
        raise ValueError("--width-cm and --height-cm must be positive values")

    input_dir: Path = args.input_dir
    output_dir: Path = args.output_dir

    if not input_dir.exists() or not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    source_files = list(collect_input_images(input_dir))
    if not source_files:
        print(f"No JPG/PNG files found in: {input_dir}")
        return

    print(f"Found {len(source_files)} image(s). Starting conversion...")
    for source in source_files:
        out = export_tiff(
            source_path=source,
            output_dir=output_dir,
            curtain_width_cm=args.width_cm,
            curtain_height_cm=args.height_cm,
            dpi=args.dpi,
            seamless=args.seamless,
        )
        print(f"Converted: {source.name} -> {out.name}")

    print("Done.")


if __name__ == "__main__":
    main()
