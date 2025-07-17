# PocketMod PDF Generator

A Python script to convert an 8-page A4 PDF (or a single-page PDF, repeated) into a single A4 PDF formatted for printing as a PocketMod booklet.

## What is a PocketMod?
A PocketMod is a small, foldable booklet made from a single sheet of paper, folded to create 8 pages. This script arranges the pages of your PDF so that, after printing and folding, the pages appear in the correct order and orientation.

## Features
- Takes an 8-page A4 PDF and outputs a single-page A4 PDF in PocketMod layout
- Supports two layout options: `top` (default, folds on top) and `bottom` (folds on bottom)
- **NEW:** Supports a single-page PDF as input (with `-r/--repeat`), repeating the page 8 times
- Uses [PyMuPDF](https://pymupdf.readthedocs.io/) for high-quality PDF manipulation

## Requirements
- Python 3.7+
- [PyMuPDF](https://pymupdf.readthedocs.io/) (install with `pip install pymupdf`)

### Installation

Install all required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python pdf_to_pocketmod.py <input_file.pdf> [-l bottom|top] [-r]
```

- `<input_file.pdf>`: Path to your 8-page A4 PDF file (or a single-page PDF if using `-r`)
- `-l, --layout`: (Optional) Layout for the PocketMod PDF. Use `top` for pages folds on top (default), or `bottom` for open pages folds on bottom.
- `-r, --repeat`: (Optional) Use a single-page PDF and repeat it 8 times to fill the PocketMod.

### Examples

**Standard 8-page PDF:**
```bash
python pdf_to_pocketmod.py mybooklet.pdf
```
This will create `mybooklet_pocketmod-top.pdf` in the same directory.

**Single-page PDF, repeated 8 times:**
```bash
python pdf_to_pocketmod.py mypage.pdf -r
```
This will create `mypage_pocketmod-top.pdf` with the same page repeated in all 8 panels.

**Using the `bottom` layout:**
```bash
python pdf_to_pocketmod.py mybooklet.pdf -l bottom
```

## Output
- The script creates a new PDF named `<input_file>_pocketmod-bottom.pdf` or `<input_file>_pocketmod-top.pdf`.
- The output is a single A4 landscape page with all 8 panels arranged for PocketMod folding.

## Notes
- The input PDF **must have exactly 8 pages**, unless you use `-r/--repeat`, in which case it must have exactly 1 page.
- For best results, ensure your input PDF pages are sized for A4.
- For more information on the PocketMod folding process, see [pocketmod.com](http://www.pocketmod.com/).

## License
See [LICENSE](LICENSE).

---
Author: [github.com/jagalile](https://github.com/jagalile)