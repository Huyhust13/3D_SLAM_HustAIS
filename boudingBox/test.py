import os 
import cv2 as cv
import numpy as np
import json
import argparse

parser = argparse.ArgumentParser(description="boundingbox")
parser.add_argument("--name", help="name of data", default="aachen_000000_000019")
args = parser.parse_args()

# Cityscapes
imgColor = args.name + "_leftImg8bit.png"
labelFile = args.name + "_gtFine_polygons.json"

# Apollo 
# imgColor = args.name + "_bin.png"
# labelFile = args.name + ".json"

img = cv.imread(imgColor)

if labelFile:
    with open(labelFile, 'r') as f:
        datastore = json.load(f)
                
object_labels = ['traffic sign','traffic light','pole']
font = cv.FONT_HERSHEY_SIMPLEX

print("SL object: " + str(len(datastore["objects"])))

for j in range(len(datastore["objects"])):      #range(10):     #
    X= []
    Y= []
    for i in range(len(datastore["objects"][j]['polygon'])):
        X.append(datastore["objects"][j]['polygon'][i][0])
        Y.append(datastore["objects"][j]['polygon'][i][1])
        
    X = np.array(X)
    Y = np.array(Y)
    
    xmax = X[np.argmax(X)]
    ymax = Y[np.argmax(Y)]
    xmin = X[np.argmin(X)]
    ymin = Y[np.argmin(Y)]
    label = str(datastore["objects"][j]['label'])
    try:
        index = object_labels.index(label)
        print("Number of vertices of Object {} is : {}".format(j, len(X)))
    except:
        continue
    
    if len(X) < 6:
        print("Number of vertices: " + str(len(X)))
        print(label)
        print(xmin, ymin, xmax -xmin, ymax -ymin)
        cv.putText(img, str(datastore["objects"][j]['label']), (xmin+5,ymin-5), font, 1, (255,255,0), 1) 
        cv.rectangle(img, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))

img_out = args.name + "_labeled.png"
cv.imwrite(img_out,img) #bochum_000000_003245

