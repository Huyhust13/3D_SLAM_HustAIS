# Depth estimate:

## Cách 1: Tính chiều sâu từ 2 ảnh stereo
Tham khảo: https://docs.opencv.org/master/dd/d53/tutorial_py_depthmap.html

Thông tin bị thiếu:
- f: Độ hội tụ của camera
- B: Khoảng cách giữa 2 camera.

## Cách 2: Lấy từ tập ảnh depth có trong dataset
Sử dụng code trên.  
Click chuột lên ảnh để in chiều sâu --> đang có vẻ bị sai.

Tham khảo:
- https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
- https://www.opencv-srf.com/2011/11/mouse-events.html
- https://docs.opencv.org/3.1.0/d7/dfc/group__highgui.html#ggaab4dc057947f70058c80626c9f1c25cead9b7a4f148eeff7eca24609f7a64adb1

## Cách 3: Dùng CNN
Như chỉ dẫn: https://github.com/JiaRenChang/PSMNet