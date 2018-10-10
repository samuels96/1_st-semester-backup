
import sys
import time
import RPi.GPIO as GPIO

#MOTOR 1 F
en1 = 7
m1f = 5
m1b = 3

#MOTOR 1 RIGHT
en2 = 15
m2f = 13
m2b = 11

#MOTOR 2 LEFT
en3 = 37
m3f = 35
m3b = 33

#MOTOR 2 RIGHT
en4 = 40
m4f = 38
m4b = 36

#SENSORS
left = 23 #LEFT
mid = 19 #MIDDLE
right = 21 #RIGHT

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)

	GPIO.setup([en1, m1f, m1b, en2, m2f, m2b, en3, m3f, m3b, en4, m4f, m4b], GPIO.OUT)  #set all of the motors as OUTPUT
	GPIO.setup([mid,left,right], GPIO.IN) #set all of the sensors as INPUT
	
def init_pwm():
	#set all the motors forward as a pwm with frequency of 100
	m1 = GPIO.PWM(m1f, 100) 
	m2 = GPIO.PWM(m2f, 100) 
	m3 = GPIO.PWM(m3f, 100) 
	m4 = GPIO.PWM(m4f, 100) 
	
	#variable holding default duty cycle for PWMs, ds stands for default speed
	ds = 50

	#start all the motors with duty cycle of 50
	m1.start(ds)
	m2.start(ds)
	m3.start(ds)
	m4.start(ds)



def loop():
		
		#initialize variables that will hold the values of each individual motor duty cycle, set to ds as a default
        m1v = m2v = m3v = m4v = ds
		state = 0
		
        while True:
			# If at least one of the sensors get triggered, enable motors and enter the tracking functions
            if  not GPIO.input(left) or not GPIO.input(mid) or not GPIO.input(right):
				
				if state == 0:
					GPIO.output([en1, en2, en3, en4], 1)
					state = 1
				
                # print(m1v,m3v,m2v,m4v)
		
                if not GPIO.input(left):
                    if m1v == ds and m3v == ds:
                        # print("LEFT SLOW")
                        m1.ChangeDutyCycle(ds//2)
                        m3.ChangeDutyCycle(ds//2)
                        m1v = m3v = ds//2
                    
                if GPIO.input(left):
                    if m1v != ds and m3v != ds:
                        # print("GET speed back LEFT")
                        m1.ChangeDutyCycle(ds)
                        m3.ChangeDutyCycle(ds)
                        m1v = m3v = ds

                if not GPIO.input(right):                    
                    if m2v == ds and m4v == ds:
                        # print("RIGHT SLOW")
                        m2.ChangeDutyCycle(ds//2)
                        m4.ChangeDutyCycle(ds//2)
                        m2v = m4v = ds//2

                if GPIO.input(right):
                    if m2v != ds and m4v != ds:
                        # print("GET speed back RIGHT")
                        m2.ChangeDutyCycle(ds)
                        m4.ChangeDutyCycle(ds)
                        m2v = m4v = ds
            else:
				if state == 1:
					GPIO.output([en1, en2, en3, en4], 0)

def main():

	setup()
	init_pwm()

	try:
		loop()
	except:
		GPIO.cleanup()

