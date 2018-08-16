Home security system built with Python. Goal is to report any human activity when the system is running.

The human detection is carried out using Histogram of Gradients and Support Vector Machine.

The program utilizes OpenCV and a webcam (in-built or external) to continuously monitor a given space. The program is not affected by random motions, for example pets moving around the space or ceiling fans.

If a human(s) is detected in the webcam feed, the program sends a notification email along with the image of the anomaly and along with this, it records clips from the webcam feed and uploads the videos to google drive.

The notifcation email has a cooldown, so once a detection is made and email is sent, the next email is sent after a certain amount of time to avoid spamming emails. This time can be modified in the constants.py file.

The video clips are recorded for a certain amount of time and uploaded as soon as the recording is done. If the human(s) are still in the frame, the next recording is started immediately. The recording time for these clips can be modified in the constants.py file.

This program was made with windows systems on mind.

Steps to run the program:
1) Clone or Download this repository.
2) Modify the constants.py file with a gmail email id and password (I recommend making a new one just for this programs purpose.)
3) Enable the Google Drive API, create a new project and acquire the credentials json file and place it in the program along with the other py files.
4) The program is started with `python human_detector.py`. Some dependencies may have to be downloaded.
5) The program will require authentication for Google Drive, which will occur when the program is run for the first time and a detection is made. A new browser window will open and will require login into the google account that is being used for the program. Once this is done, a storage.json file will be created which will hold some authentication data.

After this, the program should be good to use. Once the program is started the PC can be locked, to ensure the PC is secured.
