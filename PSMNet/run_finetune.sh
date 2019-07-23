python finetune.py --maxdisp 192 \
                   --model stackhourglass \
                   --datatype 2015 \
                   --datapath ../../2.Data/KITTI/data_scene_flow/training/ \
                   --epochs 300 \
                   --loadmodel ../../2.Data/KITTI/pretrained_sceneflow.tar \
                   --savemodel ./trained/