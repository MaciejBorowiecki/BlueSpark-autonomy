import cv2
import math
from ultralytics import YOLO
from ultralytics.utils import LOGGER
from distance_utils import z_from_pixel_width, angle_from_center, euclidean_distance_from_z_and_angle


LOGGER.setLevel("ERROR")    # turn off yolo status info except errors
model = YOLO("yolo11n.pt").to("cpu")
THRESH = 0.5    # Treshold for yolo model
DEBUG = True    # printing info on console


# main computing method
def detect_objects(frame):
    """Returns modified frame with detected objects and information about distances.
       Detect object in every given camera frame, calculate distance between
       center of the camera and the object and show this info on screen"""  
    results = model(frame, imgsz=224, verbose=False)
    objs = []   
    h, w = frame.shape[:2]

    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0]) 
            if conf < THRESH:
                continue
            cls = int(box.cls[0])
            label = model.names[cls]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            pw = x2 - x1            # object width in pixels
            xc = (x1 + x2) / 2.0    # center of an object in pixel

            # Z (depth) from width
            z_cm = z_from_pixel_width(label, pw)
            angle_rad = angle_from_center(w, xc)
            
            # calculate distance to object in cm
            D_cm = euclidean_distance_from_z_and_angle(
                z_cm, angle_rad) if z_cm is not None else None

            # draw bounding box for the object, and write information about distance if there is any
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if D_cm is not None:
                text = f"{label} {conf:.2f} {D_cm:.1f}cm"
            elif z_cm is not None:
                text = f"{label} {conf:.2f} Z:{z_cm:.1f}cm"
            else:
                text = f"{label} {conf:.2f}"

            cv2.putText(frame, text, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            objs.append({"label": label, "conf": conf, "pw": pw, "z_cm": z_cm,
                        "D_cm": D_cm, "angle_deg": math.degrees(angle_rad)})
            
            # print more info about detected object to console 
            if DEBUG:
                print(
                    f"[DEBUG] {label} pw={pw}px z={z_cm}cm angle={math.degrees(angle_rad):.2f}° D={D_cm}cm")

    return frame, objs
