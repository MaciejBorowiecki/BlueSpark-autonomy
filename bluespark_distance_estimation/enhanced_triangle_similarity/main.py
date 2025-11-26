import cv2
import time
import os
from datetime import datetime
from detector import ObjectDetector
from simple_distance_calculator import SimpleDistanceCalculator

def main():
    # --- RECORDING CONFIGURATION ---
    save_folder = "images"
    os.makedirs(save_folder, exist_ok=True)  # Creates images folder if it doesn't exist
    
    auto_save_interval = 2.0  # How often (seconds) to automatically save detected gate
    last_auto_save_time = 0   # Helper variable for time tracking
    # ---------------------------

    # Initialization
    detector = ObjectDetector("trained_gate.pt")
    distance_calc = SimpleDistanceCalculator()
    
    print("Enhanced Pose Estimation & Recording")
    print("Controls:")
    print(" -> 'q': Quit")
    print(" -> 'SPACE': Save image manually")
    
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) 
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not cap.isOpened():
        print("Cannot open camera")
        return
    
    frame_count = 0
    fps = 0
    last_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Copy of clean frame (if you want to save images WITHOUT boxes for training)
        # clean_frame = frame.copy() 

        detections = detector.detect_objects(frame, threshold=0.5, imgsz=640)
        
        gate_detected = False # Flag, whether a gate is present in this frame

        for detection in detections:
            x1, y1, x2, y2, label, conf = detection
            
            # If gate detected, set flag to True
            if label == "gate":
                gate_detected = True

            # Drawing information
            if label in distance_calc.object_attrs:
                distance_calc.draw_info(frame, (x1, y1, x2, y2), label, conf)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 100), 1)
                cv2.putText(frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100,100,100), 1)
        
        # --- AUTO-SAVE LOGIC (When gate detected) ---
        current_time = time.time()
        if gate_detected and (current_time - last_auto_save_time > auto_save_interval):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{save_folder}/auto_gate_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"[AUTO] Gate image saved: {filename}")
            last_auto_save_time = current_time

        # Calculate FPS
        frame_count += 1
        if current_time - last_time >= 1.0:
            fps = frame_count / (current_time - last_time)
            frame_count = 0
            last_time = current_time
        
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Recording mode information
        if gate_detected:
            cv2.circle(frame, (620, 20), 10, (0, 0, 255), -1) # Red "REC" dot
        
        cv2.imshow("Pose & Rotation Estimation", frame)
        
        # --- KEYBOARD HANDLING ---
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord(' '): # ASCII code for space is 32
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Saving images of detected object - manual
            filename = f"{save_folder}/manual_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"[MANUAL] Image saved: {filename}")
            # Screen flash (optional visual confirmation effect)
            cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]), (255,255,255), 5)
            cv2.imshow("Pose & Rotation Estimation", frame)
            cv2.waitKey(50) # Short pause for effect
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()