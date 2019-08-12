#!/usr/bin/env python
import os
import argparse
import cv2
import numpy as np
from log_yaml import *

#usage: 
# ./objectPosFromDisparity.py --disp ../PSMNet/disparity/tmp_1024x512/berlin_000000_000019_leftImg8bit.png --leftColor ../data/CityScapes/Berlin/Left/berlin_000000_000019_leftImg8bit.png 

parser = argparse.ArgumentParser(description="depthFromDisparity")
parser.add_argument("--dataset", default="CityScapes", help="Dataset used (CityScapes, KITTY)")
parser.add_argument("--disp", help="path to disparity image")
parser.add_argument("--leftColor", help="path to Left color image")
args = parser.parse_args()

if not args.disp or not args.leftColor:
    logger.error("Dont enough images. Please give disparity and Left color images path!")
    exit()

# Cac thong so:
if args.dataset == "CityScapes":
    # Stereo camera parameters - Cityscape:
    focal = 2262.52 #pixel
    baseline = 0.209313 #met
elif args.dataset == "KITTY":
    # KITTY
    focal = 721
    baseline = 0.54

# He so:
# scale_factor: su dung khi scale anh nho xuong de chay PSMNet
# depth_factor: su dung khi nhanh he so vao anh depth de hien thi
scale_factor = 2.0 
depth_factor = 1.0
# depth_max: neu depth tinh duoc lon hon depth_max thi bo qua vi thieu chinh xac 
depth_max = 30

def averageDepth(x, y, depth, numPx = 7):
    tmpSum = 0
    totalPx = 0
    for i in range(numPx):
        for j in range(numPx):
            if depth[y-numPx/2 + j][x-numPx/2 + i] != 0:
                tmpSum += depth[y-numPx/2 + j][x-numPx/2 + i]
                totalPx += 1    
    if tmpSum != 0:
        return float(tmpSum/totalPx)
    else:
        logger.warn("Not have depth infor")
        return 0

# Ham tinh Position:
def readPos(x, y, dispMap):
    disp = averageDepth(x, y, dispMap)
    disp_i = float(disp)*scale_factor/256.0
    width = dispMap.shape[1]
    # depth:
    X = ((x - width/2) * baseline)/disp_i
    Z = (focal * baseline)/(disp_i)
    
    return X, Z

# Ham doc file anh disparity
def readDisp(disp_path):
    dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)
    if dispMap is None:
        logger.error("[ERROR] Cannot load Image!")
        exit()     
    return dispMap
        
def click_event(event, x, y, flags, dispMap):
    if event == cv2.EVENT_FLAG_LBUTTON:
        x_ = int(x/scale_factor)
        y_ = int(y/scale_factor)
        # logger.debug(x_)
        X, Z = readPos(x_, y_, dispMap)
        logger.info("At ({}:{}): Depth = {:.2f} - X = {:.2f}".format(x, y, Z, X)) 
    

if __name__ == "__main__":
    dispMap = readDisp(args.disp)
    leftImage = cv2.imread(args.leftColor, cv2.IMREAD_COLOR)

    cv2.namedWindow("Disparity", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Left Image", cv2.WINDOW_NORMAL)

    cv2.setMouseCallback("Left Image", click_event, dispMap)
    while True:
        cv2.imshow("Disparity", dispMap)
        cv2.imshow("Left Image", leftImage)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()