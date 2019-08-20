#!/usr/bin/env python

import os
import os.path
import argparse
import sys

from ultils import *
from log_yaml import *
from g2o_ultils import * 

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
# Path to vehicle folder
vehicleFoler = args.dataset + args.city + "/vehicle/" 

# Check input
logger.debug(leftImgFolder)
logger.debug(gtFine)
logger.debug(dispFolder)

# ====== MAIN ===============================
# 1. Doc file gtFine .json de lay toa do diem
# 2. Tinh toa do landmark tu disparity va thong tin tai 1
#   2.1. Tinh depth: trung binh nhieu diem
#   2.1. Tinh X: Diem trung tam
if __name__ == "__main__":
    indexImgs = indexLoader(leftImgFolder, ['.png'])
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
    _verticeMax = 8
    _restrictedWidthFactor = 20
    _depth_th = 30
    _area_th = 500
    strParams = "Filter Params:\n\
        \t_landmark_labels: {}\n\
        \t_verticeMax: {}\n\
        \t_restrictedWidthFactor: {}\n\
        \t_depth_th: {}\n\
        \t_area_th: {}\n".format(_landmark_labels,_verticeMax,_restrictedWidthFactor, _depth_th, _area_th)
    logger.info(strParams)
    # id su dung cho file .g2o
    _id = 0
    poseInit = [0,0,0]
    rbPoseOld = [0,0,0]
    # Gia dinh
    info_edgeXY = [1.58114, 0, 1.58114]
    info_edgeSE2 = [100, 0, 0, 500, 0, 500]

    vertexFilePath = "g2o/.vertexG2o.g2o"
    edgeFilePath = "g2o/.edgeG2o.g2o"
    g2oFilePath = "g2o/{}.g2o".format(args.city)
    if os.path.exists(vertexFilePath):
        os.rename(vertexFilePath, "g2o/.vertexG2o_old.g2o")
    if os.path.exists(edgeFilePath):
        os.rename(edgeFilePath, "g2o/.edgeG2o_old.g2o")
    if os.path.exists(g2oFilePath):
        os.rename(g2oFilePath, "g2o/.g2o_old.g2o")

    for i in range(len(indexImgs)):
        logger.info(args.city + indexImgs[i])
        # load left image:
        leftImgPath = leftImgFolder + args.city.split("_")[0] + indexImgs[i] + "leftImg8bit.png" 
        # load disparity 
        disp_path = dispFolder + args.city.split("_")[0] + indexImgs[i] + "leftImg8bit.png"
        # Load camera params 
        camParamsPath = camParamFolder + args.city.split("_")[0] + indexImgs[i] + "camera.json"
        # vehicle file path
        vehiclePath = vehicleFoler + args.city.split("_")[0] + indexImgs[i] + "vehicle.json"

        # Thong so Stereo camera CityScapes
        baseline, focal, x_ex, y_ex = getCameraParams(camParamsPath)
        
        try:
            leftImg = cv2.imread(leftImgPath, cv2.IMREAD_COLOR)
            dispMap = cv2.imread(disp_path, cv2.IMREAD_ANYDEPTH)
        except:
            logger.error("Unexpected error:" + str(sys.exc_info()[0]))
            raise

        # objects = getObjects(gtFine + args.city.split("_")[0] + indexImgs[i] + "gtFine_polygons.json", _landmark_labels, _verticeMax )
        objects = getObjectsYOLO(gtFine + args.city.split("_")[0] + indexImgs[i] + "gtFine_polygons.json", _landmark_labels, _verticeMax )
        logger.debug("\nobjects: " + str(objects))

        # get landmarks possition to Camera
        landmarks = getLandmarks(dispMap, leftImg, objects, baseline, focal, depth_threshold, scale_factor)
        logger.debug("\nlandmarks" + str(landmarks))
        # Apply Filter
        landmarkFiltered = landmark_filter(landmarks,leftImg, _restrictedWidthFactor, _depth_th, _area_th)

        # Convert to Vehicel coordinate
        landmarksPos = getLandmarksPos(landmarkFiltered, x_ex, y_ex)
        logger.debug("\nlandmarksPos" + str(landmarksPos))

        # ===== ghi vao file *.g20 ==============
        # x_pv, y_pv = landmarksPos[0:2]

        # Toa do gps tuyet doi cua vi tri dau tien
        if i==0:
            poseInit = getRobotPoseGPS(vehiclePath)
            rbPose = [0,0,0]
            rbPoseOld = rbPose
            writeVertex(vertexFilePath, "VERTEX_SE2", _id, rbPose)
            id_pose = _id
            _id += 1
            for landmark in landmarksPos:
                x_pv, y_pv = landmark[0:2]
                measure_ = landmark[0:2]
                x_po = rbPose[0] + x_pv*math.cos(rbPose[2])
                y_po = rbPose[2] + y_pv*math.cos(rbPose[2])
                landmark_estimate = [x_po, y_po]
                writeVertex(vertexFilePath, "VERTEX_XY", _id, landmark_estimate)
                writeEdge(edgeFilePath, "EDGE_SE2_XY", id_pose, _id, measure_, info_edgeXY)
                _id += 1
        else:
            rbPose = odomFromGPS(getRobotPoseGPS(vehiclePath), poseInit)
            writeVertex(vertexFilePath, "VERTEX_SE2", _id, rbPose)
            measure_ = disc2pose(rbPose, rbPoseOld)
            rbPoseOld = rbPose
            writeEdge(edgeFilePath, "EDGE_SE2", id_pose, _id, measure_, info_edgeSE2)
            id_pose = _id
            _id += 1
            # writeEdge(edgeFilePath, "EDGE_SE2", _id-1, _id, )
            for landmark in landmarksPos:
                x_pv, y_pv = landmark[0:2]
                measure_ = landmark[0:2]
                x_po = rbPose[0] + x_pv*math.cos(rbPose[2])
                y_po = rbPose[1] + y_pv*math.cos(rbPose[2])
                landmark_estimate = [x_po, y_po]
                writeVertex(vertexFilePath, "VERTEX_XY", _id, landmark_estimate)
                writeEdge(edgeFilePath, "EDGE_SE2_XY", id_pose, _id, measure_, info_edgeXY)
                _id += 1

        # logger.info("rbPose: " + str(rbPose))
        
        # Ve landmark len leftImage
        imgLandmarkCam = drawLandmarks(leftImg, landmarks, textType='area')
        imgLandmarkVehicle = drawLandmarks(leftImg, landmarksPos)
        # imgObjects = drawObjects(leftImg, objects)
        
        # Show hinh anh. ()
        showImgs = 0
        if showImgs:
            cv2.namedWindow("Landmark Camera", flags=cv2.WINDOW_NORMAL)
            cv2.namedWindow("Landmark Vehicle", flags=cv2.WINDOW_NORMAL)
            while True:
                cv2.imshow("Landmark Camera", imgLandmarkCam)
                cv2.imshow("Landmark Vehicle", imgLandmarkVehicle)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

        # Luu anh
        # imgOutName_Obj = ".log/landmarked/" + args.city + indexImgs[i] + "objects.png"
        imgOutName_Cam = ".log/landmarked/" + args.city + indexImgs[i] + "landmarked_Cam.png"
        imgOutName_Vehicle = ".log/landmarked/" + args.city + indexImgs[i] + "landmarked_Vehicle.png"
        # cv2.imwrite(imgOutName_Obj, imgObjects)
        cv2.imwrite(imgOutName_Cam, imgLandmarkCam)
        cv2.imwrite(imgOutName_Vehicle, imgLandmarkVehicle)

    jointFile(g2oFilePath, vertexFilePath, edgeFilePath)