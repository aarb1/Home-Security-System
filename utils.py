import cv2
import numpy as np

# Resize the image to a smaller size if possible
def modifyImageSize(image, standardWidth, imageWidth, imageHeight):
    width = min(standardWidth, imageWidth)
    ratio = width / imageWidth
    height = int(ratio * imageHeight)
    newImage = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return newImage