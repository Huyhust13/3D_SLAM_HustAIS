#!/usr/bin/env python
import os 
import cv2 as cv
import numpy as np
import json
import argparse

parser = argparse.ArgumentParser(description="boundingbox")
parser.add_argument("--name", help="name of data", default="170927_070404283_Camera_5")
args = parser.parse_args()

# Cityscapes
# imgColor = args.name + "_leftImg8bit.png"
# labelFile = args.name + "_gtFine_polygons.json"

# Apollo 
imgColor = args.name + ".jpg" #"_bin.png"
labelFile = args.name + ".json"

img = cv.imread(imgColor)

if labelFile:
    with open(labelFile, 'r') as f:
        datastore = json.load(f)
                
# object_labels = ['traffic sign','traffic light','pole']
font = cv.FONT_HERSHEY_SIMPLEX

print("SL object: " + str(len(datastore["objects"])))

for j in range(len(datastore["objects"])):      #range(10):     #
    X= []
    Y= []
    # print(datastore["objects"][j]['polygons'])
    # print(datastore["objects"][j]['polygons'][0][1])
    # exit()

    for i in range(len(datastore["objects"][j]['polygons'][0])):
        X.append(datastore["objects"][j]['polygons'][0][i][0])
        Y.append(datastore["objects"][j]['polygons'][0][i][1])
    
    # print("X: " + str(X))
    # print("Y: " + str(Y))
    # exit()
    ymax = max(Y)
    xmax = max(X)
    xmin = min(X)
    ymin = min(Y)
    label = str(datastore["objects"][j]['label'])
    # try:
    #     index = object_labels.index(label)
    #     print("Number of vertices of Object {} is : {}".format(j, len(X)))
    # except:
    #     continue
    # exit()
    # if len(X) < 6:
        # print("Number of vertices: " + str(len(X)))
        # print(label)
    print(xmin, ymin, xmax -xmin, ymax -ymin)
    cv.putText(img, str(datastore["objects"][j]['label']), (xmin+5,ymin-5), font, 1, (255,255,0), 3) 
    cv.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3)

img_out = args.name + "_labeled.png"
cv.imwrite(img_out,img) #bochum_000000_003245

