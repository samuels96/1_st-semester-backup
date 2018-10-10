import time
import os
import RPi.GPIO as GPIO

def setup():
		
	en1 = 7
	m1f = 5
	m1b = 3

	en2 = 15
	m2f = 13
	m2b = 11

	en3 = 37
	m3f = 35
	m3b = 33

	en4 = 40
	m4f = 38
	m4b = 36
	
	all_outputs = [en1, m1f, m1b, en2, m2f, m2b, en3, m3f, m3b, en4, m4f, m4b]
	
	left = 23 #LEFT
	mid = 19 #MIDDLE
	right = 21 #RIGHT

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
		sensors = [GPIO.input(left), GPIO.input(mid), GPIO.input(right)]
		error = str(sensors[0]) + str(sensors[1]) + str(sensors[2])

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
				GPIO.output(m1f, GPIO.HIGH)    
				GPIO.output(m1b, GPIO.LOW)
				
				lm1.start(100)            
				
				GPIO.output(m3f, GPIO.HIGH)     
				GPIO.output(m3b, GPIO.LOW)   
				
				lm2.start(100 if speed_left > 100 else speed_left)     
		
		else:				
				GPIO.output(m1f, GPIO.LOW)       
				GPIO.output(m1b, GPIO.HIGH)    
				
				lm1.start(100)                 

				GPIO.output(m3f, GPIO.LOW)        
				GPIO.output(m3b, GPIO.HIGH)     
				
				lm2.start(100 if speed_left <= 100 else speed_left * (-1))                  
							
		if(speed_right > 0):
				GPIO.output(m2f, GPIO.HIGH)       
				GPIO.output(m2b, GPIO.LOW)     
				
				rm1.start(100)                 

				GPIO.output(m4f, GPIO.LOW)       
				GPIO.output(m4b, GPIO.HIGH)  
				
				rm2.start(100 if speed_right > 100 else speed_right)                  

		else:		
				GPIO.output(m2f, GPIO.LOW)       
				GPIO.output(m2b, GPIO.HIGH)   
				
				rm1.start(100)             

				GPIO.output(m2f, GPIO.HIGH)     
				GPIO.output(m2b, GPIO.LOW)  
				
				rm2.start(100 if speed_right < -100 else speed_right *(-1))             

def loop():

		Kp = 75             
		Ki = 0							      
		Kd = 0							
		dT = 0.000435           		
		offset = -0.476         
		Tp = 1000               		
		integral = 0
		integral_max = 20
		integral_min = -20
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
	