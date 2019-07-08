#!/usr/bin/env python3
import cv2

def click_event(event, x, y, flags, depth):
    if event == cv2.EVENT_FLAG_LBUTTON:
        print("Deptp at ({}:{}) is {}".format(x, y, depth[y, x]/200.0))

depth_path = "/media/huynv/Data2/3D_SLAM/Front_end/2.CodeTest/170927_070404283_Camera_5.png"
depthImg = cv2.imread(depth_path, cv2.IMREAD_ANYDEPTH)
cv2.namedWindow("depth", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("depth", click_event, depthImg)
while True:
    cv2.imshow("depth", depthImg)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()