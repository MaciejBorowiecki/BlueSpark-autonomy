import math

FX_PX = 412.0        # focal length in pixels
CX_PX = 320.0        # The expected center of the image's X axis

# real widths of objects
KNOWN_WIDTHS = {
    "bottle": 7.5,
    "person": 45.0,
    "car": 180.0,
}


# Method to calculate Z (depth) distance between object and camera
def z_from_pixel_width(label, pixel_width):
    """Returns depth Z (cm) calculated from width in pixels.
       FX_PX must be in pixels."""
    if pixel_width == 0:
        return None
    w_real = KNOWN_WIDTHS.get(label)
    if w_real is None:
        return None
    return (w_real * FX_PX) / pixel_width


# Method to calculate angle between object and center of the camera
def angle_from_center(frame_width, object_center_x):
    """Returns angle relative to the center of the image (radians).
       Using FX_PX i CX_PX."""
    
    # center x - calculating with frame widht or using expected frame width
    cx = CX_PX if frame_width is None else frame_width / 2.0
    dx = object_center_x - cx
    
    # Use FX_PX to calculate angle
    return math.atan2(dx, FX_PX)


#
def euclidean_distance_from_z_and_angle(z_cm, angle_rad):
    """Returns real distance in cm between center of the camera and detected object
       using D = Z / cos(theta)"""
    if z_cm is None:
        return None
    cos_t = math.cos(angle_rad)
    if cos_t == 0:
        return None
    return z_cm / cos_t
