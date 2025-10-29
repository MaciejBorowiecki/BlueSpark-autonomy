import math

# Konfiguracja -> ustaw po kalibracji
# Wartość focal length w pikselach (uzyskana w calibration.py)
FX_PX = 412.0        # <- ZASTĄP zmierzoną wartością w px
CX_PX = 320.0        # środek obrazu x (dla 640x480 -> 320)
# realne szerokości (cm)
KNOWN_WIDTHS = {
    "bottle": 7.5,
    "person": 45.0,
    "car": 180.0,
}

def z_from_pixel_width(label, pixel_width):
    """Zwraca głębokość Z (cm) wyliczoną z szerokości w pikselach.
       FX_PX musi być w pikselach."""
    if pixel_width == 0:
        return None
    w_real = KNOWN_WIDTHS.get(label)
    if w_real is None:
        return None
    return (w_real * FX_PX) / pixel_width

def angle_from_center(frame_width, object_center_x):
    """Kąt względem środka obrazu (radiany). Używa FX_PX i CX_PX."""
    # center x - możesz liczyć frame_width/2 lub użyć CX_PX z kalibracji
    cx = CX_PX if frame_width is None else frame_width / 2.0
    dx = object_center_x - cx
    # używamy FX_PX (px) do obliczenia kąta
    return math.atan2(dx, FX_PX)   # [radiany]

def euclidean_distance_from_z_and_angle(z_cm, angle_rad):
    """D = Z / cos(theta)"""
    if z_cm is None:
        return None
    cos_t = math.cos(angle_rad)
    if cos_t == 0:
        return None
    return z_cm / cos_t
