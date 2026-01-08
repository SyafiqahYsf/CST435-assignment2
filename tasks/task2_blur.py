import cv2

def apply(img):
    # Standard 3x3 Gaussian Blur
    return cv2.GaussianBlur(img, (3, 3), 0)
