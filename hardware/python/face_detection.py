"""
This code uses open cv to analyze and process the frames received from the camera
"""

# import all the required modules
import numpy as np
import serial
import time
import sys
import cv2

# Set up communication with arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)
print("Connecting...")
time.sleep(2)
print("Connected to arduino")

# importing Haarcascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# capture video stream from the webcam
cap = cv2.VideoCapture(0)

# read the captured image, convert it to gray scale and find images
while 1:
    ret, img = cap.read()
    cv2.resizeWindow('img', 500, 500)
    cv2.line(img, (500, 250), (0, 250), (0, 255, 0), 1)
    cv2.line(img, (250, 0), (250, 500), (0, 255, 0), 1)
    cv2.circle(img, (250, 250), 5, (255, 255, 255), -1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3)

    # detect the face and make a rectangle around it
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 5)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        arr = {y:y+h, x:x+w}
        print(arr)

        print('X: ' + str(x))
        print('Y: ' + str(y))
        print('x+w: ' + str(x+w))
        print('y+h: ' + str(y+h))

        # center of image rectangle
        xx = int(x+(x+h))+2
        yy = int(y+(y+h))/2
        print(xx)
        print(yy)

        center = (xx, yy)

        # sending data to arduino
        print("Center of rectangle is: ", center)
        data = "X{0:d}Y{1:d}Z".format(xx, yy)
        print("Output = " + data + "")
        arduino.write(data)

        # display the stream
        cv2.imshow('img', img)

        # hit 'esc' to terminate execution
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break


