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

    landmark_labels = ['traffic light','pole']  #'traffic sign',
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
def getPos(x, y, dispMap, baseline, focal, scale_factor=2.0):
    disp = averageValue(x, y, dispMap)
    disp_i = float(disp)*scale_factor/256.0
    width = dispMap.shape[1]
    # depth:
    X = ((x - width/2) * baseline)/disp_i
    Z = (focal * baseline)/(disp_i)
    return X, Z


# Ham getLandmark Position
# IN: disparity map, preLandmark
# OUT: landmarks = [[subindex, X, Z]...]
def getLandmarks(dispMap, preLandmarks, baseline, focal, depth_threshold=30, scale_factor = 2.0):
    subIndex = 1
    landmarks = []
    for landmark in preLandmarks:
        _x = int((landmark[0] + landmark[2])/(2*scale_factor)) 
        _y = int((landmark[1] + landmark[3])/(2*scale_factor))
        n = 200
        restricted_width = dispMap.shape[1]*scale_factor/n 
        if _x < restricted_width or _x > restricted_width*(n-1):
            continue
        X, Z = getPos(_x, _y, dispMap, baseline, focal)
        if Z < depth_threshold:
            landmarks.append([subIndex, X, Z, landmark])
            subIndex += 1
        
    return landmarks
            
    # Ham lay thong tin camera 
def getCameraParams(fileJson):
    # load json file
    with open(fileJson, 'r') as f:
        params = json.load(f)
    
    baseline = params["extrinsic"]["baseline"]
    focal = params["intrinsic"]["fx"]
    x_ex = params["extrinsic"]["x"]
    y_ex = params["extrinsic"]["y"]

    return baseline, focal, x_ex, y_ex

# Ham chuyen vi tri cua landmark doi voi odometry cua xe
def getLandmarksPos(landmarks, x_ex, y_ex):
    landmarksPos = []
    for landmark in landmarks:
        x_pv = landmark[2] + x_ex
        y_pv = landmark[1] + y_ex
        landmarksPos.append([landmark[0], x_pv, y_pv, landmark[3]])
    return landmarksPos


# Ham ve len anh cac thong tin can thiet de kiem tra
def drawLandmarks(imgIn, landmarks):
    # Ve landmark len leftImage
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Su dung ham .copy() de copy sang mot image moi de khong ve len anh goc
    imgOut = imgIn.copy()
    for landmark in landmarks:
        xmin = landmark[3][0]
        ymin = landmark[3][1]
        xmax = landmark[3][2]
        ymax = landmark[3][3]
        cv2.rectangle(imgOut, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(imgOut, "{} - [{:.2f} ; {:.2f}]".format(landmark[0], landmark[1], landmark[2]), (xmin+5,int((ymin+ymax)/2)), font, 1, (255,255,0), 2) 
    return imgOut