import cv2
import time
from detector import detect_bottle
from distance_estimator import load_camera_params, estimate_distance_pnp, estimate_distance_pnp_simple

def main(camera_index=0):
    # load camera parameters
    camera_matrix, dist_coeffs = load_camera_params()
    
    print("Camera calibration loaded successfully")
    print("Method: solvePnP")
    print("YOLO Size: 224")
    print("Press 'q' to exit")
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Cannot open camera.")
        return
    
    # set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # check actual resolution
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera resolution: {actual_width}x{actual_height}")
    
    # start with full PnP
    use_simple_pnp = False
    
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame from camera.")
            break
        
        # keep the original frame for display
        display_frame = frame.copy()
        
        # detect bottles with processing size 320 (Note: variable says 224, was 320 in code)
        bottles = detect_bottle(frame, threshold=0.5, imgsz=224)
        
        for bbox in bottles:
            x1, y1, x2, y2, conf = bbox
            
            # calculate distance using PnP
            if use_simple_pnp:
                distance = estimate_distance_pnp_simple(display_frame, (x1, y1, x2, y2), 
                                                       camera_matrix, dist_coeffs)
            else:
                distance = estimate_distance_pnp(display_frame, (x1, y1, x2, y2), 
                                                camera_matrix, dist_coeffs)
            
            # draw bounding box
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            if distance is not None:
                # display distance
                text = f"{distance:.2f}m (PnP)"
                cv2.putText(display_frame, text, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            else:
                cv2.putText(display_frame, "Dist. N/A (PnP)", (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # display detection confidence
            conf_text = f"conf: {conf:.2f}"
            cv2.putText(display_frame, conf_text, (x1, y2 + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # calculate FPS
        end_time = time.time()
        fps = 1.0 / (end_time - start_time) if (end_time - start_time) > 0 else 0.0
        
        # display info
        cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(display_frame, f"Bottles: {len(bottles)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(display_frame, "Method: solvePnP", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(display_frame, "YOLO: 320px", (10, 120),  # Note: imgsz=224 in code
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # display image
        cv2.imshow("Bottle Detection - solvePnP", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m'):
            use_simple_pnp = not use_simple_pnp
            method = "Simple PnP" if use_simple_pnp else "Full PnP"
            print(f"Switched method to: {method}")

    cap.release()
    cv2.destroyAllWindows()
    print("Application closed.")

if __name__ == "__main__":
    main()