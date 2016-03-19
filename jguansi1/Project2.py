# Name: Jerson Guansing
# CMSC471 - Project 2
# Instructor: Prof. Maksym Morawski
import math
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax):
	current_x = random.uniform(xmin, xmax)
	current_y = random.uniform(ymin, ymax)
	current_z = function_to_optimize(current_x, current_y)
	path = []
	path.append([current_x, current_y, current_z])
	while True:
		addToList = False
		# make sure to stay within the range given
		plus_x = path[len(path) - 1][0] + step_size
		if plus_x > xmax:
			plus_x = xmax
		minus_x = path[len(path) - 1][0] - step_size
		if minus_x < xmin:
			minus_x = xmin
		plus_y = path[len(path) - 1][1] + step_size
		if plus_y > ymax:
			plus_y = ymax
		minus_y = path[len(path) - 1][1] - step_size
		if minus_y < ymin:
			minus_y = ymin
		# x and y + step_size
		addToList, current_x, current_y, current_z = getNeighbor(function_to_optimize, path[len(path) - 1][0], plus_y, addToList, current_x, current_y, current_z)
		# x and y - step_size
		addToList, current_x, current_y, current_z = getNeighbor(function_to_optimize, path[len(path) - 1][0], minus_y, addToList, current_x, current_y, current_z)
		# x + step_size and y
		addToList, current_x, current_y, current_z = getNeighbor(function_to_optimize, plus_x, path[len(path) - 1][1], addToList, current_x, current_y, current_z)
		# x + step_size and y + step_size
		addToList, current_x, current_y, current_z = getNeighbor(function_to_optimize, plus_x, plus_y, addToList, current_x, current_y, current_z)
		# x + step_size and y - step_size
		addToList, current_x, current_y, current_z = getNeighbor(function_to_optimize, plus_x, minus_y, addToList, current_x, current_y, current_z)
		# x - step_size and y
		addToList, current_x, current_y, current_z = getNeighbor(function_to_optimize, minus_x, path[len(path) - 1][1], addToList, current_x, current_y, current_z)
		# x - step_size and y + step_size
		addToList, current_x, current_y, current_z = getNeighbor(function_to_optimize, minus_x, plus_y, addToList, current_x, current_y, current_z)
		# x - step_size and y - step_size
		addToList, current_x, current_y, current_z = getNeighbor(function_to_optimize, minus_x, minus_y, addToList, current_x, current_y, current_z)
		# add the xyz coordinates to the list
		if addToList == True:
			path.append([current_x, current_y, current_z])
		else:
			# exit since the current value is the lowest hill climbing value -- could be a local min
			break
	# return the path list - the last element is the min
	return path

def getNeighbor(function_to_optimize, x, y, addToList, current_x, current_y, current_z):
	z = function_to_optimize(x, y)
	if z < current_z:
		current_x, current_y, current_z = x, y, z
		addToList = True
	return addToList, current_x, current_y, current_z
	
def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax):
	path = []
	x, y, z = 0, 0, 0
	for n in range(0, num_restarts):
		# call hill climbing n number of times
		temp = hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax)
		if n == 0:
			x = temp[len(temp) - 1][0]
			y = temp[len(temp) - 1][1]
			z = temp[len(temp) - 1][2]
		elif temp[len(temp) - 1][2] < z:
			x = temp[len(temp) - 1][0]
			y = temp[len(temp) - 1][1]
			z = temp[len(temp) - 1][2]
		# append each hill climbing to the total list
		path = path + temp
	# return the path list and the coordinates of the min
	return path, x, y, z
	
