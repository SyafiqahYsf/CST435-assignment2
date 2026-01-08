import cv2

def apply(img):
    # alpha=1.0 (contrast), beta=30 (brightness)
    return cv2.convertScaleAbs(img, alpha=1.0, beta=30)
