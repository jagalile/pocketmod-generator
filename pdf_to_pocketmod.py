# pdf_to_pocketmod.py
#
# Author: github.com/jagalile
# Date: 2025-07-16
# Description: A Python script that converts an 8-page A4 PDF
#              into a single A4 PDF formatted to be printed as a PocketMod.
# Usage: python pdf_to_pocketmod.py <input_file.pdf>

import argparse
import sys
import pymupdf

# --- CONSTANTS AND CONFIGURATION ---

# Get the dimensions of an A4 sheet in landscape orientation.
# PyMuPDF's coordinate system has its origin (0,0) at the top-left corner.
# paper_size returns a tuple (width, height).
A4_LANDSCAPE_SIZE = pymupdf.paper_size("a4-l")

# Imposition layout for the PocketMod format.
# Defines the position, source page index, and rotation for each of the 8 panels.
# The structure is based on a detailed analysis of the PocketMod folding process.
# Reference: Table 1 of the technical report.
POCKETMOD_LAYOUT_BOTTOM = [
    # Upper row (panels are placed upside down)
    {"source_page_index": 5, "rotation": 180, "grid_pos": (0, 0)},
    {"source_page_index": 6, "rotation": 180, "grid_pos": (0, 1)},
    {"source_page_index": 7, "rotation": 180, "grid_pos": (0, 2)},  # Back cover
    {"source_page_index": 0, "rotation": 180, "grid_pos": (0, 3)},  # Front cover
    # Lower row (panels are placed in normal orientation)
    {"source_page_index": 4, "rotation": 0, "grid_pos": (1, 0)},
    {"source_page_index": 3, "rotation": 0, "grid_pos": (1, 1)},
    {"source_page_index": 2, "rotation": 0, "grid_pos": (1, 2)},
    {"source_page_index": 1, "rotation": 0, "grid_pos": (1, 3)},
]

POCKETMOD_LAYOUT_TOP = [
    # Upper row (panels are placed in normal orientation)
    {"source_page_index": 5, "rotation": 0, "grid_pos": (0, 0)},
    {"source_page_index": 6, "rotation": 0, "grid_pos": (0, 1)},
    {"source_page_index": 7, "rotation": 0, "grid_pos": (0, 2)},  # Back cover
    {"source_page_index": 0, "rotation": 0, "grid_pos": (0, 3)},  # Front cover
    # Lower row (panels are placed upside down)
    {"source_page_index": 4, "rotation": 180, "grid_pos": (1, 0)},
    {"source_page_index": 3, "rotation": 180, "grid_pos": (1, 1)},
    {"source_page_index": 2, "rotation": 180, "grid_pos": (1, 2)},
    {"source_page_index": 1, "rotation": 180, "grid_pos": (1, 3)},
]

# --- HELPER FUNCTIONS ---


def calculate_target_rect(
    page_width: float, page_height: float, grid_pos: tuple
) -> pymupdf.Rect:
    """
    Calculates the destination rectangle (pymupdf.Rect) for a specific panel
    on the 4x2 grid of the output page.
    """
    rows, cols = 2, 4
    cell_width = page_width / cols
    cell_height = page_height / rows

    row, col = grid_pos

    x0 = col * cell_width
    y0 = row * cell_height
    x1 = x0 + cell_width
    y1 = y0 + cell_height

    return pymupdf.Rect(x0, y0, x1, y1)


# --- MAIN FUNCTION ---


def create_pocketmod_pdf(input_path: str, layout: str) -> None:
    """
    Main function that reads an 8-page PDF and creates a single-page PDF
    in PocketMod format.
    """
    try:
        # Open the source PDF document
        source_doc = pymupdf.open(input_path)
    except Exception as e:
        print(f"Error: Could not open input file '{input_path}'.")
        print(f"Detail: {e}")
        sys.exit(1)

    # Validation: Ensure the source document has exactly 8 pages.
    if len(source_doc) != 8:
        print(
            f"Error: Input file must have exactly 8 pages. "
            f"The provided file has {len(source_doc)} pages."
        )
        source_doc.close()
        sys.exit(1)

    print("Input file validated. Creating PocketMod PDF...")

    # Create a new PDF document in memory for the output
    output_doc = pymupdf.open()

    # Add a single blank page in A4 landscape size
    output_page = output_doc.new_page(
        width=A4_LANDSCAPE_SIZE[0], height=A4_LANDSCAPE_SIZE[1]
    )

    if layout not in ["bottom", "top"]:
        print(
            f"Error: Invalid layout option '{layout}'. "
            f"Please use 'bottom' or 'top'."
        )
        source_doc.close()
        sys.exit(1)
    elif layout == "bottom":
        pocketmod_layout = POCKETMOD_LAYOUT_BOTTOM
    elif layout == "top":
        pocketmod_layout = POCKETMOD_LAYOUT_TOP

    # Iterate through the imposition map to place each page
    for panel_info in pocketmod_layout:
        # Get the information for the current panel
        source_page_idx = panel_info["source_page_index"]
        rotation = panel_info["rotation"]
        grid_pos = panel_info["grid_pos"]

        # Calculate the target rectangle on the output page
        target_rect = calculate_target_rect(
            page_width=output_page.rect.width,
            page_height=output_page.rect.height,
            grid_pos=grid_pos,
        )

        # Use show_pdf_page to place the source page in the target rectangle.
        # This function is the core of the operation. It treats the source page as a
        # vector object, preserving quality and allowing for precise transformations.
        output_page.show_pdf_page(
            target_rect,  # Where to place the page
            source_doc,  # From which document to take the page
            source_page_idx,  # Which page number to take
            rotate=rotation,  # With what rotation to display it
        )

    # Save the output document to the specified path

    try:
        output_path = input_path.replace(".pdf", f"_pocketmod-{layout}.pdf")
        output_doc.save(output_path, garbage=4, deflate=True, clean=True)
        print(f"Success! PocketMod file saved to: {output_path}")
    except Exception as e:
        print(f"Error: Could not save output file to '{output_path}'.")
        print(f"Detail: {e}")
        sys.exit(1)
    finally:
        # Make sure to close all documents
        source_doc.close()
        output_doc.close()


# --- SCRIPT ENTRY POINT ---

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Converts an 8-page PDF into a single-page PocketMod layout."
    )

    # Add required positional arguments
    parser.add_argument("input_file", help="The path to the 8-page input PDF file.")

    # Add the optional argument for layout
    parser.add_argument(
        "-l",
        "--layout",
        type=str,
        default="bottom",
        help="The layout of the PocketMod PDF. Default is open pages in 'bottom'.",
    )

    # Parse the arguments provided by the user
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    create_pocketmod_pdf(input_path=args.input_file, layout=args.layout)
