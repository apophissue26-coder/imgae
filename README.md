# curtain-tiff-tool

A Python tool to convert JPG and PNG files into print-ready TIFF files for curtains.

## Features

- Converts `.jpg`, `.jpeg`, and `.png` files to `.tiff`
- Accepts curtain size in centimeters
- Supports **150 DPI** and **300 DPI** output
- Optional seamless pattern generation
- Exports TIFF files with **LZW compression**

## Project Structure

```text
curtain-tiff-tool/
├── input/
├── output/
├── main.py
├── requirements.txt
└── README.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Place source images (`.jpg`, `.jpeg`, `.png`) into `input/`.
2. Run conversion:

```bash
python main.py --width-cm 140 --height-cm 250 --dpi 300
```

### Generate Seamless Patterns

Use `--seamless` to build a mirrored 2x2 tile and repeat it to fill the requested curtain size:

```bash
python main.py --width-cm 140 --height-cm 250 --dpi 150 --seamless
```

## Command Options

- `--input-dir` (default: `input`)
- `--output-dir` (default: `output`)
- `--width-cm` (required)
- `--height-cm` (required)
- `--dpi` (required, must be `150` or `300`)
- `--seamless` (optional flag)

## Output

Converted files are written to `output/` as:

- `<source_name>_150dpi.tiff`
- `<source_name>_300dpi.tiff`

Each TIFF includes:

- LZW compression (`tiff_lzw`)
- Embedded DPI metadata
- Dimensions calculated from curtain size in cm
