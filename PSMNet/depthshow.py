import cv2
import argparse

parser = argparse.ArgumentParser(description='depth')
parser.add_argument('--image', default='000000_10.png', help='path depth image')

args = parser.parse_args()


def showDepth(imagePath):
    depthImage = cv2.imread(args.image, cv2.IMREAD_ANYDEPTH)
    cv2.imshow("dept image",  depthImage)
    depthValue = depthImage[50, 50]
    print(depthValue)
    cv2.waitKey(0)

if args.image:
    showDepth(args.image)
    