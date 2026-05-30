import cv2

def detect_rotten_area(input_path, output_path):
    img = cv2.imread(input_path)

    # Dummy rotten area (random box)
    h, w, _ = img.shape

    x = int(w * 0.3)
    y = int(h * 0.3)
    box_w = int(w * 0.3)
    box_h = int(h * 0.3)

    # Draw red box
    cv2.rectangle(img, (x, y), (x+box_w, y+box_h), (0, 0, 255), 2)

    # Label
    cv2.putText(img, "Rotten Area", (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    cv2.imwrite(output_path, img)