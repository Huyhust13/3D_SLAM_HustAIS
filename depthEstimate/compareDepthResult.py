#!/usr/bin/env python
# run:
# ./compareDepthResult.py --image1 /media/huyhv/My\ Passport/1.3DVision/2.Data/cityscapesDataset/disparity\_trainvaltest/disparity/test/berlin/berlin_000002_000019_disparity.png --image2 ../PSMNet/disparity/tmp_1024x512/berlin_000002_000019_leftImg8bit.png

import os
import argparse
import cv2
import numpy as np
from log_yaml import *

parser = argparse.ArgumentParser(description="depthFromDisparity")
parser.add_argument("--image1", help="path to disparity image dataset")
parser.add_argument("--image2", help="path to disparity image PSMNet")
args = parser.parse_args()

if not args.image1 or not args.image2:
    logger.error("Dont have disparity image. Please give disparity image path!")
    exit()

# Stereo camera parameters - Cityscape:
focal = 2262.52 #pixel
baseline = 0.209313 #met

def click_event(event, x, y, flags, (depth1, depth2, diff)):
    if event == cv2.EVENT_FLAG_LBUTTON:
        logger.info("At ({}:{}): Depth 1 is {} - Depth 2 is {} - diff = {}".format(x, y, depth1[y, x], depth2[y, x], diff[y, x])) #(focal*baseline*200 / depth[y, x])))

def readDepth(disp_path, factor = 1.):
    dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)#.astype(np.float32)
    # ap dung cong thuc, chuyen tu anh disp sang anh depth
    depthCal = lambda i: (float(focal*baseline)*256/ ((float(i)*factor))) if i else 0
    convert = np.vectorize(depthCal)
    depthMap = convert(dispMap)
    depthMap = depthMap.astype('float32')
    return depthMap

def findSum(arr): 
  
    # inner map function applies inbuilt function   
    # sum on each row of matrix arr and returns  
    # list of sum of elements of each row 
    return sum(map(sum,arr))   
  
def averageDiff(diffMap):
    return findSum(diffMap)/(diffMap.shape[0]*diffMap.shape[1])
    logger.debug("shape diff map: {}-{}".format(diffMap.shape[1], diffMap.shape[0]))

if __name__ == "__main__":
    depth1 = readDepth(args.image1, factor=1) # read depth from dataset
    depth2 = readDepth(args.image2, factor=2) # read depth from result
    depth2 = cv2.resize(depth2, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
    depthDiff = depth2-depth1
    depthDiff_color = cv2.cvtColor(depthDiff, cv2.COLOR_GRAY2RGB)

    cv2.namedWindow("Depth 1", flags=cv2.WINDOW_NORMAL)
    cv2.namedWindow("Depth 2", flags=cv2.WINDOW_NORMAL)
    cv2.namedWindow("Depth Diff", flags=cv2.WINDOW_NORMAL)
    cv2.namedWindow("Depth Diff color", flags=cv2.WINDOW_NORMAL)
    
    cv2.setMouseCallback("Depth Diff", click_event, (depth1, depth2, depthDiff))

    logger.info("Depth 1: Depth from disparity that given by Cityscape dataset")
    logger.info("Depth 2: Depth from disparity that computed by PSMNet")
    logger.info("Depth Diff: different between two depth maps")
    logger.info("Average Diff = {}".format(averageDiff(depthDiff)))
    logger.info("Min Diff = {} - Max diff = {}".format(np.amin(depthDiff), np.amax(depthDiff)))

    while True:
        cv2.imshow("Depth 1", depth1.astype('uint8'))
        cv2.imshow("Depth 2", depth2.astype('uint8'))
        cv2.imshow("Depth Diff", depthDiff.astype('uint16'))
        cv2.imshow("Depth Diff color", depthDiff_color)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
