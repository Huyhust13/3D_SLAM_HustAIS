#!/usr/bin/env python
# run:
# ./compareDepthResult_KITTY.py --image ../data/KITTY/depth/color/Left/0000000009.png --depth1 ../data/KITTY/depth/depth/0000000009.png --depth2 depth/0000000009.png

import os
import argparse
import cv2
import numpy as np
from log_yaml import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

parser = argparse.ArgumentParser(description="depthFromDisparity")
parser.add_argument("--image", help="path to Left color image")
parser.add_argument("--depth1", help="path to depth KITTY dataset")
parser.add_argument("--depth2", help="path to depth from disparity PSMNet")
args = parser.parse_args()
filePath = "compare_depth.txt"
idx = 0

if not args.depth1 or not args.depth2 or not args.image:
    logger.error("Dont enough image!")
    exit()
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

def writeLine(filePath, idx, depth1, depth2):
    line = "{} {:.3f} {:.3f} {:.3f}\n".format(idx, depth1, depth2, depth2-depth1)
    with open(filePath, 'a') as f:
        f.write(line)
        
def click_event(event, x, y, flags, (color, depth1, depth2, idx, filePath)):
    if event == cv2.EVENT_FLAG_LBUTTON:
        d1 = averageDepth(x, y, depth1)
        d2 = averageDepth(x, y, depth2)
        if d1:
            idx += 1
            cv2.rectangle(color, (x-5, y-5), (x+5, y+5), (255,0,0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            pos = '({}:{})'.format(x, y)
            cv2.putText(color,pos,(x-5,y-5), font, 0.5,(255,0,0),2,cv2.LINE_AA)
            logger.info("At ({}:{}): Depth 1 is {:.2f} - Depth 2 is {:.2f} - disc = {:.2f}".format(x, y, d1, d2, d1-d2)) #(focal*baseline*200 / depth[y, x])))
            writeLine(filePath, idx, d1, d2)


def readDepth(disp_path, factor = 1.):
    dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)#.astype(np.float32)
    # depthMap = dispMap
    # ap dung cong thuc, chuyen tu anh disp sang anh depth
    depthMap = dispMap.astype('float32')
    return depthMap

if __name__ == "__main__":
    color = cv2.imread(args.image, cv2.IMREAD_COLOR)
    depth1 = readDepth(args.depth1)/256 # read depth from dataset
                                    # if read depth from KITTY lidar dataset then divide /256
    depth2 = readDepth(args.depth2) # read depth from disparity PSMNet

    # depthDisc = depth2/256.0 - depth1

    # logger.debug(type(depthDisc.shape[1]))
    # exit()

    cv2.namedWindow("Depth from dataset", flags=cv2.WINDOW_NORMAL)
    cv2.namedWindow("Depth from PSMNet", flags=cv2.WINDOW_NORMAL)
    cv2.namedWindow("Color", flags=cv2.WINDOW_NORMAL)

    cv2.setMouseCallback("Color", click_event, (color, depth1, depth2, idx, filePath))
    # cv2.setMouseCallback("Depth from dataset", click_event, (depth1, depth2))

    while True:
        cv2.imshow("Depth from dataset", depth1.astype('uint8'))# depthDisc.astype('uint8'))
        cv2.imshow("Depth from PSMNet", depth2.astype('uint8'))# depthDisc.astype('uint8'))
        cv2.imshow("Color", color)# depthDisc.astype('uint8'))
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break