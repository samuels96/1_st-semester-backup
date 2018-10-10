import time
import os
import RPi.GPIO as GPIO

def setup():
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

	lm1 = GPIO.PWM(m1f, 50)                               
	lm2 = GPIO.PWM(m3f, 50)                      
	
	rm1 = GPIO.PWM(m2f, 50)                           
	rm2 = GPIO.PWM(m4f, 50)                                      

def stop():
	GPIO.output(all_outputs, 0)

def getError():

	error = str(GPIO.input(left)) + str(GPIO.input(mid)) + str(GPIO.input(right))
	
	if(error == '111'):				#000
		error = 0
	elif(error == '110'):			#001
		error = 15
	elif(error == '101'):			#010
		error = 0
	elif(error == '100'):			#011
		error = 1
	elif(error == '011'):			#100
		error = -15
	elif(error == '010'):			#101
		error = 0
	elif(error == '001'):			#110
		error = -1
	elif(error == '000'):			#111
		error = 0   

	return error

def run(speed_left, speed_right):
	if(speed_left > 0):
			GPIO.output(m1f, 1)    
			GPIO.output(m1b, 0)
			GPIO.output(m3f, 1)     
			GPIO.output(m3b, 0)   
			
			lm1.start(100)  
			lm2.start(100 if speed_left > 100 else speed_left)     

	else:				
			GPIO.output(m1f, 0)       
			GPIO.output(m1b, 1)    
			GPIO.output(m3f, 0)        
			GPIO.output(m3b, 1)     
			
			lm1.start(100)  
			lm2.start(100 if speed_left < -100 else speed_left * (-1))                  
			  
	if(speed_right > 0):
			GPIO.output(m2f, 1)       
			GPIO.output(m2b, 0)     		
			GPIO.output(m4f, 1)       
			GPIO.output(m4b, 0)  
			
			rm1.start(100)      
			rm2.start(100 if speed_right > 100 else speed_right)                  

	else:		
			GPIO.output(m2f, 0)       
			GPIO.output(m2b, 1)   
			GPIO.output(m4f, 0)     
			GPIO.output(m4b, 1)  
			
			rm1.start(100)   
			rm2.start(100 if speed_right < -100 else speed_right *(-1))             

def loop():
	Kp, Ki, Kd = 75, 0 ,0				
	dT = 0.000435           		
	offset = -0.476         
	Tp = 1000               		
	integral, integral_max, integral_min = 0, 20, -20
	lastError = 0
	derivative = 0

	while True:
		error = getError()
		error = error - offset
		integral = integral + error * dT
		
		if(integral > integral_max):
			integral = integral_max
			
		elif(integral < integral_min):
			integral = integral_min
							
		derivative = (error - lastError)/dT
		
		Turn = Kp*error + Ki*integral + Kd*derivative
		
		run(Tp + Turn, Tp - Turn)
		
		lastError = error
		
try:
	setup()				
	loop()					
except:
	stop()
	GPIO.cleanup()
	