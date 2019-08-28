#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import argparse
import cv2
import sys


parser = argparse.ArgumentParser(description="Images2Video")
parser.add_argument("--imgFolder", help="path to images folder", default="landmarked/")
parser.add_argument("--videoPath", help="path to video output folder", default="stuttgart_0")
parser.add_argument("--videoName", help="path to video output folder", default="stuttgart_01_landmarked.mp4")

args = parser.parse_args()

# Loc file theo duoi
def is_type_file(filename, EXTENSIONS):
    return any(filename.endswith(extension) for extension in EXTENSIONS)

def fileLoader(filepath, EXTENSIONS):
    files = [file for file in os.listdir(filepath) if is_type_file(file, EXTENSIONS)]
    files.sort()
    return files

def backspace(n):
    sys.stdout.write((b'\x08' * n).decode()) # use \x08 char to go back   

if __name__ == "__main__":
    imageFiles = fileLoader(args.imgFolder, [".png"])
    img = cv2.imread(args.imgFolder+imageFiles[0], 1)
    # print(imageFiles[0])
    print(img.shape)
    height, width, layers = img.shape
    size = (width, height)
    fps = 10
    vidOut = cv2.VideoWriter(args.videoName, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    # print("Start...", end = '')
    print("Start...")
    i = 0
    for filename in imageFiles:
        img = cv2.imread(args.imgFolder+filename, 1)
        cv2.putText(img, "fps: {} | {}".format(fps, filename.split("_")[3]), (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        # cv2.putText(img, "fps: {}".format(fps), (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        vidOut.write(img)
        complete = int(i*100/len(imageFiles))
        s= "running... " + str(complete) + "%"
        sys.stdout.write(s)                     # just print
        sys.stdout.flush()                      # needed for flush when using \x08
        backspace(len(s))                       # back n chars
        i += 1    
    vidOut.release()
    print("Video output was saved at: " + str(args.videoName))



# for i in range(101):                        # for 0 to 100
#     s = str(i) + '%'                        # string for output
#     sys.stdout.write(s)                     # just print
#     sys.stdout.flush()                      # needed for flush when using \x08
#     backspace(len(s))                       # back n chars    
#     time.sleep(0.2)    