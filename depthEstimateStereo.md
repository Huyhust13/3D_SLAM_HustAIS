
# Depth Estimate from Stereo cameras
### Tham khảo:
* Depth estimation from stereo cameras (pdf)
### Disparity estimation 

- Nội dung của stereo matching là dựa trên việc tìm sự tương thích giữa hai ảnh đầu vào. 
Trong bài này, việc việc khớp gwiax hai điểm được xem xét bằng việc kiểm tra nxn pixel láng giềng N quanh cả 2 điểm đấy.
- Matching block được đặt cho mỗi pixel trong một hình ảnh. 
- Sự khác nhau trong vị trí của các ddierm trong các mặt phẳng ảnh là *disparity* của điểm đó.
- Matching block size là một thông số quan trọng ảnh hưởng tới kết quả của việc ước tính disparity. Block nhỏ hơn có thể tìm kiếm chi tiết tốt hơn, nhưng dễ có lỗi, trong khi block lớn hơn thì robust hơn nhưng lại bỏ qua các chi tiết nhỏ. 


### Depth from disparity
- Disparity không giống depth.
Bỗi quan hệ giữa disparity và depth dựa trên cấu hình camera 
- Công thức: `depth = baseline * focal / disparity`
![cong thuc](https://raw.githubusercontent.com/Huyhust13/3D_SLAM_HustAIS/master/figures/stereo_depth.png?token=AIFPE4M3KDRG46SAVAXI7O25GZ4LU) 


    - (fx,fy) - Focal length in pixels.  

        * fx=F/px  
        * fy=F/py  

    - F - Focal length in world units, typically expressed in millimeters.  
    - (px,py) — Size of the pixel in world units.

#### Ví dụ:
```
*To obtain depth, you need to convert disparity using the following formula:
depth = baseline * focal / disparity
For KITTI the baseline is 0.54m and the focal ~721 pixels. 
The relative disparity outputted by the model has to be scaled by 1242 which is the original image size.
The final formula is:
depth = 0.54 * 721 / (1242 * disp)*
```
<img align="center" src="https://raw.githubusercontent.com/Huyhust13/3D_SLAM_HustAIS/master/figures/vd_depthCitycapes.png">

Các vấn đề:
- Phải đọc được đúng định dạng dữ liệu từ disparity map. 
    Giá trị maximum của disparity thể hiện bằng D.
    Với PSMNet thì Maximum disparity là 192 ==> Quy định định dạng biến đọc từ opencv.
- Tìm được đúng thông số camera (đơn vị đo của thông số)


## Phương pháp
1. Dùng bộ dữ liệu stereo (ApolloDataset hoặc CityscapesDataset), chạy qua PSMNet để ra dispiraty map.
2. Từ dispiraty map, kết hợp với thông số camera để tính ra depth map
3. Depth map + object detected -> Dense point cloud hay gì???

- Mạng đã chạy được
- Dữ liệu camera:
    - Citicape có bộ dữ liệu camera:
    ```
    {
        "extrinsic": {
            "baseline": 0.209313, 
            "pitch": 0.038, 
            "roll": 0.0, 
            "x": 1.7, 
            "y": 0.1, 
            "yaw": -0.0195, 
            "z": 1.22
        }, 
        "intrinsic": {
            "fx": 2262.52, 
            "fy": 2265.3017905988554, 
            "u0": 1096.98, 
            "v0": 513.137
        }
    }
    ```
    Trong đó: *baseline (m), fx, fy (pixel)*. 

    fx, fy là gì???


## Các bộ dữ liệu:
1. ApoloScapesDataset: 
* [Link download](http://apolloscape.auto/stereo.html#to_metric_href)
* [git repository](https://github.com/ApolloScapeAuto/dataset-api/tree/master/stereo)

Dữ liệu:
- Ảnh stereo
- Ảnh disparity
- Ảnh depth

==> Tập Stereo_train_001 (4.4GB) có đầy đủ thông tin trên để tính depth, nhưng bộ dữ liệu này không có ảnh depth được tính sẵn.
intrinsic.txt
```
K = [2301.3147, 0, 1489.8536; 0, 2301.3147, 479.1750; 0, 0, 1]
```
==> focal = 2301.3147 (pixel)


2. Cityscapes 
* [Link download](https://www.cityscapes-dataset.com/downloads/)
* [git repository](https://github.com/mcordts/cityscapesScripts)

Dữ liệu:
- Có dữ liệu để train nhận dạng cột đèn giao thông
- Có disparity
- Có thông số camera
- Không có ảnh depth có sẵn

- Thông số camera:
    - disparity precomputed disparity depth maps. To obtain the disparity values, compute for each pixel p with p > 0: d = ( float(p) - 1. ) / 256., while a value p = 0 is an invalid measurement. Warning: the images are stored as 16-bit pngs, which is non-standard and not supported by all libraries.


## Các bước dự kiến
1. Chạy lại file submission.py chạy mạng PSMNet để ra disparity map.
2. Dùng bộ Stereo_train_001 để tính depth từ disparity.
4. Kết nối với object detection
3. Nối thông từ chạy ảnh stereo ra depth.

## Triển khai:

## Khó khăn hiện tại
- Khó xác định baseline và focal của hệ thống stereo
- Chưa ghép được hệ thống


## Một số opensource
### [PSMNet](https://github.com/JiaRenChang/PSMNet)
- Thử chạy file submission.py với dữ liệu đã train sẵn *.tar
- Hi vọng có thể sử dụng mô hình đã train, chế biến lại code submission.py để  dùng luôn.

10/7/2019:
- Code submission.py đang chạy trên cuda, gặp một số lỗi khi chạy trên cpu

--> Code này cần CUDA

Train PSMNet:
- KITTY15: bộ ảnh thật, dataset street view từ xe ô tô. Chứa 200 ảnh stereo khớp với ảnh disparity ground-truth thưa dùng LiDAR và 200 ảnh test khác không có ảnh LiDAR. Kích thước ảnh 376*1240

```
The PSMNet architecture was implemented using PyTorch. All models were end-to-end trained with Adam
(β1 = 0:9; β2 = 0:999). We performed color normalization on the entire dataset for data preprocessing. During
training, images were randomly cropped to size H = 256
and W = 512. The maximum disparity (D) was set to 192.
We trained our models from scratch using the Scene Flow
dataset with a constant learning rate of 0.001 for 10 epochs.
For Scene Flow, the trained model was directly used for
testing. For KITTI, we used the model trained with Scene
Flow data after fine-tuning on the KITTI training set for 300
epochs. The learning rate of this fine-tuning began at 0.001
for the first 200 epochs and 0.0001 for the remaining 100
epochs. The batch size was set to 12 for the training on four
nNvidia Titan-Xp GPUs (each of 3). The training process
took about 13 hours for Scene Flow dataset and 5 hours for
KITTI datasets. Moreover, we prolonged the training process to 1000 epochs to obtain the final model and the test
results for KITTI submission.
```

- Dữ liệu để sử dụng với model pre-trained cần có H và W chia hết cho 32.
`If you use your own dataset, the width and height of image should be divisible by 32.`

- Ảnh disparity map tương ứng với ảnh trái.
    `For the pixel (x; y) in the
left image, if its corresponding point is found at (x − d; y)
in the right image, then the depth of this pixel is calculated
by fB d , where f is the camera's focal length and B is the
distance between two camera centers.`


### [DenseDepth](https://github.com/ialhashim/DenseDepth)
12/7/2019: 
DenseDepth từ [link này](https://github.com/ialhashim/DenseDepth).

Tập trung vào Depth môi trường đường phố ngoài trời.
Sử dụng model đã train sẵn: [KITTI](https://s3-eu-west-1.amazonaws.com/densedepth/kitti.h5)

Chạy `python test.py` với model kitti.h5 và ảnh từ KITTI dataset (phải resize về 348x1248)

---
### Thắc mắc:
- Input: 
    - Model train sẵn
    - Ảnh
- Output: 
    - Chiều sâu???

Vì sao chỉ 1 ảnh lại có thể ra đc chiều sâu???

### Cài cuda và sử dụng trên venv
1. Cài cuda  
https://medium.com/@kapilvarshney/how-to-setup-ubuntu-16-04-with-cuda-gpu-and-other-requirements-for-deep-learning-f547db75f227
2. Tạo môi trường venv để chạy laị code submission.py
3. Cài các gói cần thiết: 
`pip install -r requirements.txt`
- Kiểm chứng kết quả đo???

