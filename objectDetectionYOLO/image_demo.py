#!/usr/bin/env python

from pydarknet import Detector, Image
import cv2
import argparse
import os

parser = argparse.ArgumentParser(description="ObjectDetectionYOLOv3")
parser.add_argument("--modelPath", help="path to model folder", default="model/")
parser.add_argument("--leftImgFolder", help="path to Left color image", default="samples/")
args = parser.parse_args()

def loadmodel(modelPath):
    net = Detector(bytes(modelPath + "yolo.cfg", encoding="utf-8"), bytes(modelPath + "yolov3.weights", encoding="utf-8"), 0, bytes(modelPath+ "yolo.data",encoding="utf-8"))
    return net

def fileLoader(filepath):
    files = [file for file in os.listdir(filepath)]
    files.sort()
    return files

if __name__ == "__main__":
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))
    net = loadmodel(args.modelPath)
    files = fileLoader(args.leftImgFolder)
    for file in files:
        img = cv2.imread(args.leftImgFolder + file)
        img2 = Image(img)

        # r = net.classify(img2)
        results = net.detect(img2)
        print(results)
        for cat, score, bounds in results:
            x, y, w, h = bounds
            cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
            cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
        
        cv2.imwrite("output/" + file[0:file.rfind("left")] + "detected.png", img)


    # cv2.imshow("output", img)
    # img2 = pydarknet.load_image(img)

    # cv2.waitKey(0)
