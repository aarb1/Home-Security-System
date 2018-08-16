import cv2
import numpy as np
import time
import constants
import email_sender as es
import os
import video_uploader
import threading
from helpers import modifyImageSize

# Holds Unix format time of the last time a notification email was sent out
lastEmailTime = 0
# Holds Unix format time of the last time a video recording was started upon detection
lastVideoStartTime = 0
# This flag when set to true, indicates that a video is currently being made
isSendingFrames = False
# Holds reference to the current cv2.VideoWriter object, used to record videos
video = None
# Loading the codec used for the videos
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Using HOGDescriptor with the DefaultPeopleDetector for the best results
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Capturing feed from webcam
wc_feed = cv2.VideoCapture(0)

isReading = True

out = None

# Continue analyzing feed images unless stopped
while isReading:

    # Convert the webcam feed into image, grab its dimensions, then resize the image to a smaller size
    # Smaller size images allow for faster and more accurate detection
    _,feed = wc_feed.read()

    image = modifyImageSize(feed, 350)

    # Detect people
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)
    
    currentTime = time.time()
        
    # Analyze the incoming dimensions and confidence weight and draw rectangles
    for (x, y, w, h) in rects:        
        if weights[0][0] > 0.70:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)            
            # If a human is detected, send a notification email, if the last email was sent atleast 
            # 5 minutes ago

            # If sufficient time has passed since the last notificaiton, then send another email            
            if currentTime - lastEmailTime > constants.EMAIL_COOLDOWN:
                lastEmailTime = currentTime              
                thread = threading.Thread(target=es.sendEmail, args=((image,)))
                thread.start()

            # If a detection has been made, and if a video is not being made, then create a video and start adding frames
            if not isSendingFrames:
                lastVideoStartTime = currentTime
                # If out is not referencing another VideoWriter, then create a new one 
                if (out is None):
                    videoName = 'videos/' + str(currentTime) + '.avi' 
                    out = cv2.VideoWriter(videoName, fourcc, 20, (350,262), isColor = True)                                
                    isSendingFrames = True
   
    # If a video is currently being made, continue adding frames to it
    if isSendingFrames:
        # Limiting the duration of the video
        if currentTime - lastVideoStartTime < constants.VIDEO_DURATION:
            out.write(image)
        else:
            # After the recording is done, release the VideoWriter
            out.release()
            # Reset the out variable, so that it can be attached to another VideoWriter later
            out = None
            thread = threading.Thread(target=video_uploader.uploadVideoToGoogleDrive, args=((videoName,)))
            thread.start()
            isSendingFrames = False         

    # Display webcam feed with detections made
    cv2.imshow("Detection", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

wc_feed.release()
cv2.destroyAllWindows()