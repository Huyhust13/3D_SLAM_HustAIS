## Trên pc cá nhân
Môi trường: 
- Ubuntu 18.04
- Python2.7


## Lỗi
|Lỗi|Đã khắc phục|Nguyên Nhân| Khắc phục|
|---|---|---|---|
|Treo máy khi chạy tới nn.DataParallel|ok|Pytorch 0.4.0 và torchvision 0.2.0 không tương thích với cuda 10.1|upgrade pytorch và torchvision|
|Khi chay tren PC cua Huy - `CUDA out of memory. Tried to allocate 352.00 MiB (GPU 0; 3.79 GiB total capacity; 1.70 GiB already allocated; 245.12 MiB free; 593.61 MiB cached)`| |Thieu dung luong GPU (recommend ~4.5GB)| Co the downscale anh dau vao xuong|
|Laptop o Vien: cung bi `out of memory` khi chay bo du lieu cityscape co kich thuoc 2048x1014|ok|anh dau vao lon dan den can nhieu memory|down scale anh xuong 1024x512|
|Su dung bo CityScape, down scale xuong con 1024x512 thi anh disparity con bi loi chua chinh xac|||