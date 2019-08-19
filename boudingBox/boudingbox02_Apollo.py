#!/usr/bin/env python

import os
import cv2
import numpy as np

threshval = 100

imagePath = "object170927_070404283_Camera_5_bin.png"

image = cv2.imread(imagePath, 0) # cv2.IMREAD_GRAY)
# bw = threshval < 128 ? (img < threshval) : (img > threshval)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binary = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.namedWindow("binary", flags=cv2.WINDOW_NORMAL)
# while True:
#     cv2.imshow("binary", binary)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord("q"):
#         break
# getting mask with connectComponents
ret, labels = cv2.connectedComponents(binary, 8)

print(ret)
# print(labels)
# exit()

cv2.namedWindow("component", flags=cv2.WINDOW_NORMAL)

for label in labels:    #range(1,ret):
    mask = np.array(labels, dtype=np.uint8)
    mask[labels == label] = 255
    cv2.imshow('component',mask)
    cv2.waitKey(0)

exit()
# getting ROIs with findContours
contours = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
print(contours)
# exit()

cv2.namedWindow("ROI", flags=cv2.WINDOW_NORMAL)
for cnt in contours:
    (x,y,w,h) = cv2.boundingRect(cnt)
    ROI = image[y:y+h,x:x+w]
    cv2.imshow('ROI', ROI)
    cv2.waitKey(0)

cv2.destroyAllWindows()