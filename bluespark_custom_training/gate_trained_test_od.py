from ultralytics import YOLO
import os

def main():
    model_path = 'best1070.pt'
    
    # Check if the model file exists
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found.")
        return

    print(f"Loading model: {model_path}...")
    # Load the model (works correctly for both Pose and Detect models to get bounding boxes)
    model = YOLO(model_path)

    images_dir = "old_data/images/train_inverted_global"
    
    # Check if the directory exists
    if not os.path.exists(images_dir):
        print(f"Error: Directory '{images_dir}' not found.")
        return

    print(f"Starting Object Detection inference on: {images_dir}...")

    
    # Run inference
    # save=True: saves the images with drawn boxes to 'runs/detect/predict'
    # stream=True: processes images one by one (generator), better for memory usage
    results = model.predict(source=images_dir, save=True, stream=True, conf=0.5)

    # Process results loop (iterates through each image in the folder)
    for result in results:
        # Get the filename of the current image being processed
        file_name = os.path.basename(result.path)
        
        # CHANGE: We check 'result.boxes' instead of 'result.keypoints'
        # Check if result.boxes is not None and contains at least one detection
        if result.boxes is not None and len(result.boxes) > 0:
            
            print(f"\n--- Objects Detected in file: {file_name} ---")
            
            # Iterate through all detected bounding boxes
            for box in result.boxes:
                # Get bounding box coordinates: x1 (left), y1 (top), x2 (right), y2 (bottom)
                # .cpu().numpy() converts the tensor to a standard numpy array
                coords = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = coords
                
                # Get confidence score
                conf = box.conf[0].item()
                
                # Get Class ID (e.g., 0, 1)
                cls_id = int(box.cls[0].item())
                # Get Class Name (e.g., 'person', 'car') using the model's internal names map
                cls_name = model.names[cls_id]

                print(f" -> Class: {cls_name} (ID: {cls_id}) | Conf: {conf:.2f}")
                print(f"    Box: [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]")
                
        else:
            # Optional: logic for files where nothing was detected
            # print(f"No objects detected in file: {file_name}")
            pass

    print("\nDone! All results saved in 'runs/detect/predict' (or 'runs/pose/predict')")

if __name__ == "__main__":
    main()