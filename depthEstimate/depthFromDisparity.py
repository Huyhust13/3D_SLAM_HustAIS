#!/usr/bin/env python
import os
import argparse
import cv2
import numpy as np
from log_yaml import *

parser = argparse.ArgumentParser(description="depthFromDisparity")
parser.add_argument("--image", help="path to disparity image")
args = parser.parse_args()

if not args.image:
    logger.error("Dont have disparity image. Please give disparity image path!")
    exit()

# Stereo camera parameters - Cityscape:
focal = 2262.52 #pixel
baseline = 0.209313 #met

def click_event(event, x, y, flags, (depth, dispMap)):
    if event == cv2.EVENT_FLAG_LBUTTON:
        logger.info("At ({}:{}): Disparity is {} - Depth is {}".format(x, y, (dispMap[y, x])/256, depth[y, x])) #(focal*baseline*200 / depth[y, x])))

def readDepth(disp_path):
    # dispMap = cv2.imread(disp_path, cv2.IMREAD_UNCHANGED).astype(np.float32)
    dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)#.astype(np.float32)
    # ap dung cong thuc, chuyen tu anh disp sang anh depth
    depthCal = lambda i: (float(focal*baseline)*256/ ((float(i)*2.))) if i else 0
    convert = np.vectorize(depthCal)
    depthMap = convert(dispMap)
    # depthMap = depthMap.astype(np.uint16)
    depthMap_gray = depthMap.astype(np.uint8)
    # depthMap_gray = depthMap

    logger.debug("type of disparity: {} - depth map: {}".format(type(dispMap[1][1]), type(depthMap[1][1])))
    logger.debug("Maximum value of disparity map: {}".format(np.amax(dispMap)))
    if depthMap is None:
        logger.error("[ERROR] Cannot load Image!")
        exit()     
    cv2.namedWindow("depth", cv2.WINDOW_NORMAL)
    cv2.namedWindow("disp", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("depth", click_event, (depthMap, dispMap))
    while True:
        cv2.imshow("disp", dispMap)
        cv2.imshow("depth", depthMap_gray)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    readDepth(args.image)