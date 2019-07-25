python submission.py --maxdisp 192 \
                     --model stackhourglass \
                     --KITTI 2015 \
                     --datapath "../data/CityScapes/Berlin/" \
                     --loadmodel "../pretrained/pretrained_model_KITTI2015.tar" \
                    #  2>&1 | tee -a log/submission.log
                    #  &>> log/submission.log
                    #  --datapath "/media/huyhv/My Passport/1.3DVision/2.Data/KITTI/data_scene_flow/testing/" \
                     # --datapath "../data/CityScapes/Berlin/" \
		     #--datapath "../data/KITTY/" \
