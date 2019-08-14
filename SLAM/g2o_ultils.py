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
    return [head_degree, latitude_m, longitude_m]

# Ham vi tri tuong doi cua robot theo vi tri ban dau
# Gia du lieu odom tu gps
def odomFromGPS(poseGPS, poseInit):
    odom = []
    for i in range(len(poseGPS)):
        odom[i] = poseGPS[i] - poseInit
    return odom



# Test
# filePath = "/media/huynv/Data/14.ComputerVision/3.Data/3DSlamData/aachen_dev/vehicle/aachen_000000_000019_vehicle.json"        
# getRobotPoseGPS(filePath)