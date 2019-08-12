import os 
import os.path
import cv2 as cv
import numpy as np
import json
import argparse
from log_yaml import *

# Loc file theo duoi
def is_type_file(filename, EXTENSIONS):
    return any(filename.endswith(extension) for extension in EXTENSIONS)

def gtFineLoader(filepath):
    files = [file for file in os.listdir(filepath) if is_type_file(file, ['.json'])]
    files.sort()
    return files

# === Ham lay toa do object ===
# Input:
#       - file *_gtFine_polygons.json
# Output:
#       - List toa do (x,y) cua nhieu diem tren moi object
def getDepthPoint(filePath):
    gtFineFiles = gtFineLoader(filePath)

    logger.debug(gtFineFiles)


