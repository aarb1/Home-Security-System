import constants
import smtplib
import cv2
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

message = "Anomaly detected"

def sendEmail(image):
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Create an email with an attached image of the detectection event
    msg = __constructEmail(image)
    # Initiate connection to email service, login and send the email
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(constants.EMAIL_ADDRESS, constants.EMAIL_PASSWORD)
        server.sendmail(constants.EMAIL_ADDRESS, constants.EMAIL_ADDRESS, msg.as_string())
    except:
        print('An error while sending email')
        pass
    finally:
        server.quit()

def __constructEmail(image):
    msg = MIMEMultipart()
    msg['Subject'] = message
    msg['From'] = constants.EMAIL_ADDRESS
    msg['To'] = constants.EMAIL_ADDRESS
    try:
        # Attach the correct image, image name is based on time of capture
        imageName = 'image_' + str(time.time()) + '.png'
        cv2.imwrite('images/'+imageName, image)
        fp = open('images/' + imageName, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
    except:
        print('An error while creating email')
        pass
    return msg