#!/usr/bin/env python3
import cv2
import numpy as np

# Stereo camera parameters - Cityscape:
focal = 2262.52 #pixel
baseline = 0.209313 #met

def click_event(event, x, y, flags, depth):
    if event == cv2.EVENT_FLAG_LBUTTON:
        print("Deptp at ({}:{}) is {}".format(x, y, depth[y, x])) #(focal*baseline*200 / depth[y, x])))

def readDepth(disp_path):
    dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)
    depthCal = lambda i: (float(focal*baseline)/ float(i)) if i else 0
    a = np.vectorize(depthCal)
    depthMap = a(dispMap)
    depthMap_gray = depthMap.astype(np.uint8)
    # depthMap_gray = depthMap*2000

    # depthMap = map(depthCal, dispMap)
    print(type(dispMap))
    print(type(depthMap))
    print(np.amax(dispMap))
    print(np.amax(depthMap))
    print(np.amin(depthMap))
    # exit()
    if depthMap is None:
        print("[ERROR] Cannot load Image!")
        exit()     
    cv2.namedWindow("depth", cv2.WINDOW_NORMAL)
    cv2.namedWindow("disp", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("depth", click_event, depthMap)
    while True:
        cv2.imshow("disp", dispMap)
        cv2.imshow("depth", depthMap_gray)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    depth_path = "./dataSets/000000_10.png"
    readDepth(depth_path)