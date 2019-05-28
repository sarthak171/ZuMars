import cv2 
import numpy as np
import math

focalLen = 480
horizCent = 240
vertiCent = 320
ang = math.atan2(0.0508,0.2032)

def createTarget (temp):

    cont = temp
    
    avgX = 0

    avgY = 0

    minX = temp[0][0][0]

    maxX = temp[0][0][0]

    minY = temp[0][0][1]

    maxY = temp[0][0][1]
    
    pref = temp[0]
    
    hyp = 0

    #sets mins and maxs based on the first points x and y, to be changed later
    #temp is an input from approxpolydp, an array of points, of a single target (one rectangle)
    
    for p in temp: #iterate through each point
        
        if p[0][0] < minX: #if the point's x is less than the lowest x previouly
            minX = p[0][0] #set lowest x to current points x
        
        if p[0][0] > maxX:
            maxX = p[0][0]
		
        if p[0][1] < minY:
            minY = p[0][1]
        
        if p[0][1] > maxY:
            maxY = p[0][1]
        
        hyp1 = math.sqrt((temp[0][0][0]-p[0][0])**2 + (temp[0][0][1] - p[0][1])**2)
                         
        if hyp1 > hyp:
            hyp = hyp1
            
        #minX, maxX, minY, maxY will have their respective values based off all the points in temp

    width1 = maxX-minX #width is highest x minus lowest x
    
    height1 = maxY-minY#height is highest y minus lowest y
    
    
    
    height = hyp*math.sin(ang)*0.677
    
    width = hyp*math.cos(ang)*0.677
    
    avgX = (maxX+minX)/2 
    
    avgY = (maxY+minY)/2
    
    centerPoint = [avgX, avgY] #the center is the average x and y in an array
    return centerPoint
def findAzimuth(offsetX):
    azimuth = np.arctan(offsetX/ focalLen)*180/math.pi #calculates azimuth using objects values
    return (azimuth)

def findAltitude(offsetY):
    altit = np.arctan(offsetY/ focalLen)*180/math.pi #calculates altitude using objects values
    return (altit)
