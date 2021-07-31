import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Initialize servo
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
p.start(2.5)

# Indicate whether first object has been dropped
firstFlag = False

# Indicate whether second object has been dropped
secondFlag = False


# Get video from default camera
cap = cv2.VideoCapture(0)


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
    
    # Check if circles found
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        try:
          while (not firstFlag or not secondFlag):
            if (not firstFlag):
              p.ChangeDutyCycle(10)
              firstFlag = True
              print("First Ball Dropped!")
              time.sleep(3) # Set according to requirement
              break
            if (firstFlag and not secondFlag):
              p.ChangeDutyCycle(5)
              secondFlag = True
              print("Second Ball Dropped!")
              time.sleep(3)
              break
        except KeyboardInterrupt:
            p.stop()
            GPIO.cleanup()
            
            if (firstFlag and secondFlag):
                break
            
if (firstFlag and secondFlag):
  cap.release()
  exit()
