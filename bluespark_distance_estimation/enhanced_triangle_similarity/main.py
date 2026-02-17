import cv2
import time
import sys
from datetime import datetime
from detector import ObjectDetector
from simple_distance_calculator import SimpleDistanceCalculator
from pathlib import Path

# FIXME for remote_addons
project_root=Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

try:
    from remote_addons.vision_manager import VisionControl
    from remote_addons.exceptions import CameraError
except ImportError as e:
    print(f"Import error: {e}.")
    sys.exit(1)
    
from remote_addons.camera import UniversalCamera

def main():
    model_name = "yolo11n.pt"
    model_path = project_root / "ml_models" / model_name
    detector = ObjectDetector(str(model_path))
    distance_calc = SimpleDistanceCalculator()

    try:
        vision_manager = VisionControl()
    except CameraError as e:
        # probably camera initialization error
        exit(1)
    
    
    frame_count = 0
    fps = 0
    last_time = time.time()
    
    while True:
        ret, frame = vision_manager.read()
        if not ret or frame is None:
            continue

        detections = detector.detect_objects(frame, threshold=0.5, imgsz=224)
        
        gate_detected = False 

        for detection in detections:
            x1, y1, x2, y2, label, conf = detection
            
            if label == "gate":
                gate_detected = True

            # drawing information
            if label in distance_calc.object_attrs:
                distance_calc.draw_info(frame, (x1, y1, x2, y2), label, conf)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 100), 1)
                cv2.putText(frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100,100,100), 1)
        
        # calculate FPS
        current_time = time.time()
        frame_count += 1
        if current_time - last_time >= 1.0:
            fps = frame_count / (current_time - last_time)
            frame_count = 0
            last_time = current_time
        
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        vision_manager.update(frame)
        # keyboard controls
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
    
    vision_manager.stop()

if __name__ == "__main__":
    main()