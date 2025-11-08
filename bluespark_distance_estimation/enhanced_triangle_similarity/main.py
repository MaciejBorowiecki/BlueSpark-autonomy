import cv2
import time
from detector import ObjectDetector
from simple_distance_calculator import SimpleDistanceCalculator

def main():
    # initialization
    detector = ObjectDetector("yolo11s.pt")
    distance_calc = SimpleDistanceCalculator()
    
    print("Enhanced Triangle Similarity method")
    print("Press 'q' to exit.")
    
    # camera initialization and setup
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("Nie można otworzyć kamery")
        return
    
    # fps variables
    frame_count = 0
    fps = 0
    last_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect_objects(frame, threshold=0.5, imgsz=320)
        
        # calculate distance for every detection
        for detection in detections:
            x1, y1, x2, y2, label, conf = detection
            
            # check if the type is supported
            if label in distance_calc.object_attrs:
                distance_calc.draw_info(frame, (x1, y1, x2, y2), label, conf)
            else:
                # draw only bounding box for unsupported types
                # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # cv2.putText(frame, f"{label}: {conf:.2f}", (x1, y1-10),
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
                """don't draw bounding box if object is not supported"""
                pass
        
        # calculate and display statistics
        frame_count += 1
        current_time = time.time()
        if current_time - last_time >= 1.0:
            fps = frame_count / (current_time - last_time)
            frame_count = 0
            last_time = current_time
        
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Obiekty: {len(detections)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Metoda: Geometryczna", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow("Enhanced Triangle Similarity", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()