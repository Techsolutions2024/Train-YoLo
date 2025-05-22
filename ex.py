import cv2

def get_focal_length(known_distance_cm, real_height_cm, pixel_height):
    return (pixel_height * known_distance_cm) / real_height_cm

def draw_rectangle(event, x, y, flags, param):
    global drawing, pt1, pt2
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        pt1 = (x, y)
        pt2 = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        pt2 = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        pt2 = (x, y)

# --- Thông số đã biết ---
KNOWN_DISTANCE_CM = 40  # Khoảng cách từ camera đến đối tượng (VD: 200 cm)
REAL_HEIGHT_CM = 20     # Chiều cao thực tế của đối tượng (VD: người 1m70)

drawing = False
pt1 = (0, 0)
pt2 = (0, 0)

cap = cv2.VideoCapture(1, cv2.CAP_MSMF)
cv2.namedWindow("Calibration")
cv2.setMouseCallback("Calibration", draw_rectangle)

print("👉 Hướng dẫn:")
print(" 1. Đặt vật thể cách camera đúng", KNOWN_DISTANCE_CM, "cm.")
print(" 2. Kẻ khung từ đỉnh đến đáy vật thể (VD: đầu -> chân).")
print(" 3. Nhấn 'c' để tính focal length.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    temp = frame.copy()
    if drawing:
        cv2.rectangle(temp, pt1, pt2, (0, 255, 255), 2)

    cv2.imshow("Calibration", temp)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("c"):
        y1 = min(pt1[1], pt2[1])
        y2 = max(pt1[1], pt2[1])
        pixel_height = y2 - y1
        if pixel_height <= 0:
            print("❌ Vui lòng chọn lại bounding box đúng.")
            continue
        focal_length = get_focal_length(KNOWN_DISTANCE_CM, REAL_HEIGHT_CM, pixel_height)
        print(f"✅ Chiều cao bbox: {pixel_height} px")
        print(f"✅ Focal length: {focal_length:.2f} px")
        break
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
