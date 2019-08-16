#!/usr/bin/env python
import os
import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(description="get Objects")
parser.add_argument("--image", help="path to disparity image", default="170927_070404283_Camera_5_bin.png")
args = parser.parse_args()

if not args.image:
    print("Dont have disparity image. Please give disparity image path!")
    exit()

def readImg(imgPath):
    # dispMap = cv2.imread(disp_path, cv2.IMREAD_UNCHANGED).astype(np.float32)
    imgIn = cv2.imread(imgPath, 0)#.astype(np.float32)
    # ap dung cong thuc, chuyen tu anh disp sang anh depth
    ids = [65, 66, 81, 82, 83]
    objectFilter = lambda i: i if i in ids else 255
    convert = np.vectorize(objectFilter)
    imgOut = convert(imgIn)
    return imgOut

if __name__ == "__main__":
    img = readImg(args.image)
    cv2.namedWindow("objects", cv2.WINDOW_NORMAL)
    while True:
        # cv2.imshow("disp", dispMap)
        cv2.imshow("objects", img.astype(np.uint8)) #image = image.astype(np.uint8)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cv2.imwrite('object' + args.image, img) #*256.0
            break

