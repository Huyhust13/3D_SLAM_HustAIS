import math
import os
import json
import matplotlib.pyplot as plt 

R = 6378.137 #Radius of the Earth in km
# kinh do - vi do
lat_m = [0]
longi_m = [0]
# huong
head_a = [0] #head all

# Ham tinh khoang cach giua hai diem bang kinh do va vi do
def distance(lat1, longi1, lat2, longi2):
	dlat = lat2*math.pi/180 - lat1*math.pi/180
	dlongi = longi2*math.pi/180 - longi1*math.pi/180
	a = math.sin(dlat/2)*math.sin(dlat/2) + math.cos(lat1*math.pi/180)*math.cos(lat2*math.pi/180)*math.sin(dlongi/2)*math.sin(dlongi/2)
	c = 2*math.asin(math.sqrt(a))
	d = R*c
	return d*1000 #meter

# Ham chen them diem vao list cac diem gps
def gps2meters(i, head, lat, longi):
	lat_m.append(distance(0,longi,lat,longi))
	longi_m.append(distance(lat,0,lat,longi))
	head_a.append(head)
	return [head_a, lat_m, longi_m]

# Ham doc cac file json de lay du lieu
def openfile(path):
	a = open(path)
	print('a')
	b = json.load(a)
	gpsHeading = b['gpsHeading']
	gpsLatitude = b['gpsLatitude']
	gpsLongitude = b['gpsLongitude']
	a.close()
	return [gpsHeading, gpsLatitude, gpsLongitude]

if __name__ == '__main__':
	#Path to dataset folder
	# path = "/media/tungngo/DATA/Chuyen_mon/Mechatronics/Introduction to Mobile Robotics/GraphSLAM/vehicle_trainextra/vehicle/train_extra/nuremberg/"
	path = "/media/huynv/Data/14.ComputerVision/3.Data/3DSlamData/aachen/vehicle/"

	print('open')
	#Read and set files in order
	for root, dirs, files in os.walk(path):
		for i in range(len(files)-1):
			for j in range(len(files)-1):
				if (files[i]<files[j]): 
					swap = files[i]
					files[i] = files[j]
					files[j] = swap

		#read gps data
		for i in range(len(files)-1):
			print(files[i])
			file = openfile(path + files[i])
			print(file[0])
			print(file[1])
			print(file[2])
			result = gps2meters(i, file[0], file[1], file[2])
	
	del lat_m[0]
	del longi_m[0]
	del head_a[0]

	plt.plot(longi_m,lat_m)
	plt.show()