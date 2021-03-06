from __future__ import print_function
import argparse
import os
import random
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
from torch.autograd import Variable
import torch.nn.functional as F
import skimage
import skimage.io
import skimage.transform
import numpy as np
import time
import math
from utils import preprocess 
from models import *
from log_yaml import *
# import cv2

# 2012 data /media/jiaren/ImageNet/data_scene_flow_2012/testing/

parser = argparse.ArgumentParser(description='PSMNet')
parser.add_argument('--KITTI', default='2015',
                    help='KITTI version')
parser.add_argument('--datapath', default='/media/jiaren/ImageNet/data_scene_flow_2015/testing/',
                    help='select model')
parser.add_argument('--loadmodel', default=None,
                    help='loading model')
parser.add_argument('--model', default='stackhourglass',
                    help='select model')
parser.add_argument('--maxdisp', type=int, default=192,
                    help='maxium disparity')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='enables CUDA training')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()

torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

if args.KITTI == '2015':
   from dataloader import KITTI_submission_loader as DA
else:
   from dataloader import KITTI_submission_loader2012 as DA  

test_left_img, test_right_img = DA.dataloader(args.datapath)

if args.model == 'stackhourglass':
    model = stackhourglass(args.maxdisp)
elif args.model == 'basic':
    model = basic(args.maxdisp)
else:
    print('no model')
    
model = nn.DataParallel(model, device_ids=[0]) #, device_ids=[0,1,2,3]
# torch.distributed.init_process_group(backend="nccl", world_size=4, rank=2)
# model = nn.parallel.DistributedDataParallel(model)
model.cuda()

if args.loadmodel is not None:
    state_dict = torch.load(args.loadmodel)
    model.load_state_dict(state_dict['state_dict'])

logger.info('Number of model parameters: {}'.format(sum([p.data.nelement() for p in model.parameters()])))

def test(imgL,imgR):
        model.eval()

        if args.cuda:
           imgL = torch.FloatTensor(imgL).cuda()
           imgR = torch.FloatTensor(imgR).cuda()     

        imgL, imgR= Variable(imgL), Variable(imgR)

        with torch.no_grad():
            output = model(imgL,imgR)
        output = torch.squeeze(output)
        pred_disp = output.data.cpu().numpy()

        return pred_disp
def crop_center(img, cropx, cropy):
	y = img.shape[1]
	x = img.shape[2]
	startx = x//2-(cropx//2)
	starty = y//2-(cropy//2)
	return img[:,starty:starty+cropy, startx:startx+cropx]

def main():
    processed = preprocess.get_transform(augment=False)
    for inx in range(len(test_left_img)): #len(test_left_img)

        imgL_o = (skimage.io.imread(test_left_img[inx]).astype('float32'))
        imgR_o = (skimage.io.imread(test_right_img[inx]).astype('float32'))

        sizex = 640#1024 # = 2048/6.4
        sizey = 384#512 # = 1024/3.2
        logger.debug("Before resize {}:{}:{}".format(imgL_o.shape[0], imgL_o.shape[1], imgL_o.shape[2]))
        imgL_o = skimage.transform.resize(imgL_o, (sizey, sizex),anti_aliasing=True)
        imgR_o = skimage.transform.resize(imgR_o, (sizey, sizex),anti_aliasing=True)
        logger.debug("After resize {}:{}:{}".format(imgL_o.shape[0], imgL_o.shape[1], imgL_o.shape[2]))
        
        imgL = processed(imgL_o).numpy()
        imgR = processed(imgR_o).numpy()
        
        # crop image Cityscapes:
        # logger.debug("Before crope {}:{}:{}".format(imgL.shape[0], imgL.shape[1], imgL.shape[2]))
        # imgL = crop_center(imgL, sizex, sizey)
        # imgR = crop_center(imgR, sizex, sizey)
        # logger.debug("After crope {}:{}:{}".format(imgL.shape[0], imgL.shape[1], imgL.shape[2]))


        imgL = np.reshape(imgL,[1,3,imgL.shape[1],imgL.shape[2]])
        imgR = np.reshape(imgR,[1,3,imgR.shape[1],imgR.shape[2]])

        # pad to (384, 1248)
        # Doan code nay dung cho bo KITTI voi kich thuoc anh nho hon (384, 1248)
        # phai them vao de dat duoc kich thuoc anh phu hop   
        # top_pad = 384-imgL.shape[2]
        # left_pad = 1248-imgL.shape[3]
        # imgL = np.lib.pad(imgL,((0,0),(0,0),(top_pad,0),(0,left_pad)),mode='constant',constant_values=0)
        # imgR = np.lib.pad(imgR,((0,0),(0,0),(top_pad,0),(0,left_pad)),mode='constant',constant_values=0)

        start_time = time.time()
        pred_disp = test(imgL,imgR)
        logger.info('time = {}'.format(time.time() - start_time))

        # top_pad   = 384-imgL_o.shape[0]
        # left_pad  = 1248-imgL_o.shape[1]
        # img = pred_disp[top_pad:,:-left_pad]

        img = pred_disp
        dispmap = "disparity/"+test_left_img[inx].split('/')[-1]
        skimage.io.imsave(dispmap,(img*256).astype('uint16'))
        logger.info('disparity map was saved at {}'.format(dispmap)) 
if __name__ == '__main__':
    main()
