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

# Folder path to Left color Images
leftImgFolder = args.dataset + args.city + "/leftImg/"
# Folder path to gtFine json files
gtFine = args.dataset + args.city + "/gtFine/" 
# Folder path to disparity files
dispFolder = args.dataset + args.city + "/disparityPSMNet/" 
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

    try:
        leftImg = cv2.imread(leftImgPath, cv2.IMREAD_COLOR)
        dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)
    except:
        logger.error("Unexpected error:" + str(sys.exc_info()[0]))
        raise

    # get landmarks
    landmarks = getLandmarks(dispMap, preLandmarks)
    logger.debug("landmarks" + str(landmarks))
