# gen_charuco_pdf.py
import cv2
import numpy as np
import img2pdf

# ---------------- Parametry planszy ----------------
squares_x = 5           # liczba pól w poziomie
squares_y = 7           # liczba pól w pionie
square_length_m = 0.035 # długość boku pola w metrach (35 mm)
marker_length_m = 0.7 * square_length_m
DPI = 300               # drukarska rozdzielczość
# ----------------------------------------------------

# Konwersja metry → piksele
inch_per_meter = 39.3700787
px_per_meter = DPI * inch_per_meter
square_length_px = int(round(square_length_m * px_per_meter))
width_px = squares_x * square_length_px
height_px = squares_y * square_length_px

# Inicjalizacja słownika ArUco
aruco = cv2.aruco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Tworzenie planszy ChArUco (OpenCV 4.12+)
board = aruco.CharucoBoard((squares_x, squares_y),
                           square_length_m,
                           marker_length_m,
                           aruco_dict)

# Generowanie obrazu w OpenCV
img = board.generateImage((width_px, height_px))

# ✅ Białe tło i czarne markery
img = 255 - img  # odwracamy kolory: czarne markery na białym tle

# Zapis tymczasowy do PNG
tmp_png = "charuco_temp.png"
cv2.imwrite(tmp_png, img)

# Konwersja PNG do PDF A4 przy zachowaniu proporcji
a4_width_mm = 210
a4_height_mm = 297
a4_width_pt = img2pdf.mm_to_pt(a4_width_mm)
a4_height_pt = img2pdf.mm_to_pt(a4_height_mm)

pdf_bytes = img2pdf.convert(tmp_png, 
                            layout_fun=img2pdf.get_layout_fun(
                                pagesize=(a4_width_pt, a4_height_pt)
                            ))

pdf_file = "charuco_A4.pdf"
with open(pdf_file, "wb") as f:
    f.write(pdf_bytes)

print(f"[OK] Zapisano planszę ChArUco w PDF: {pdf_file}")
print(f"Wymiary obrazu w px: {width_px}x{height_px}, kwadrat: {square_length_m*1000:.1f} mm")
print("Drukuj w 100% (no scaling), białe tło + czarne markery")
