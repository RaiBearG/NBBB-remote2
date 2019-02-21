
# Import local libraries
import math

# system constants 
#m and b values of front yard found using tools/line_parameters.py
m = 2.347939316690
b = 335.732012260547
#gps points of the starting reference 
slat = 48.015409967799
slon = -122.540046375689

def find_point(m, b, x, y):
	"""
	m,b equation variables of reference line
	x,y real time point. 
	find distance between (x,y) and y=mx+b
	"""
	# p = slope of perpendicular line
	p = -(1/m)
	#print p
	# c = y intersept of perpendicular line
	c = y - (p*x)
	#print c

	lon = (c-b)/(m-p)
	lat = (m*lon) + b

	return lat, lon

def distance (lat1, lon1, lat2, lon2):
	"""
	Finds the distance between 2 GPS lat and long 
	coordinates in inches
	"""
	dlong = (lon2 - lon1) * math.pi / 180.0
	dlat = (lat2 - lat1) * math.pi / 180.0
	a = pow(math.sin(dlat/2.0), 2) + math.cos(lat1*math.pi/180.0) * math.cos(lat2*math.pi/180.0) * pow(math.sin(dlong/2.0),2)
	c =  2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	#convert distance to inches
	d = 6367 * c * 39370.07874016

	return d
def get_distance(lat, lon):
	#find perpendicular point of point on line
	linepoint = find_point(m, b, lon, lat)
	#calculate distance of point from line
	dist = distance(lat, lon, linepoint[0], linepoint[1])
	#figure out direction of travel 
	if lon<linepoint[1]:
		dist = dist*-1
	return dist

def get_howfarout(lat, lon, dist):
	#how far from the lat long in the brackers
	howfarout = distance(slat, slon, lat, lon) 
	#compendate for distance from center line
	howfarout = abs(pow(dist,2)-pow(howfarout,2))
	#convert fistance to ft from inches
	howfarout = (math.sqrt(howfarout))/12
	#figure out direction of travel
	if lat < slat: 
		howfarout = howfarout * -1
	return howfarout

def tilt_angle(accx, accy, accz, defx, defy, defz):
	# algorythm from http://www.hobbytronics.co.uk/accelerometer-info
	dx = float(accx-defx)
	dy = float(accy-defy)
	#dz = float(accz-defz)
	dz=1
	x2 = dx*dx
	y2 = dy*dy
	z2 = dz*dz

	# xaxis
	result = math.sqrt(y2+z2)
	if result==0:
		xangle=0
	else:
		result = dx/result
		xangle = math.atan(result)*180/math.pi*2
	
	# yaxis
	result = math.sqrt(x2+z2)
	if result==0:
		yangle=0
	else:
		result = dy/result
		yangle = math.atan(result)*180/math.pi*2

	return xangle, yangle


#def tilt_error(dist,x,y,height):

#	return dist 

def status_update(status):
	if status == 0:
		fix = "no fix"
	elif status == 1:
		fix = "single point"
	elif status == 2:
		fix = "DGPS"
	elif status == 3:
		fix = "Float RTK"
	elif status == 4:
		fix = "fixed RTK"
	elif status == 5:
		fix = "Dead Rekon"
	elif status == 6:
		fix = "SBAS"
	return fix


def get_output(lat, lon, status, accx, accy, accz, defx, defy, defz, height):

	dist = get_distance(lat, lon)
	
	howfarout = get_howfarout(lat, lon, dist)

	angles = tilt_angle(accx, accy, accz, defx, defy, defz)

	#dist = tilt_error(dist,x,y,height)

	fix = status_update(status)
	tilt=angles[0]

	return dist, howfarout, fix, tilt