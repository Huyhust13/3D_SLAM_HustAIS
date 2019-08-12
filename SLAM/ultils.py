import os 
import os.path
import numpy as np
import json
import argparse
from log_yaml import *
import cv2

# Loc file theo duoi
def is_type_file(filename, EXTENSIONS):
    return any(filename.endswith(extension) for extension in EXTENSIONS)

def fileLoader(filepath, EXTENSIONS):
    files = [file for file in os.listdir(filepath) if is_type_file(file, EXTENSIONS)]
    files.sort()
    return files

def indexLoader(filepath, EXTENSIONS):
    files = [("_" + file.split('_')[1] + "_" + file.split("_")[2] + "_") for file in os.listdir(filepath) if is_type_file(file, EXTENSIONS)]
    files.sort()
    return files

# === Ham lay toa do pixel cua objects===
# Input:
#       - file *_gtFine_polygons.json
# Output:
#       - List toa do (x,y) cua nhieu diem tren moi object
#       - preLandmaks: [[xmin, ymin, xmax, ymax]...]
def getObjects(filePath):
    # load json file
    with open(filePath, 'r') as f:
        boundingboxs = json.load(f)

    landmark_labels = ['traffic sign','traffic light','pole']
    preLandmarks = []
    for i in range(len(boundingboxs["objects"])):
        # Toa do dinh hinh da giac cua objects:
        X = []
        Y = []
        for j in range(len(boundingboxs["objects"][i]["polygon"])):
            X.append(boundingboxs["objects"][i]['polygon'][j][0])
            Y.append(boundingboxs["objects"][i]['polygon'][j][1])
        
        xmax = max(X)
        ymax = max(Y)
        xmin = min(X)
        ymin = min(Y)
        label = str(boundingboxs["objects"][i]['label'])
        
        if ((label in landmark_labels) & (len(X)<6)):
            preLandmarks.append([xmin, ymin, xmax, ymax])
    return preLandmarks

# Thong so Stereo camera CityScapes
focal = 2262.52 #pixel
baseline = 0.209313 #met
# He so:
# scale_factor: su dung khi scale anh nho xuong de chay PSMNet
# depth_factor: su dung khi nhanh he so vao anh depth de hien thi
scale_factor = 2.0 
depth_factor = 1.0
# depth_threshold: neu depth tinh duoc lon hon depth_threshold thi bo qua vi thieu chinh xac 
depth_threshold = 30

# Ham lay depth trung binh cua nhieu diem xung quanh (x,y)
def averageValue(x, y, depth, numPx = 5):
    tmpSum = 0
    totalPx = 0
    for i in range(numPx):
        for j in range(numPx):
            if depth[y-numPx/2 + j][x-numPx/2 + i] != 0:
                tmpSum += depth[y-numPx/2 + j][x-numPx/2 + i]
                totalPx += 1    
    if tmpSum != 0:
        return float(tmpSum/totalPx)
    else:
        logger.warn("Not have depth infor")
        return 0

# Ham tinh Position:
def getPos(x, y, dispMap):
    disp = averageValue(x, y, dispMap)
    disp_i = float(disp)*scale_factor/256.0
    width = dispMap.shape[1]
    # depth:
    X = ((x - width/2) * baseline)/disp_i
    Z = (focal * baseline)/(disp_i)
    return X, Z


# Ham getLandmark Position
# IN: disparity map, preLandmark
# OUT: landmarks
def getLandmarks(dispMap, preLandmarks):
    subIndex = 1
    landmarks = []
    for landmark in preLandmarks:
        _x = int((landmark[0] + landmark[2])/(2*scale_factor)) 
        _y = int((landmark[1] + landmark[3])/(2*scale_factor)) 
        X, Z = getPos(_x, _y, dispMap)
        if Z < depth_threshold:
            landmarks.append([subIndex, X, Z])
            subIndex += 1
        
    return landmarks
            

    