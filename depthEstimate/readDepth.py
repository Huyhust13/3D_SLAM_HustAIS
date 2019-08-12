#!/usr/bin/env python
import cv2
import argparse

parser = argparse.ArgumentParser(description="read depth image")
parser.add_argument("--image", help="Path to depth image")
args = parser.parse_args()

def click_event(event, x, y, flags, depth):
    if event == cv2.EVENT_FLAG_LBUTTON:
        print("Deptp at ({}:{}) is {}".format(x, y, float(depth[y, x]))) #/256.0 
        # print(type(depth[x,y]/200))


def readDepth(depth_path):
    depthImg = cv2.imread(depth_path, cv2.IMREAD_ANYDEPTH)
    # print(type(depthImg))
    # print(depthImg)
    # exit()
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
    depth_path = args.image
    # depth_path = "./dataSets/berlin_000000_000019_disparity.png"
    readDepth(depth_path)
