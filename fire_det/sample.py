import cv2
import numpy as np
import smtplib
import playsound
import threading


Fire_Reported = 0
Alarm_Status = False


def play_alarm():
	while True:
	    playsound.playsound('Alarm.mp3', True)


def send_mail_function():

    recipientEmail = "mannvishnoi100@gmail.com"
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("mannvishnoi_bca18_21@its.edu.in","Hindustan_Times")
        server.sendmail('mannvishnoi_bca18_21@its.edu.in', recipientEmail,
                        "Warning A Fire Accident has been reported at Mann's Place")
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
    	print(e)


video = cv2.VideoCapture("video.mov")

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, hsv, mask=mask)
    
    no_red = cv2.countNonZero(mask)

    if int(no_red) > 15000:
        Fire_Reported = Fire_Reported + 1

    cv2.imshow("output", output)

    if Fire_Reported >= 1:

    	if Alarm_Status == False:
		    threading.Thread(target=play_alarm).start()
    		Alarm_Status = True

    	if Email_Status == False:
		threading.Thread(target=send_mail_function).start()
    		Email_Status = True


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
