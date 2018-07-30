import constants
import smtplib
import cv2
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

message = "Anomaly detected"

def sendEmail(image):
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    msg = __constructEmail(image)
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(constants.EMAIL_ADDRESS, constants.EMAIL_PASSWORD)
        server.sendmail(constants.EMAIL_ADDRESS, constants.EMAIL_ADDRESS, msg.as_string())
    finally:
        server.quit()

def __constructEmail(image):
    msg = MIMEMultipart()
    msg['Subject'] = message
    msg['From'] = constants.EMAIL_ADDRESS
    msg['To'] = constants.EMAIL_ADDRESS
    try:
        imageName = 'image_' + str(time.time()) + '.png'
        cv2.imwrite('images/'+imageName, image)
        fp = open('images/' + imageName, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
    except:
        pass
    return msg