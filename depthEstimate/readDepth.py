#!/usr/bin/env python3
import cv2

# Stereo camera parameters - Cityscape:
focal = 2262.52 #pixel
baseline = 0.209313 #met

def click_event(event, x, y, flags, depth):
    if event == cv2.EVENT_FLAG_LBUTTON:
        print("Deptp at ({}:{}) is {}".format(x, y, (focal*baseline*200 / depth[y, x])))

# depth_path = "/media/huynv/Data/14.ComputerVision/ApolloDataset/Depth/Record021/Camera 5/170927_070404283_Camera_5.png"

def readDepth(depth_path):
    depthImg = cv2.imread(depth_path, cv2.IMREAD_ANYDEPTH)
    if depthImg is None:
        print("[ERROR] Cannot load Image!")
        exit()     
    cv2.namedWindow("depth", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("depth", click_event, depthImg)
    while True:
        cv2.imshow("depth", depthImg)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    depth_path = "./dataSets/berlin_000000_000019_disparity.png"
    readDepth(depth_path)
