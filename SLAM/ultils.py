import os 
import os.path
import numpy as np
import json
import argparse
from log_yaml import *
import cv2
import math

#region load, file
# Loc file theo duoi
def is_type_file(filename, EXTENSIONS):
    return any(filename.endswith(extension) for extension in EXTENSIONS)

def fileLoader(filepath, EXTENSIONS):
    files = [file for file in os.listdir(filepath) if is_type_file(file, EXTENSIONS)]
    files.sort()
    return files

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

def indexLoader(filepath, EXTENSIONS):
    files = [("_" + file.split('_')[1] + "_" + file.split("_")[2] + "_") for file in os.listdir(filepath) if is_type_file(file, EXTENSIONS)]
    files.sort()
    return files
#endregion 

#region objects, landmarks
# === Ham lay toa do pixel cua objects===
# Input:
#       - file *_gtFine_polygons.json
# Output:
#       - List toa do (x,y) cua nhieu diem tren moi object
#       - preLandmaks: [[xmin, ymin, xmax, ymax]...]
def getObjects(filePath, landmark_labels, verticeMax):
    # load json file
    with open(filePath, 'r') as f:
        boundingboxs = json.load(f)
    
    objects = []
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
        
        if ((label in landmark_labels) & (len(X)<verticeMax)):
            objects.append([xmin, ymin, xmax, ymax])
    return objects

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
# OUT: landmarks = [[X, Z, [xmin, ymin, xmax,]]...]
def getLandmarks(dispMap, leftImg, objects, baseline, focal, depth_threshold=30, scale_factor = 2.0):
    landmarks = []
    for _object in objects:
        _x = int((_object[0] + _object[2])/(2*scale_factor)) 
        _y = int((_object[1] + _object[3])/(2*scale_factor))
        X, Z = getPos(_x, _y, dispMap, baseline, focal)
        landmarks.append([X, Z, _object])
    return landmarks
            
# Ham loc lay landmark tin cay
# IN: 
#   - landmarks 
#   - img: anh leftImg 
#   - restricedWidthFactor = n, he so gioi han. Vung gioi han tu imgWidth/n -> imgWidth *(n-1)/n
#   - depth_threshold: Gioi han neu depth tinh ra duoc lon hon depth_threshold thi bi loai bo
def landmark_filter(landmarks, img, restrictedWidthFactor = 20, depth_th = 25, area_th=100):
    landmarkFiltered = []
    n = restrictedWidthFactor
    imgWidth = img.shape[1]
    for landmark in landmarks:
        # Gioi han chieu sau
        depth = landmark[1]
        if depth > depth_th:
            continue
        # Gioi han hai ben theo phuong x
        xmax = landmark[2][2]
        xmin = landmark[2][0]
        if xmax < imgWidth/n or xmin > imgWidth*(n-1)/n:
            continue
        # Gioi han theo dien tich object
        _area = area(landmark[2])
        if _area < area_th:
            continue
        landmarkFiltered.append(landmark)
    cv2.line(img, (int(imgWidth/n), 0), (int(imgWidth/n), img.shape[0]), (255, 0, 0), 2)
    cv2.line(img, (int(imgWidth*(n-1)/n), 0), (int(imgWidth*(n-1)/n), img.shape[0]), (255, 0, 0), 2)
    return landmarkFiltered

def area(_object):
    xmin, ymin, xmax, ymax = _object
    return (xmax - xmin)*(ymax - ymin)

# Ham chuyen vi tri cua landmark doi voi odometry cua xe
def getLandmarksPos(landmarks, x_ex, y_ex):
    landmarksPos = []
    for landmark in landmarks:
        x_pv = landmark[1] + x_ex
        y_pv = landmark[0] + y_ex
        landmarksPos.append([x_pv, y_pv, landmark[2]])
    return landmarksPos
#endregion

#region draw
# --------- DRAW FUNCTION ------------------------
# Ham ve len anh cac thong tin can thiet de kiem tra
def drawLandmarks(imgIn, landmarks,textType = 'landmark'):
    # Ve landmark len leftImage
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Su dung ham .copy() de copy sang mot image moi de khong ve len anh goc
    imgOut = imgIn.copy()
    index = 0
    for landmark in landmarks:
        xmin = landmark[2][0]
        ymin = landmark[2][1]
        xmax = landmark[2][2]
        ymax = landmark[2][3]
        cv2.rectangle(imgOut, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        if(textType=='landmark'):
            cv2.putText(imgOut, "{} - [{:.2f} ; {:.2f}]".format(index, landmark[0], landmark[1]), (xmin+5,int((ymin+ymax)/2)), font, 1, (255,255,0), 2)
        elif(textType=='area'):
            cv2.putText(imgOut, "{}-areaPx:{:.2f}".format(index, area(landmark[2]), landmark[1]), (xmin+5,int((ymin+ymax)/2)), font, 1, (255,255,0), 2)
            cv2.putText(imgOut, "   D:{:.2f}".format(landmark[1]), (xmin+5,int((ymin+ymax)/2+30)), font, 1, (255,255,0), 2)
        index += 1
    return imgOut

# draw objects 
def drawObjects(imgIn, objects):
    # Ve objects len leftImage
    # Su dung ham .copy() de copy sang mot image moi de khong ve len anh goc
    imgOut = imgIn.copy()
    for _object in objects:
        xmin = _object[0]
        ymin = _object[1]
        xmax = _object[2]
        ymax = _object[3]
        cv2.rectangle(imgOut, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    return imgOut
#endregion