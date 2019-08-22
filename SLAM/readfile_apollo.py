import numpy as np
import math

data = [0]

x = [0]
y = [0]
z = [0]
theta = [0]

A = [np.zeros((4,4))]
print(A)
time = [0]

if __name__ == '__main__':
	# Mo file
	path = '/home/tungngo/Downloads/pose.txt'
	with open(path, 'r') as file:
		count = 0
		for line in file:
			count += 1
			b = [0]
			for word in line.split():
				b.append(word)
			del(b[0])
			# Doc ma tran dich chuyen T
			T = np.array([[b[0], b[1], b[2], b[3]], [b[4], b[5], b[6], b[7]], [b[8], b[9], b[10], b[11]], [b[12], b[13], b[14], b[15]]])
			A.append(T)
			time.append(b[16])
			theta.append(math.atan(float(b[4])/float(b[0]))) # Tinh huong

		print(A[1])

	# So sanh time de sap xep thu tu cac diem
	for i in range(len(time)-1):
		for j in range(len(time)-1):
			if (time[i]<time[j]):
				swap_time = time[i]
				time[i] = time[j]
				time[j] = swap_time

				swap_mat = A[i]
				A[i] = A[j]
				A[j] = swap_mat
	print(A[1])
	print(time[1])

	# Them cac diem moi vao list x, y
	for i in range(count):
		x.append(A[i+1][0][3].tostring())
		y.append(A[i+1][1][3].tostring())
		z.append(A[i+1][2][3].tostring())
	print(x[1])

	print(type(x[1]))
	print(y[1])
	print(z[1])
	print(time[1])

	# Tao file g2o
	file_odom = open("/home/tungngo/Desktop/apollo_odom_result.g2o", 'w')
	s = " "
	for i in range(len(x)):
		#file_odom.write(x[i])
		file_odom.write("VERTEX_SE2"+ s + str(i) + s + str(x[i]) + s + str(y[i]) + s + str(theta[i]) + "\n")
	for i in range(len(x)-1):
		file_odom.write("EDGE_SE2" + s + str(i) + s + str(i+1) + s + str(float(x[i+1])-float(x[i])) + s + str(float(y[i+1])-float(y[i])) + s + str(theta[i+1]-theta[i]) + " 100 0 0 500 0 500" "\n")
	file_odom.close()
