"""
Generates a printable A4 PDF file of a ChArUco calibration board with
specified physical dimensions.

Printing this PDF at 100% scale (no scaling or "fit to page") is
CRITICAL for accurate camera calibration, as the algorithm relies
on the exact real-world measurements (e.g., square_length_m).
"""

import cv2
import numpy as np
import img2pdf
import os

# ----------------------------------------------------
# Board Configuration
# ----------------------------------------------------
# Define the layout of the board
SQUARES_X = 5           # Number of squares horizontally
SQUARES_Y = 7           # Number of squares vertically

# Define the physical size of the board elements in meters
SQUARE_LENGTH_M = 0.035 # 35 mm
MARKER_LENGTH_M = 0.025 # 25 mm (e.g., 0.7 * SQUARE_LENGTH_M)

# Print quality settings
PRINT_DPI = 300         # Dots Per Inch for the output image
# ----------------------------------------------------

# --- Image Generation ---

# 1. Convert real-world meters to pixels for image generation
INCH_PER_METER = 39.3700787
px_per_meter = PRINT_DPI * INCH_PER_METER
square_length_px = int(round(SQUARE_LENGTH_M * px_per_meter))
width_px = SQUARES_X * square_length_px
height_px = SQUARES_Y * square_length_px

# 2. Initialize the ArUco dictionary
# We use DICT_4X4_50, a common and robust dictionary
aruco = cv2.aruco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# 3. Create the ChArUco board object
board = aruco.CharucoBoard((SQUARES_X, SQUARES_Y),
                           SQUARE_LENGTH_M,
                           MARKER_LENGTH_M,
                           aruco_dict)

# 4. Generate the board image in memory
# This function creates a white background with black markers/squares
img = board.generateImage((width_px, height_px))

# --- PDF Conversion ---

# 5. Save a temporary PNG file
tmp_png = "_charuco_temp.png"
cv2.imwrite(tmp_png, img)

# 6. Define A4 paper size in points (standard for PDF)
a4_width_mm = 210
a4_height_mm = 297
a4_width_pt = img2pdf.mm_to_pt(a4_width_mm)
a4_height_pt = img2pdf.mm_to_pt(a4_height_mm)

# 7. Convert PNG to PDF, centering it on an A4 page
# The layout_fun ensures the image retains its physical size (based on DPI)
# and is centered on the A4 page.
try:
    pdf_bytes = img2pdf.convert(tmp_png,
                                layout_fun=img2pdf.get_layout_fun(
                                    pagesize=(a4_width_pt, a4_height_pt)
                                ))

    pdf_file = "charuco_A4_for_print.pdf"
    with open(pdf_file, "wb") as f:
        f.write(pdf_bytes)

    print(f"[SUCCESS] Generated ChArUco PDF: {pdf_file}")
    print(f"  Board: {SQUARES_X}x{SQUARES_Y} squares")
    print(f"  Square Size: {SQUARE_LENGTH_M * 1000:.1f} mm")
    print(f"  Marker Size: {MARKER_LENGTH_M * 1000:.1f} mm")
    print("------------------------------------------------------------------")
    print("!!! IMPORTANT: Print this PDF at 100% SCALE (no 'fit to page') !!!")
    print("------------------------------------------------------------------")

finally:
    # 8. Clean up the temporary file
    if os.path.exists(tmp_png):
        os.remove(tmp_png)