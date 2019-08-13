#!/usr/bin/env python

import os
import argparse
import sys
from ultils import *
from log_yaml import *

parser = argparse.ArgumentParser(description="graphBaseSLAM")
parser.add_argument("--dataset", help="path to dataset", default="/media/huynv/My Passport/1.3DVision/2.Data/3DSlamData/")
parser.add_argument("--city", help="name of city route", default="aachen")
args = parser.parse_args()

# Path to left Img folder
leftImgFolder = args.dataset + args.city + "/leftImg/"
# Path to gtFine folder
gtFine = args.dataset + args.city + "/gtFine/" 
# Path to disparity PSMNet folder 
dispFolder = args.dataset + args.city + "/disparityPSMNet/" 
# Path to camera folder
camParamFolder = args.dataset + args.city + "/camera/" 

# Check input
logger.info(leftImgFolder)
logger.info(gtFine)
logger.info(dispFolder)

# ====== MAIN ===============================
# 1. Doc file gtFine .json de lay toa do diem
# 2. Tinh toa do landmark tu disparity va thong tin tai 1
#   2.1. Tinh depth: trung binh nhieu diem
#   2.1. Tinh X: Diem trung tam
if __name__ == "__main__":
    indexImgs = indexLoader(leftImgFolder, ['.png'])
    logger.debug("indexImgs: " + str(indexImgs))

    preLandmarks = getObjects(gtFine + args.city.split("_")[0] + indexImgs[0] + "gtFine_polygons.json" )
    logger.debug("preLandmarks: " + str(preLandmarks))

    # load left image:
    leftImgPath = leftImgFolder + args.city.split("_")[0] + indexImgs[0] + "leftImg8bit.png" 
    # load disparity 
    disp_path = dispFolder + args.city.split("_")[0] + indexImgs[0] + "leftImg8bit.png"
    # Load camera params 
    camParamsPath = camParamFolder + args.city.split("_")[0] + indexImgs[0] + "camera.json"
    
    try:
        leftImg = cv2.imread(leftImgPath, cv2.IMREAD_COLOR)
        dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)
    except:
        logger.error("Unexpected error:" + str(sys.exc_info()[0]))
        raise

    # Thong so Stereo camera CityScapes
    baseline, focal, x_ex, y_ex = getCameraParams(camParamsPath)
    # He so:
    # scale_factor: su dung khi scale anh nho xuong de chay PSMNet
    # depth_factor: su dung khi nhanh he so vao anh depth de hien thi
    scale_factor = 2.0 
    depth_factor = 1.0
    # depth_threshold: neu depth tinh duoc lon hon depth_threshold thi bo qua vi thieu chinh xac 
    depth_threshold = 30

    # get landmarks
    landmarks = getLandmarks(dispMap, preLandmarks, baseline, focal, depth_threshold, scale_factor)
    logger.debug("landmarks" + str(landmarks))
    
    landmarksPos = getLandmarksPos(landmarks, x_ex, y_ex)

    # Ve landmark len leftImage
    imgLandmarkCam = drawLandmarks(leftImg, landmarks)
    imgLandmarkVehicle = drawLandmarks(leftImg, landmarksPos)
    cv2.namedWindow("Landmark Camera", flags=cv2.WINDOW_NORMAL)
    cv2.namedWindow("Landmark Vehicle", flags=cv2.WINDOW_NORMAL)
    while True:
        cv2.imshow("Landmark Camera", imgLandmarkCam)
        cv2.imshow("Landmark Vehicle", imgLandmarkVehicle)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    imgOutName_Cam = ".log/landmarked/" + args.city.split("_")[0] + indexImgs[0] + "landmarked_Cam.png"
    imgOutName_Vehicle = ".log/landmarked/" + args.city.split("_")[0] + indexImgs[0] + "landmarked_Cam.png"
    cv2.imwrite(imgOutName_Cam, imgLandmarkCam)
    cv2.imwrite(imgOutName_Vehicle, imgLandmarkVehicle)