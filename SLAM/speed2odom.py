import math
import json
import os

x=[0]
y=[0]
theta=[0]
timestep = [0]
files_19 = []

def speed2odom(i, speed, yawRate):
	#Te = 2 #timestep
	Te = timestep[i+1] - timestep[i]#*1e-9
	ds = speed*Te
	dtheta = yawRate*Te
	print(x[i])
	x.append(x[i] + ds*math.cos(theta[i] + dtheta/2))
	y.append(y[i] + ds*math.sin(theta[i] + dtheta/2))
	theta.append(theta[i] + dtheta)
	return [x, y, theta]

def openfile(path):
	a = open(path)
	b = json.load(a)
	speed = b['speed']
	yawRate = b['yawRate']
	a.close()
	return [speed, yawRate]

if __name__ == '__main__':
	
	# Path to timestamp folder
	time_path = "/home/tungngo/catkin_ws/src/test_dataset/video/timestamp/demoVideo/stuttgart_02/"
	#print(type(time_path))

	# Read timestamp
	for root, dirs, files in os.walk(time_path):
		print('Length of timestamp: ')
		print(len(files))
		'''
		for i in range(len(files)-1):
			if '019_t' in files[i]:
				files_19.append(files[i])
		print(len(files_19))
		#print(type(files_19[3]))
		'''
		for i in range(len(files)-1):
			for j in range(len(files)-1):
				if (files[i]<files[j]): 
					swap = files[i]
					files[i] = files[j]
					files[j] = swap

		'''
		for i in range(len(files_19)-1):	
			for j in range(len(files_19)-1):
				if (files_19[i]<files_19[j]): 
					swap = files_19[i]
					files_19[i] = files_19[j]
					files_19[j] = swap
		del(files_19[0])
		'''
		for j in range(len(files)-1):
			#print(time_path + files_19[i])
			temp_path = time_path + str(files[j])
			time_file = open(temp_path)
			time = time_file.read(9)
			timestep.append(int(time)*1e-8)
			#print(time)
			time_file.close()
		#print(timestep)



	#Path to dataset folder
	path = "/home/tungngo/catkin_ws/src/test_dataset/video/vehicle/demoVideo/stuttgart_02/"
	
	#Read and set files in order
	for root, dirs, files in os.walk(path):
		print('Length of odom:')
		print(len(files))
		for i in range(len(files)-1):
			for j in range(len(files)-1):
				if (files[i]<files[j]): 
					swap = files[i]
					files[i] = files[j]
					files[j] = swap
		
		#calculate odometry
		for i in range(len(files)-1):
			print(files[i])
			file = openfile(path + files[i])
			print(file[0])
			print(file[1])
			result = speed2odom(i, file[0], file[1])
	
	#for i in range(len(x)):


	file_odom = open(path + "result/odom_result.g2o", 'w')
	s = " "
	for i in range(len(x)):
		
		file_odom.write("VERTEX_SE2"+ s + str(i) + s + str(x[i]) + s + str(y[i]) + s + str(theta[i]) + "\n")
	for i in range(len(x)-1):
		file_odom.write("EDGE_SE2" + s + str(i) + s + str(i+1) + s + str(x[i+1]-x[i]) + s + str(y[i+1]-y[i]) + s + str(theta[i+1]-theta[i]) + " 100 0 0 500 0 500" "\n")
	file_odom.close()