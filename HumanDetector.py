#Human detection with OpenCV and HOG
import cv2
import numpy as np
from utils import modifyImageSize

# Using HOGDescriptor with the DefaultPeopleDetector for the best results
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Capturing feed from webcam
wc_feed = cv2.VideoCapture(0)

isReading = True

# Continue analyzing feed images unless stopped
while isReading:

    # Convert the webcam feed into image, grab its dimensions, then resize the image to a smaller size
    # Smaller size images allow for faster and more accurate detection
    _,feed = wc_feed.read()
    (h, w) = feed.shape[:2]
    image = modifyImageSize(feed, 350, w, h)

    # Detect people
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)
    
    # Analyze the incoming dimensions and confidence weight and draw rectangles
    for (x, y, w, h) in rects:
        if weights[0][0] > 0.70:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display webcam feed with detections made
    cv2.imshow("Detection", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break