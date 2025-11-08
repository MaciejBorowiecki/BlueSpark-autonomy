from ultralytics import YOLO
import cv2

model = YOLO("yolo11s.pt").to("cpu")

def detect_bottle(frame, threshold=0.5, imgsz=224):
    # load model with no unnecessary information
    results = model(frame, imgsz=imgsz, verbose=False)
    detections = []
    
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            
            if conf < threshold:
                continue
                
            label = model.names[cls]
            
            # currently handling only bottle
            if label == "bottle":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append((x1, y1, x2, y2, conf))
                
    return detections