#!/usr/bin/env python

import os
import cv2
import numpy as np

threshval = 500

# imagePath = "test.png"
imagePath = "object170927_070404283_Camera_5_bin.png"

def writeMat2txt(file, mat):
    fs_write = cv2.FileStorage(file, cv2.FILE_STORAGE_WRITE)
    fs_write.write("floatdata", mat)
    fs_write.release()


image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE) #IMREAD_UNCHANGED) #GRAYSCALE)
# bw = threshval < 128 ? (img < threshval) : (img > threshval)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# binary = image
binary = cv2.threshold(image, -1, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

outputs = cv2.connectedComponentsWithStats(binary, 8, cv2.CV_32S)

num_labels, labelmap, stats, centers = outputs
colored = np.full((image.shape[0], image.shape[1], 3), 0, np.uint8)
for l in range(1, num_labels):
    # print(stats[l][4])
    if stats[l][4] > 50:
        colored[labelmap == l] = (0, 255*l/num_labels, 255*num_labels/l)
        cv2.circle(colored,
(int(centers[l][0]), int(centers[l][1])), 5, (255, 0, 0), cv2.FILLED)
image = cv2.cvtColor(binary*255, cv2.COLOR_GRAY2BGR)
# ret, labels = cv2.connectedComponents(binary, 8, cv2.CV_32S)

# print(ret)
# writeMat2txt("labels.txt", labels)

# cv2.namedWindow("component", flags=cv2.WINDOW_NORMAL)
cv2.namedWindow("image", flags=cv2.WINDOW_NORMAL)
while True:
    # cv2.imshow("binary", binary)
    cv2.imshow('image',np.hstack((image, colored)))
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
# getting mask with connectComponents

# exit()

# for label in range(1,ret): #labels: 
#     mask = np.array(labels, dtype=np.uint8)
#     mask[labels == label] = 255
#     cv2.imshow('component',mask)
#     cv2.waitKey(0)

# # exit()
# # getting ROIs with findContours
# contours = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
# print(contours)
# exit()

# cv2.namedWindow("ROI", flags=cv2.WINDOW_NORMAL)
# for cnt in contours:
#     (x,y,w,h) = cv2.boundingRect(cnt)
#     ROI = image[y:y+h,x:x+w]
#     cv2.imshow('ROI', ROI)
#     cv2.waitKey(0)

# cv2.destroyAllWindows()