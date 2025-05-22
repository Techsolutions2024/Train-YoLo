import cv2
import numpy as np
import glob

# Kích thước checkerboard (số góc trong checkerboard)
CHECKERBOARD = (9,6)

# Chuẩn bị điểm 3D trong thế giới thực, giả sử mỗi ô vuông 2.5 cm
square_size = 2.5  # cm

objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1],3), np.float32)
objp[:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1,2)
objp = objp * square_size  # nhân kích thước ô vuông

# Mảng để lưu điểm 3D và điểm 2D từ các ảnh
objpoints = []  # điểm 3D
imgpoints = []  # điểm 2D

# Đường dẫn ảnh chụp checkerboard (thay đổi theo nơi lưu ảnh)
images = glob.glob('calibration_images/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Tìm góc checkerboard
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        # Tinh chỉnh góc cho chính xác hơn
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imgpoints.append(corners2)

        # Vẽ góc ra ảnh để kiểm tra
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# Calibrate camera
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera matrix:\n", camera_matrix)
print("Distortion coefficients:\n", dist_coeffs)

# Lưu thông số calibrate
np.save("camera_matrix.npy", camera_matrix)
np.save("dist_coeffs.npy", dist_coeffs)
