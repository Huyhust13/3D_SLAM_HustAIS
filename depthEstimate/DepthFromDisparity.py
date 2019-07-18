#!/usr/bin/env python3
import cv2
import readDepth

disp_path = "/home/huyhv/1.Coding/3D_SLAM_HustAIS/depthEstimate/dataSets/berlin_000000_000019_disparity.png"

# Stereo camera parameters - Cityscape:
focal = 2262.52 #pixel
baseline = 0.209313 #met

dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)
print(dispMap[10,100])
exit()
# depthMap = new Mat(dispMap.shape[1], dispMap.shape[0])
for col in dispMap.shape[1]:
    for row in dispMap.shape[0]:
        depthMap[col, row] = focal*baseline/dispMap[col, row]




