import cv2
import numpy as np

def detect_all(image_path):
    img = cv2.imread(image_path)
    output = img.copy()

    # ---------- RIPENESS (COLOR BASED) ----------
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Yellow = ripe
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Green = unripe
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    yellow_ratio = np.sum(yellow_mask) / (img.shape[0] * img.shape[1])
    green_ratio = np.sum(green_mask) / (img.shape[0] * img.shape[1])

    if yellow_ratio > 0.3:
        ripeness = "Ripe 🟡"
    elif green_ratio > 0.3:
        ripeness = "Unripe 🟢"
    else:
        ripeness = "Overripe 🔴"

    # ---------- ROTTEN DETECTION (DARK SPOTS) ----------
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # dark area threshold
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # filter small noise
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(output, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # save result
    output_path = "static/results/output.jpg"
    cv2.imwrite(output_path, output)

    return ripeness, output_path