def getRelPos():
	azi_blue_int = 0
	azi_green_int = 0
	alt_blue_int = 0
	alt_green_int = 0
	_, img = cap.read()

	# Converts images from BGR to HSV 
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
	lower_blue = np.array([90,50,50]) 
	upper_blue = np.array([130,255,255]) 
	thresh_blue = cv2.inRange(hsv, lower_blue, upper_blue) 


	lower_green = np.array([30,100,50]) 
	upper_green = np.array([90,255,255]) 
	thresh_green = cv2.inRange(hsv, lower_green, upper_green)


	contours_blue, blah = cv2.findContours(thresh_blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

	count = -1
	for cont in contours_blue: #goes through each contour out of the set, outputted by findContours
			count = count +1
			epsilon = 0.02*cv2.arcLength(cont,True)
			approx = cv2.approxPolyDP(cont, epsilon, True) #approximates a shape out of the contours (orners only)
			if cv2.contourArea(approx) > 100 and len(approx) == 4: #shape has 4 corners and is not extremely small
				approx2 = [approx]
				cv2.drawContours(img, approx2, -1, (255,0,0), 10)
				cv2.drawContours(img, approx, 0, (255,0,0), 10)
				offsetX = float(createTarget(approx)[0] - horizCent)
				offsetY = float(-1*(createTarget(approx)[1]- vertiCent))
				azi_blue_int = findAzimuth(offsetX)
				alt_blue_int = findAltitude(offsetY)
	contours_green, blah = cv2.findContours(thresh_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
	count = -1
	for cont in contours_green: #goes through each contour out of the set, outputted by findContours
			count = count +1
			epsilon = 0.02*cv2.arcLength(cont,True)
			approx = cv2.approxPolyDP(cont, epsilon, True) #approximates a shape out of the contours (orners only)
			if cv2.contourArea(approx) > 100 and len(approx) == 4: #shape has 4 corners and is not extremely small
				approx2 = [approx]
				cv2.drawContours(img, approx2, -1, (0,255,0), 10)
				cv2.drawContours(img, approx, 0, (0,255,0), 10)
				offsetX = float(createTarget(approx)[0] - horizCent)
				offsetY = float(-1*(createTarget(approx)[1]- vertiCent))
				azi_green_int = findAzimuth(offsetX)
				alt_green_int = findAltitude(offsetY)
	cv2.imshow("livefeed",img)
	cv2.imshow("thresh_blue",thresh_blue)
	return azi_green_int-azi_blue_int, alt_green_int-alt_blue_int


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BRIGHTNESS,0)

while(1):
	print(getRelPos())
	'''
	_, img = cap.read()

	# Converts images from BGR to HSV 
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
	lower_blue = np.array([110,100,50]) 
	upper_blue = np.array([130,255,255]) 
	thresh_blue = cv2.inRange(hsv, lower_blue, upper_blue) 


	lower_green = np.array([30,100,50]) 
	upper_green = np.array([90,255,255]) 
	thresh_green = cv2.inRange(hsv, lower_green, upper_green)


	contours_blue, blah = cv2.findContours(thresh_blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

	count = -1
	for cont in contours_blue: #goes through each contour out of the set, outputted by findContours
			count = count +1
			epsilon = 0.02*cv2.arcLength(cont,True)
			approx = cv2.approxPolyDP(cont, epsilon, True) #approximates a shape out of the contours (orners only)
			if cv2.contourArea(approx) > 100 and len(approx) == 4: #shape has 4 corners and is not extremely small
				approx2 = [approx]
				print (cv2.contourArea(approx))
				cv2.drawContours(img, approx2, -1, (255,0,0), 10)
				cv2.drawContours(img, approx, 0, (255,0,0), 10)
				offsetX = float(createTarget(approx)[0] - horizCent)
				offsetY = float(-1*(createTarget(approx)[1]- vertiCent))
				azi_blue_int = findAzimuth()
				alt_blue_int = findAltitude()
				azi_blue = "Blue Azimuth" + str(findAzimuth())
				alt_blue = "Blue Altitude" + str(findAltitude())
				cv2.putText(img, azi_blue, (10, 400 + (0)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 0, 0), 1)
				cv2.putText(img, alt_blue, (10, 400 + (20)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 0, 0), 1)
				print ("azimuth",findAzimuth())
				print ("altitude",findAltitude())

	contours_green, blah = cv2.findContours(thresh_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
	count = -1
	for cont in contours_green: #goes through each contour out of the set, outputted by findContours
			count = count +1
			epsilon = 0.02*cv2.arcLength(cont,True)
			approx = cv2.approxPolyDP(cont, epsilon, True) #approximates a shape out of the contours (orners only)
			if cv2.contourArea(approx) > 100 and len(approx) == 4: #shape has 4 corners and is not extremely small
				approx2 = [approx]
				print (cv2.contourArea(approx))
				cv2.drawContours(img, approx2, -1, (0,255,0), 10)
				cv2.drawContours(img, approx, 0, (0,255,0), 10)
				offsetX = float(createTarget(approx)[0] - horizCent)
				offsetY = float(-1*(createTarget(approx)[1]- vertiCent))
				azi_green_int = findAzimuth()
				alt_green_int = findAltitude()
				azi_green = "Green Azimuth" + str(findAzimuth())
				alt_green = "Green Altitude" + str(findAltitude())
				cv2.putText(img, azi_green, (10, 400 + (40)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 0), 1)
				cv2.putText(img, alt_green, (10, 400 + (60)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 0), 1)
				print ("azimuth",findAzimuth())
				print ("altitude",findAltitude())

	rel_pos_y = azi_green_int-azi_blue_int
	rel_pos_x = alt_green_int-alt_blue_int

	cv2.putText(img, str(rel_pos_y), (10, 400 + (-20)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 255), 1)
	cv2.putText(img, str(rel_pos_x), (10, 400 + (-40)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 255), 1)

	cv2.imshow('live feed',img) 
	cv2.imshow('thresh_blue',thresh_blue)
	cv2.imshow('thresh_green',thresh_green)
	'''
	k = cv2.waitKey(5) & 0xFF
	if k == 27: 
		break
cv2.destroyAllWindows() 
cap.release() 

