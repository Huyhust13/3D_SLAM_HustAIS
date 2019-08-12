import cv2 as cv
import numpy as np
import json

img = cv.imread("170927_070404283_Camera_5_instanceIds.png")

if "170927_070404283_Camera_5.json":
            with open("170927_070404283_Camera_5.json", 'r') as f:
                datastore = json.load(f)

font = cv.FONT_HERSHEY_SIMPLEX
for j in range(len(datastore["objects"])):
    X= []
    Y=[]
    print(j)
    for i in range(len(datastore["objects"][j]['polygons'][0])):
        X.append(datastore["objects"][j]['polygons'][0][i][0])
        Y.append(datastore["objects"][j]['polygons'][0][i][1])
        
    X = np.array(X)
    Y = np.array(Y)
    xmax = X[np.argmax(X)]
    ymax = Y[np.argmax(Y)]
    xmin = X[np.argmin(X)]
    ymin = Y[np.argmin(Y)]
    cv.putText(img, str(datastore["objects"][j]['label']), (xmin+5,ymin-5), font, 1, (255,255,0), 1) 
    cv.rectangle(img, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))
cv.imwrite("test.jpg",img)


