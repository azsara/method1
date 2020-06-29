# -*- coding: utf-8 -*-
"""
Created on Thu May 25 02:07:14 2020
CSE 30 Spring 2020 Program 4 starter code
@author: Fahim
"""

import cv2
import numpy as np

cap = cv2.VideoCapture('sample1 (1).avi')
#cap = cv2.VideoCapture(0)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 1000:
            continue
        #cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame1, (x+33, y+85), 25, (0, 255, 255), 2)
        cv2.circle(frame1, (x+18, y +15), 25, (255, 0, 0), 2)
        cv2.putText(frame1, "Status: {}".format('People Moving'), (0, 25), cv2.FONT_HERSHEY_TRIPLEX,
                    1, (250, 0, 0), 3)
    cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (640,480))
    out.write(image)
    cv2.imshow("output", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()