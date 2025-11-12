from ultralytics import YOLO
import cv2

# Ścieżki
model_path = './runs/pose/train11/weights/last.pt'
image_path = './IMG_0254.jpeg'

# Wczytaj obraz
img = cv2.imread(image_path)

# Załaduj model YOLO-pose
model = YOLO(model_path)

# Wykonaj inferencję
results = model(image_path)[0]

# Iteruj po wykrytych obiektach
for det_idx, keypoints_tensor in enumerate(results.keypoints.xy):
    keypoints = keypoints_tensor.cpu().numpy()  # [4, 2] w Twoim przypadku
    for idx, (x, y) in enumerate(keypoints):
        # Rysuj punkt
        cv2.circle(img, (int(x), int(y)), 4, (0, 255, 0), -1)
        # Podpisz numer punktu
        cv2.putText(img, str(idx), (int(x) + 5, int(y) - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Pokaż obraz z naniesionymi punktami
cv2.imshow('YOLO Pose - Keypoints', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
