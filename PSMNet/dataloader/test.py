import os
import os.path

filepath = "/home/huyhv/1.Coding/3D_SLAM_HustAIS/depthEstimate/disparity_given/berlin/"

img = [img for img in os.listdir(filepath)]
img.sort()
print(img)