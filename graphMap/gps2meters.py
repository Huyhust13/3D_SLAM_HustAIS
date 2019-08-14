import math
import os
import json
import matplotlib.pyplot as plt 

R = 6378.137 #Radius of the Earth in km
lat_m = [0] #Latitude (kinh do)
longi_m = [0] #Longitude (vi do)
head_a = [0] #head all (list cac huong cua robot)

# Distance between 2 points by latitude and longitude
def distance(lat1, longi1, lat2, longi2):
	dlat = lat2*math.pi/180 - lat1*math.pi/180
	dlongi = longi2*math.pi/180 - longi1*math.pi/180
	a = math.sin(dlat/2)*math.sin(dlat/2) + math.cos(lat1*math.pi/180)*math.cos(lat2*math.pi/180)*math.sin(dlongi/2)*math.sin(dlongi/2)
	c = 2*math.asin(math.sqrt(a))
	d = R*c
	return d*1000 #meter

# Add poses to list
def gps2meters(i, head, lat, longi):
	lat_m.append(distance(0,longi,lat,longi))
	longi_m.append(distance(lat,0,lat,longi))
	head_a.append(head)
	return [head_a, lat_m, longi_m]

# Read data from files
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
	path = "/media/tungngo/DATA/Chuyen_mon/Mechatronics/Introduction to Mobile Robotics/GraphSLAM/vehicle_trainextra/vehicle/train_extra/nuremberg/"

	print('open')
	#Read files and set files in order
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
	'''
	del lat_m[0]
	del longi_m[0]
	del head_a[0]

	plt.plot(longi_m,lat_m)
	plt.show()
	'''
	
	# Create temporary list
	lat_m_t = [0]
	longi_m_t = [0]
	head_a_t = [0]

	# Add data to temporary list
	for i in range(len(lat_m)-1):
		lat_m_t.append(lat_m[i+1]-lat_m[1])

	for i in range(len(longi_m)-1):
		longi_m_t.append(longi_m[i+1]-longi_m[1])

	for i in range(len(head_a)-1):
		head_a_t.append(head_a[i+1]-head_a[1])

	# Delete the first zero element
	del lat_m_t[0]
	del longi_m_t[0]
	del head_a_t[0]

	# Write data to g2o file
	file_odom = open(path + "result/odom_result.g2o", 'w')
	s = " "
	for i in range(len(head_a_t)):
		
		file_odom.write("VERTEX_SE2"+ s + str(i) + s + str(longi_m_t[i]) + s + str(lat_m_t[i]) + s + str(head_a_t[i]) + "\n")
	for i in range(len(head_a_t)-1):
		file_odom.write("EDGE_SE2" + s + str(i) + s + str(i+1) + s + str(longi_m_t[i+1]-longi_m_t[i]) + s + str(lat_m_t[i+1]-lat_m_t[i]) + s + str(head_a_t[i+1]-head_a_t[i]) + " 100 0 0 500 0 500" "\n")
	file_odom.close()