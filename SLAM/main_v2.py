#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import argparse
import sys
import shutil
from ultils import *
from log_yaml import *
from g2o_ultils import * 

parser = argparse.ArgumentParser(description="graphBaseSLAM")
parser.add_argument("--dataset", help="path to dataset", default="/media/huynv/Data/14.ComputerVision/3.Data/3DSlamData/")
parser.add_argument("--city", help="name of city route", default="stuttgart_00")
parser.add_argument("--dataFolder", help="name of data folder", default="stuttgart_00")

args = parser.parse_args()

# Path to left Img folder
leftImgFolder = args.dataset + args.dataFolder + "/leftImg/"
# Path to gtFine folder
gtFine = args.dataset + args.dataFolder + "/gtFine/" 
# Path to disparity PSMNet folder 
dispFolder = args.dataset + args.dataFolder + "/disparityPSMNet/" 
# Path to camera folder
camParamFolder = args.dataset + args.dataFolder + "/camera/" 
# Path to vehicle folder
vehicleFoler = args.dataset + args.dataFolder + "/vehicle/" 
# Path to time stamp
timestampFolder = args.dataset + args.dataFolder + "/timestamp/" 

# Check input
logger.debug(leftImgFolder)
logger.debug(gtFine)
logger.debug(dispFolder)

# ====== MAIN ===============================
#TODO:
# 1. Doc file gtFine .json de lay toa do diem
# 2. Tinh toa do landmark tu disparity va thong tin tai 1
#   2.1. Tinh depth: trung binh nhieu diem
#   2.1. Tinh X: Diem trung tam
# 3. Ap dung bo loc
# 4. Xử lý landmark trùng 
# 5. Thay đổi cơ chế ghi file g2o
# 6. Lấy odom thật từ file vehicle và timestamp 
# =========================================
# FIXME: all 

