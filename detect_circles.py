import cv2
import numpy as np

#Comments with * represent code for color detection
#which is not currently being implemented


# Get video from default camera
cap = cv2.VideoCapture(0)

# To detect black area *
boundaries = [
    [0, 0, 0], [20, 20, 20]
]
lower = np.array(boundaries[0], dtype="uint8")
upper = np.array(boundaries[1], dtype="uint8")



while True:
    success, img = cap.read()
    copy = img.copy()
    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 5)
    gray = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3.5)
    kernel = np.ones((3,3), np.uint8)
    gray = cv2.erode(gray, kernel, iterations=1)
    gray = cv2.dilate(gray, kernel, iterations=1)

    # Detect circles using Hough Transform
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100, minRadius=0)

    # Applies a mask to find specific color *
    mask = cv2.inRange(copy, lower, upper)
    output = cv2.bitwise_and(copy, copy, mask = mask)
    
    # Draws circle
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            cv2.circle(copy, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(copy, (x - 5, y- 5), (x + 5, y + 5), (0, 128, 255), -1)

    cv2.imshow("Output", copy)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    