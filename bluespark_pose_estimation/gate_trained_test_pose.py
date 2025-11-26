from ultralytics import YOLO
import os

def main():
    model_path = 'best.pt'
    
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found.")
        return

    print(f"Loading model: {model_path}...")
    model = YOLO(model_path)

    # CHANGE: Point to the directory instead of a single file
    images_dir = "old_data/images/train"
    
    if not os.path.exists(images_dir):
        print(f"Error: Directory '{images_dir}' not found.")
        return

    print(f"Starting inference on all images in: {images_dir}...")

    # YOLO automatically iterates through all images in the folder provided in 'source'
    results = model.predict(source=images_dir, save=True, stream=True, conf=0.5)

    # 3. Process results loop (iterates through each image in the folder)
    for result in results:
        # Get the filename of the current image being processed
        file_name = os.path.basename(result.path)
        
        # Check if any objects/keypoints were detected in this specific image
        if result.keypoints is not None and result.keypoints.conf is not None and len(result.keypoints.xy) > 0:
            
            # Iterate through ALL detected objects in the image (in case there is more than one gate)
            for obj_idx, kpts in enumerate(result.keypoints.xy):
                points = kpts.cpu().numpy()

                print(f"\n--- Object Detected in file: {file_name} (ID: {obj_idx}) ---")
                
                # Iterate through the points for this object
                for idx, point in enumerate(points):
                    x, y = point
                    
                    if x > 0 and y > 0:
                        print(f"Point {idx}: X={x:.1f}, Y={y:.1f}")
                    else:
                        print(f"Point {idx}: Not visible / Not detected")
        else:
            # Optional: print if nothing was found in a specific file
            # print(f"No object detected in file: {file_name}")
            pass

    print("\nDone! All results saved in 'runs/pose/predict'")

if __name__ == "__main__":
    main()