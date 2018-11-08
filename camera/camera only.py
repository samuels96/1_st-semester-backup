import time
import os
import RPi.GPIO as GPIO
import numpy as np
import cv2

en1, m1f, m1b = 7, 5, 3
en2, m2f, m2b = 15, 13, 11
en3, m3f, m3b = 37, 35, 33
en4, m4f, m4b = 40, 38, 36
all_outputs = [en1, m1f, m1b, en2, m2f, m2b, en3, m3f, m3b, en4, m4f, m4b]

left, mid, right = 23, 19, 21 

GPIO.setmode(GPIO.BOARD)                             
GPIO.setwarnings(False)                              
GPIO.setup(all_outputs, GPIO.OUT)
GPIO.setup([left, mid, right], GPIO.IN)                             

lm1 = GPIO.PWM(m1f, 100)
lm2 = GPIO.PWM(m3f, 100)                

rm1 = GPIO.PWM(m2f, 100)                           
rm2 = GPIO.PWM(m4f, 100)


def start():
	GPIO.output(all_outputs, 1)
	
def stop():
	GPIO.output(all_outputs, 0)
	GPIO.cleanup()



def get_status():
	return str(GPIO.input(left)) + str(GPIO.input(mid)) + str(GPIO.input(right))

def getError(error):
	global c
	# if error == '111' or error == '000':
		# c+= 1
		# return 0
	# else:
		# c = 0
			
	if(error == '100'):
		error = 20
	elif(error == '001'):			#001
		error = -20
	elif error == '011':
		error = -20
	elif error == '110':
		error = 20
	elif error == '101':
		error = 0
	else:		
		error = 0
	
	return error

def run(speed_left, speed_right):
	ds = 100
	if(speed_left > 0):
			GPIO.output(m1f, 1)    
			GPIO.output(m1b, 0)
			GPIO.output(m3f, 1)     
			GPIO.output(m3b, 0)   

			lm1.start(ds)  
			lm2.start(ds if speed_left > 100 else speed_left)     

	else:				
			GPIO.output(m1f, 0)       
			GPIO.output(m1b, 1)    
			GPIO.output(m3f, 0)        
			GPIO.output(m3b, 1)     
			
			lm1.start(ds)  
			lm2.start(ds if speed_left < -100 else -speed_left)                  
			  
	if(speed_right > 0):
			GPIO.output(m2f, 1)       
			GPIO.output(m2b, 0)     		
			GPIO.output(m4f, 1)       
			GPIO.output(m4b, 0)  
			
			rm1.start(ds)      
			rm2.start(ds if speed_right > 100 else speed_right)                  

	else:		
			GPIO.output(m2f, 0)       
			GPIO.output(m2b, 1)   
			GPIO.output(m4f, 0)     
			GPIO.output(m4b, 1)  

			rm1.start(ds)   
			rm1.start(100 if dcr<= 100 else dcr*(-1))
			rm2.start(ds if speed_right < -100 else -speed_right)     

					
def loop():		
	Kp, Ki, Kd = 220, 30, 15	
	dT = 0.000435   		
	offset = -0.476         
	Tp = 150
	derivative = 0
	lastError = 0
	integral, integral_max, integral_min = 0, 20, -20

	global c
	c = 0
	
	video_capture = cv2.VideoCapture(-1)
	video_capture.set(3, 160)
	video_capture.set(4, 120)
		
	while True:
		
		# status = get_status()
		ret, frame = video_capture.read()
		crop_img = frame[60:120, 0:160]

		gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray,(5,5),0)
		ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
		x,contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
		
		if len(contours) > 0:
			c = max(contours, key=cv2.contourArea)
			M = cv2.moments(c)

			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])

			cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
			cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

			cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
			if cx >= 120:
				status = '110'
			elif cx < 120 and cx > 50:
				status = '111'
			elif cx <= 50:
				status = '011'
			else:
				status = '010'
		else:
			status = '010'
				
		error = getError(status) - offset
		
		integral += error * dT
		
		if(integral > integral_max):
		    integral = integral_max
		    
		elif(integral < integral_min):
		    integral = integral_min
		                                    
		derivative = (error - lastError)/dT
		
		
		Turn = Kp*error + Ki*integral + Kd*derivative

		run(Tp + Turn, Tp - Turn)
		lastError = error
		
		
def main():
	start()
	try:			
		loop()					
	except:
		stop()
		GPIO.cleanup()
	
main()