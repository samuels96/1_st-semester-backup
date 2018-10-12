
import sys
import time
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

	left = 23 #LEFT
	mid = 19 #MIDDLE
	right = 21 #RIGHT

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup([en1, m1f, m1b], GPIO.OUT) 
	GPIO.setup([en2, m2f, m2b], GPIO.OUT)
	GPIO.setup([en3, m3f, m3b], GPIO.OUT)
	GPIO.setup([en4, m4f, m4b], GPIO.OUT)
	GPIO.setup([mid,left,right], GPIO.IN) 

	m1 = GPIO.PWM(m1f, 100)
	m2 = GPIO.PWM(m2f, 100)
	m3 = GPIO.PWM(m3f, 100)
	m4 = GPIO.PWM(m4f, 100)

	m1.start(100)
	m2.start(100)
	m3.start(100)
	m4.start(100)

	ds = 100

	change = False
	
	GPIO.output([en1, en2, en3, en4], 1)
	GPIO.add_event_detect(left, GPIO.RISING, callback=c_left, bouncetime=10)
	GPIO.add_event_detect(right, GPIO.RISING, callback=c_right, bouncetime=10)
	GPIO.add_event_callback(left, change)
	GPIO.add_event_callback(right, change)
	

def change(x=0):
	global change
	change = not change
	
def c_left(x=0):
	global speed_left
	global speed_right

	speed_left = ds

	while GPIO.input(left):
		speed_right = ds if not GPIO.input(mid) else 0
		pass

	speed_left = 50

def c_right(x=0):
    global speed_left
    global speed_right
	
    speed_right = ds
	
    while GPIO.input(right):
        speed_left = ds if not GPIO.input(mid) else 0
        pass

    speed_right = 50

    
def c_mid(x=0):
    pass
    
def main():
	while True:
		if change:
			m1.ChangeDutyCycle(speed_left)
			m3.ChangeDutyCycle(speed_left)
			m2.ChangeDutyCycle(speed_right)
			m4.ChangeDutyCycle(speed_right)
try:
	setup()
	main()
except:
    GPIO.cleanup()