def simulated_annealing(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax):
	current_x = random.uniform(xmin, xmax)
	current_y = random.uniform(ymin, ymax)
	current_z = function_to_optimize(current_x, current_y)
	path = []
	path.append([current_x, current_y, current_z])
	x, y, z = 0, 0, 0
	# keep looping until the temp is low enough - converges fast
	while max_temp > 1e-4:
		# randomly select a successor of current
		current_x = random.uniform(xmin, xmax)
		current_y = random.uniform(ymin, ymax)
		current_z = function_to_optimize(current_x, current_y)
		delta = current_z - path[len(path) - 1][2]
		if delta < 0:
			path.append([current_x, current_y, current_z])
		else:
			probability = math.exp(-delta / max_temp)
			if random.random() < probability:
				path.append([current_x, current_y, current_z])
			else:
				current_x = path[len(path) - 1][0]
				current_y = path[len(path) - 1][1]
				current_z = path[len(path) - 1][2]
		# keep track of the lowest value
		if len(path) == 1 or current_z < z:
			x = current_x
			y = current_y
			z = current_z
		max_temp = max_temp * 0.9
	# return the path list and the coordinates of the min
	return path, x, y, z

def getZ(x, y):
	r = math.sqrt(x**2 + y**2)
	z = (math.sin(x**2 + (3*(y**2))) / (0.01 + r**2)) + ( (x**2 + 5*(y**2)) * ( (math.exp(1 - r**2)) / 2) )
	return z

def plotPath(path, graphTitle, xmin, xmax, ymin, ymax, figNum):
	fig = plt.figure(figNum)
	ax = fig.gca(projection='3d')
	X = np.arange(xmin, xmax, 0.1)
	Y = np.arange(ymin, ymax, 0.1)
	X, Y = np.meshgrid(X, Y)
	R = np.sqrt(X**2 + Y**2)
	Z = (np.sin(X**2 + (3*(Y**2))) / (0.01 + R**2)) + ( (X**2 + 5*(Y**2)) * ( (np.exp(1 - R**2)) / 2) )
	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='y', alpha=0.3)
	ax.set_zlim(-1, 5)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
	ax.set_xlabel('X Axis')
	ax.set_ylabel('Y Axis')
	ax.set_zlabel('Z Axis')
	# the path taken by the algorithm
	pathX, pathY, pathZ = [], [], []
	for n in range(0, len(path)):
		pathX.append(path[n][0])
		pathY.append(path[n][1])
		pathZ.append(path[n][2])
	ax.scatter(pathX, pathY, pathZ)
	plt.title(graphTitle)
	


xmin, xmax, ymin, ymax = -2.5, 2.5, -2.5, 2.5
step_size = 0.01
num_restarts = 10
max_temp = 50

# test hill climbing
path = hill_climb(getZ, step_size, xmin, xmax, ymin, ymax)
graphTitle = "Hill Climbing"
if len(path) > 0:
	# the min is the last element in the list
	graphTitle = graphTitle + "\nPlot Size: " + str(len(path)) + "\n Min: x=" +  str(path[len(path) -1][0])  + "   y=" +  str(path[len(path) -1][1]) + "   z=" + str( path[len(path) -1][2])
plotPath(path, graphTitle, xmin, xmax, ymin, ymax, 1)

# test hill climbing with random restart
path, x, y, z = hill_climb_random_restart(getZ, step_size, num_restarts, xmin, xmax, ymin, ymax)
graphTitle = "Hill Climbing with Random Restart"
if len(path) > 0:
	# the min is returned as values x, y and z
	graphTitle = graphTitle + "\nPlot Size: " + str(len(path)) + "\n Min: x=" +  str(x)  + "   y=" +  str(y) + "   z=" + str(z)
plotPath(path, graphTitle, xmin, xmax, ymin, ymax, 2)

# test simulated annealing
path, x, y, z = simulated_annealing(getZ, step_size, max_temp, xmin, xmax, ymin, ymax)
graphTitle = "Simulated Annealing"
if len(path) > 0:
	# the min is returned as values x, y and z
	graphTitle = graphTitle + "\nPlot Size: " + str(len(path)) + "\n Min: x=" +  str(x)  + "   y=" +  str(y) + "   z=" + str(z)
plotPath(path, graphTitle, xmin, xmax, ymin, ymax, 3)

# show the three figure plots
plt.show()
