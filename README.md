# PocketMod PDF Generator

A Python script to convert an 8-page A4 PDF into a single A4 PDF formatted for printing as a PocketMod booklet.

## What is a PocketMod?
A PocketMod is a small, foldable booklet made from a single sheet of paper, folded to create 8 pages. This script arranges the pages of your PDF so that, after printing and folding, the pages appear in the correct order and orientation.

## Features
- Takes an 8-page A4 PDF and outputs a single-page A4 PDF in PocketMod layout
- Supports two layout options: `bottom` (default) and `top` (for double-sided printing)
- Uses [PyMuPDF](https://pymupdf.readthedocs.io/) for high-quality PDF manipulation

## Requirements
- Python 3.7+
- [PyMuPDF](https://pymupdf.readthedocs.io/) (install with `pip install pymupdf`)

## Usage

```bash
python pdf_to_pocketmod.py <input_file.pdf> [-l bottom|top]
```

- `<input_file.pdf>`: Path to your 8-page A4 PDF file
- `-l, --layout`: (Optional) Layout for the PocketMod PDF. Use `bottom` for open pages facing down (default), or `top` for open pages facing up (for duplex printing).

### Example

```bash
python pdf_to_pocketmod.py mybooklet.pdf
```

This will create `mybooklet_pocketmod-bottom.pdf` in the same directory.

To use the `top` layout (for double-sided printing):

```bash
python pdf_to_pocketmod.py mybooklet.pdf -l top
```

## Output
- The script creates a new PDF named `<input_file>_pocketmod-bottom.pdf` or `<input_file>_pocketmod-top.pdf`.
- The output is a single A4 landscape page with all 8 panels arranged for PocketMod folding.

## Notes
- The input PDF **must have exactly 8 pages**.
- For best results, ensure your input PDF pages are sized for A4.
- For more information on the PocketMod folding process, see [pocketmod.com](http://www.pocketmod.com/).

## License
See [LICENSE](LICENSE).

---
Author: [github.com/jagalile](https://github.com/jagalile)
