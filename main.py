import cv2 
import numpy as np

# Set dimensions for the onscreen video
frameWidth = 640
frameHeight = 480


cap = cv2.VideoCapture(0) #acquire video from webcam 

# Set camera parameters
cap.set(3, frameWidth)
cap.set(4, frameHeight)


#Empty function for trackbar
def nothing(a):
    pass

#Create trackbars to acquire thresholds
cv2.namedWindow("Threshold Parameters")
cv2.resizeWindow("Threshold Parameters", 640, 240)
cv2.createTrackbar("Threshold 1" , "Parameters", 20, 255, nothing)
cv2.createTrackbar("Threshold 2", "Parameters", 85, 255, nothing)

#Find contours and area and draw them 
def makeContours(img, imgContour):
    contours, hierarcy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:
            cv2.drawContours(imgContour, contour, -1, (255, 0, 255), 7)
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y+ 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0) , 2)
            
while True: 
    success, img = cap.read() #Acquire each frame
    imgContour = img.copy() #Draw contours on this copy

    imgBlur = cv2.GaussianBlur(img, (7, 7), 1) #Add gaussian blur to the frame
    imgGrey = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY) #Convert frame to greyscale

    #Provide 2 thresholds for canny edge detections
    threshold1 = cv2.getTrackbarPos("Threshold 1", "Threshold Parameters") 
    threshold2 = cv2.getTrackbarPos("Threshold 2", "Threshold Parameters")

    
    imgCanny = cv2.Canny(imgGrey, threshold1, threshold2) #Canny edge detection

    #Dilate frame using a 5x5 kernel
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    makeContours(imgDil, imgContour) #Draw contours

    cv2.imshow("Result", imgContour) #Output window

    #Quit options
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break
