# distance_estimator.py

def get_focal_length(known_distance_cm, real_height_cm, pixel_height):
    """
    Tính tiêu cự camera (focal length) dựa vào ảnh đo được
    """
    return (pixel_height * known_distance_cm) / real_height_cm


def estimate_distance(focal_length, real_height_cm, pixel_height):
    """
    Ước lượng khoảng cách từ camera đến vật thể
    """
    if pixel_height == 0:
        return None
    return (real_height_cm * focal_length) / pixel_height
