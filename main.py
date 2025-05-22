# main.py

import cv2
from ultralytics import YOLO
from distance import estimate_distance

# --- Khai báo thông số đã calibrate ---
FOCAL_LENGTH = 354  # Ví dụ: bạn tính được từ bước calibrate
REAL_HEIGHT_CM = 170  # Chiều cao thực tế (VD: người cao 1m70)

# Tải model YOLO
model = YOLO("yolov8n.pt")

# Mở camera (hoặc dùng file video)
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect đối tượng bằng YOLO
    results = model(frame)
    annotated_frame = results[0].plot()

    # Lặp qua từng bounding box
    for box in results[0].boxes.xyxy:
        x1, y1, x2, y2 = map(int, box)
        pixel_height = y2 - y1
        distance_cm = estimate_distance(FOCAL_LENGTH, REAL_HEIGHT_CM, pixel_height)

        # Hiển thị kết quả
        if distance_cm:
            cv2.putText(
                annotated_frame,
                f"{distance_cm:.1f} cm",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

    # Hiển thị khung hình
    cv2.imshow("YOLO + Distance", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