if __name__ == "__main__":
    indexImgs = indexLoader_v2(leftImgFolder, ['.png'])
    logger.debug("indexImgs: " + str(indexImgs))
    # He so:
    # scale_factor: su dung khi scale anh nho xuong de chay PSMNet
    # depth_factor: su dung khi nhanh he so vao anh depth de hien thi
    scale_factor = 2.0 
    depth_factor = 1.0
    # depth_threshold: neu depth tinh duoc lon hon depth_threshold thi bo qua vi thieu chinh xac 
    depth_threshold = 30
    
    # Filter Params:
    _landmark_labels = ['traffic light','pole']  #'traffic sign',
    _score = 0.5
    _restrictedWidthFactor = 20
    _depth_th = 20
    _area_th = 0
    strParams = "Filter Params:\n\
        \t_landmark_labels: {}\n\
        \t_score: {}\n\
        \t_restrictedWidthFactor: {}\n\
        \t_depth_th: {}\n\
        \t_area_th: {}\n".format(_landmark_labels,_score,_restrictedWidthFactor, _depth_th, _area_th)
    logger.info(strParams)
    
    # Su dung cho file .g2o
    _id = 0
    poseInit = [0,0,0]
    rbPoseOld = [0,0,0]
    timeOld = 0
    landmarks_mem = []
    # bien luu thong tin landmarks o buoc truoc
    landmarks_cache = [] # [[{Xpv}, {Ypv}, {boundingbox[xmin, ymin, xmax, ymax]}, {g2o ID}],...]
    distance_th = 50
    # Gia dinh
    info_edgeXY = [1.58114, 0, 1.58114]
    info_edgeSE2 = [100, 0, 0, 500, 0, 500]
    
    vertexFilePath = "g2o/.vertexG2o.g2o"
    edgeFilePath = "g2o/.edgeG2o.g2o"
    g2oFilePath = "g2o/{}.g2o".format(args.dataFolder)
    if os.path.exists(vertexFilePath):
        os.rename(vertexFilePath, "g2o/.vertexG2o_old.g2o")
    if os.path.exists(edgeFilePath):
        os.rename(edgeFilePath, "g2o/.edgeG2o_old.g2o")
    if os.path.exists(g2oFilePath):
        os.rename(g2oFilePath, "g2o/.g2o_old.g2o")

    if not os.path.exists('.log'):
        os.makedirs('.log')
    if not os.path.exists('landmarked'):
        os.makedirs('landmarked')
    
    # dev  
    # for i in range(30): 
    for i in range(len(indexImgs)):
        logger.info(args.dataFolder + indexImgs[i])
        # load left image:
        leftImgPath = leftImgFolder + args.city + indexImgs[i] + "leftImg8bit.png" 
        # load disparity 
        disp_path = dispFolder + args.city + indexImgs[i] + "leftImg8bit.png"
        # Load camera params 
        camParamsPath = camParamFolder + args.city + indexImgs[i] + "camera.json"
        # vehicle file path
        vehiclePath = vehicleFoler + args.city + indexImgs[i] + "vehicle.json"
        # timestamp file path
        timestampPath = timestampFolder + args.city + indexImgs[i] + "timestamp.txt"
        # Thong so Stereo camera CityScapes
        baseline, focal, x_ex, y_ex = getCameraParams(camParamsPath)
        
        try:
            leftImg = cv2.imread(leftImgPath, cv2.IMREAD_COLOR)
            dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)
        except:
            logger.error("Unexpected error:" + str(sys.exc_info()[0]))
            raise

        #FIXME:
        # Lấy tọa độ các object từ file kết quả của yolo deep learning
        # Lọc object ("traffic light", "pole"), lọc score nhận dạng 
        objects = getObjectsYOLO(gtFine + args.city + indexImgs[i] + "detected.json", _landmark_labels, _score )
        logger.debug("\nobjects: " + str(objects))

        # get landmarks possition to Camera
        landmarks = getLandmarks(dispMap, leftImg, objects, baseline, focal, depth_threshold, scale_factor)
        logger.debug("\nlandmarks" + str(landmarks))
        # Apply Filter
        landmarkFiltered = landmark_filter(landmarks,leftImg, _restrictedWidthFactor, _depth_th, _area_th)

        # Convert to Vehicel coordinate
        landmarkVehicles = cvtLandmarksVehicle(landmarkFiltered, x_ex, y_ex)
        logger.debug("\nlandmark2Vehicles" + str(landmarkVehicles))

        # ===== ghi vao file *.g20 ==============
        # x_pv, y_pv = landmarkVehicles[0:2]
        if i==0:
            rbPose = [0,0,0]
            rbPoseOld = rbPose
            writeVertex(vertexFilePath, "VERTEX_SE2", _id, rbPose)
            id_pose = _id
            _id += 1
            for landmark in landmarkVehicles:
                # add landmark kèm id vào cache 
                temp = landmark.append(_id)
                landmarks_cache.append(temp)
                measure_ = landmark[0:2]
                landmark_estimate = transform(rbPose, landmark)
                writeVertex(vertexFilePath, "VERTEX_XY", _id, landmark_estimate)
                writeEdge(edgeFilePath, "EDGE_SE2_XY", id_pose, _id, measure_, info_edgeXY)
                _id += 1
        else:
            timeStep = getTimeStep(timestampPath, timeOld)
            timeOld += timeStep
            rbPose = speed2odom(vehiclePath, timeStep, rbPoseOld)
            writeVertex(vertexFilePath, "VERTEX_SE2", _id, rbPose)
            measure_ = disc2pose(rbPose, rbPoseOld)
            rbPoseOld = rbPose
            writeEdge(edgeFilePath, "EDGE_SE2", id_pose, _id, measure_, info_edgeSE2)
            id_pose = _id
            _id += 1            
            cache_tmp = []
            for landmark in landmarkVehicles:
                measure_ = landmark[0:2]
                # x_pv, y_pv = measure_                
                idOldLandmard = checkLandmark(landmark, landmarks_cache, distance_th)
                if idOldLandmard:
                    writeEdge(edgeFilePath, "EDGE_SE2_XY", id_pose, idOldLandmard, measure_, info_edgeXY)
                    # add landmark kèm id vào cache 
                    landmark.append(idOldLandmard)
                    cache_tmp.append(landmark)
                else:
                    landmark_estimate = transform(rbPose, landmark)
                    writeVertex(vertexFilePath, "VERTEX_XY", _id, landmark_estimate)
                    writeEdge(edgeFilePath, "EDGE_SE2_XY", id_pose, _id, measure_, info_edgeXY)
                    # add landmark kèm id vào cache 
                    landmark.append(_id)
                    cache_tmp.append(landmark)
                    _id += 1
            landmarks_cache = cache_tmp
            logger.debug("landmarks_cache: {}".format(landmarks_cache))
        # Ve landmark len leftImage
        # imgLandmarkCam = drawLandmarks(leftImg, landmarks, textType='landmark')
        imgLandmarkVehicle = drawLandmarks(leftImg, landmarkVehicles)
        # imgObjects = drawObjects(leftImg, objects)
        
        # Show hinh anh. ()
        showImgs = 0
        if showImgs:
            cv2.namedWindow("Landmark Camera", flags=cv2.WINDOW_NORMAL)
            cv2.namedWindow("Landmark Vehicle", flags=cv2.WINDOW_NORMAL)
            while True:
                # cv2.imshow("Landmark Camera", imgLandmarkCam)
                cv2.imshow("Landmark Vehicle", imgLandmarkVehicle)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

        # Luu anh
        # imgOutName_Obj = ".log/landmarked/" + args.city + indexImgs[i] + "objects.png"
        # imgOutName_Cam = "landmarked/" + args.dataFolder + indexImgs[i] + "landmarked_Cam.png"
        imgOutName_Vehicle = "landmarked/" + args.dataFolder + indexImgs[i] + "landmarked_Vehicle.png"
        # cv2.imwrite(imgOutName_Obj, imgObjects)
        # cv2.imwrite(imgOutName_Cam, imgLandmarkCam)
        cv2.imwrite(imgOutName_Vehicle, imgLandmarkVehicle)

    jointFile(g2oFilePath, vertexFilePath, edgeFilePath)