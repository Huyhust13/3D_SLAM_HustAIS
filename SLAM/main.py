#!/usr/bin/env python

import os
import argparse
from ultils import *
from log_yaml import *

parser = argparse.ArgumentParser(description="graphBaseSLAM")
parser.add_argument("--dataset", help="path to dataset", default="/media/huynv/My Passport/1.3DVision/2.Data/cityscapes/")
parser.add_argument("--city", help="name of city route", default="aachen/")
args = parser.parse_args()

# Folder path to Left color Images
leftImg = args.dataset + "leftImg8bit_trainvaltest/leftImg8bit/train/" + args.city 
# Folder path to gtFine json files
gtFine = args.dataset + "gtFine_trainvaltest/gtFine/train/" + args.city 
# Folder path to disparity files
dispFolder = "../disparity/" + args.city
# Check input
logger.debug(leftImg)
logger.debug(gtFine)
logger.debug(dispFolder)

# ====== MAIN ===============================
# 1. Doc file gtFine .json de lay toa do diem
# 2. Tinh toa do landmark tu disparity va thong tin tai 1
#   2.1. Tinh depth: trung binh nhieu diem
#   2.1. Tinh X: Diem trung tam
if __name__ == "__main__":
    getDepthPoint(gtFine)
