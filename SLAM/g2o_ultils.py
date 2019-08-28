# -*- coding: utf-8 -*-

import math
import os
import json
import matplotlib.pyplot as plt 
from log_yaml import *

R = 6378.137 #Radius of the Earth in km

# Distance between 2 points by latitude and longitude
def distanceGPS(lati1, longi1, lati2, longi2):
	distance_latitude = lati2*math.pi/180 - lati1*math.pi/180
	distance_longitude = longi2*math.pi/180 - longi1*math.pi/180
	a = math.sin(distance_latitude/2)*math.sin(distance_latitude/2) + math.cos(lati1*math.pi/180)*math.cos(lati2*math.pi/180)*math.sin(distance_longitude/2)*math.sin(distance_longitude/2)
	c = 2*math.asin(math.sqrt(a))
	d = R*c
	return d*1000 #meter

# Ham lay vi tri robot theo gps
def getRobotPoseGPS(filePath):
    # load json file
    with open(filePath, 'r') as f:
        vehicles = json.load(f)
    gpsLongitude = vehicles["gpsLongitude"]
    gpsLatitude = vehicles["gpsLatitude"]
    gpsHeading = vehicles["gpsHeading"]
    # Vi do tuyet doi he met
    latitude_m = distanceGPS(0, gpsLongitude, gpsLatitude, gpsLongitude)
    # Kinh do tuyet doi he met
    longitude_m = distanceGPS(gpsLatitude, 0, gpsLatitude, gpsLongitude)
    # Huong theo don vi radian
    head_degree = gpsHeading*math.pi/180.0 
    return [latitude_m, longitude_m, head_degree]

# Ham vi tri tuong doi cua robot theo vi tri ban dau
# Gia du lieu odom tu gps
def odomFromGPS(poseGPS, poseInit):
    odom = [0,0,0]
    for i in range(len(poseGPS)):
        odom[i] = poseGPS[i] - poseInit[i]
    return odom

def disc2pose(pose, pose_old):
    disc = [0,0,0]
    for i in range(len(pose)):
        disc[i] = pose[i] - pose_old[i]
    return disc

# Ham tinh odom tu speed:
def speed2odom(fileVehicle, timeStep, poseOld):
    # load json file
    with open(fileVehicle, 'r') as f:
        vehicles = json.load(f)
    speed = vehicles['speed']
    yawRate = vehicles['yawRate']

    ds = speed*timeStep
    dtheta = yawRate*timeStep
    # odom tu vi tri truoc
    xOld, yOld, thetaOld = poseOld
    x = xOld + ds*math.cos(thetaOld + dtheta/2)
    y = yOld + ds*math.sin(thetaOld + dtheta/2)
    theta = thetaOld + dtheta 
    return [x, y, theta]

# Ham chuyen toa do 2D
# rbPose[x_vo, y_vo, theta]: hệ tọa độ xe trong world
# landmarkVehicle [x_pv, y_pv, boundingbox[]]
# return: [x_po, y_po]
def transform(rbPose, landmarkVehicle):
    x_vo, y_vo, theta = rbPose
    x_pv, y_pv = landmarkVehicle[0:2]
    # x_po, y_po: toa do landmark trong htd world:
    x_po = x_vo + x_pv*math.cos(theta) - y_pv*math.sin(theta)
    y_po = y_vo + x_pv*math.sin(theta) + y_pv*math.cos(theta)
    return [x_po, y_po]

# Ham tinh timeStep
def getTimeStep(timestampPath, timeOld):
    with open(timestampPath, 'r') as f:
        time = f.read()
    timeNow = int(time)*1e-9
    return timeNow - timeOld
    
#region Write g2o file:
# Ham ghi them dong vetex vao file vertex 
# Hai ham nay su dung cho main.py 
def writeVertex(vertexFilePath, tag, id_, current_estimate):
    vertexLine = "{} {} {}\n".format(tag, id_, (' '.join(map(str, current_estimate))))
    with open(vertexFilePath, 'a') as vertexWriter:
        vertexWriter.write(vertexLine)

def writeEdge(edgeFilePath, tag, id1, id2, measurement, info_matrix):
    edgeLine = "{} {} {} {} {}\n".format(tag, id1, id2, (' '.join(map(str, measurement))), (' '.join(map(str, info_matrix))))
    with open(edgeFilePath, 'a') as edgeWriter:
        edgeWriter.write(edgeLine)

def jointFile(g2oFilePath, vertexFilePath, edgeFilePath):
    with open(vertexFilePath) as vertexFile:
        with open(g2oFilePath, "a") as g2oFile:
            for line in vertexFile:
                g2oFile.write(line)

    with open(edgeFilePath) as edgeFile:
        with open(g2oFilePath, "a") as g2oFile:
            for line in edgeFile:
                g2oFile.write(line)
#endregion

# Test
# fileVehicle = "/media/huynv/Data/14.ComputerVision/3.Data/3DSlamData/aachen_dev/vehicle/aachen_000000_000019_vehicle.json"        
# getRobotPoseGPS(fileVehicle)