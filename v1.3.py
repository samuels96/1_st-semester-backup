import sys
import time
import RPi.GPIO as GPIO

def setup():
	en1, m1f, m1b = 7, 5, 3
	en2, m2f, m2b = 15, 13, 11
	en3, m3f, m3b = 37, 35, 33
	en4, m4f, m4b = 40, 38, 36
	all_outputs = [en1, m1f, m1b, en2, m2f, m2b, en3, m3f, m3b, en4, m4f, m4b]
	all_enable = [en1, en2, en3, en4]

	left, mid, right = 23, 19, 21 

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup([all_outputs], GPIO.OUT) 
	GPIO.setup([mid,left,right], GPIO.IN) 

	lm1 = GPIO.PWM(m1f, 100)
	lm2 = GPIO.PWM(m3f, 100)
	rm1 = GPIO.PWM(m2f, 100)
	rm2 = GPIO.PWM(m4f, 100)

	lm1.start(100)
	rm1.start(100)
	lm2.start(100)
	rm2.start(100)

	global max_speed
	global speed_left
	global speed_right

	max_speed = 65
	speed_left = max_speed
	speed_right = max_speed

def change_left(x=0):
	global speed_left
	global speed_right
	
	speed_left = max_speed

	while GPIO.input(left):
		speed_right = max_speed if not GPIO.input(mid) else 0

	speed_left = max_speed//1.4

def change_right(x=0):
	global speed_left
	global speed_right

	speed_right = max_speed

	while GPIO.input(right):
		speed_left = max_speed if not GPIO.input(mid) else 0
		
	speed_right = max_speed//1.4


def loop():
	GPIO.output(all_enable, 1)
	GPIO.add_event_detect(left, GPIO.RISING, callback=change_left, bouncetime=1)
	GPIO.add_event_detect(right, GPIO.RISING, callback=change_right, bouncetime=1)

	while True:
		lm1.ChangeDutyCycle(speed_left)
		lm2.ChangeDutyCycle(speed_left)
		rm1.ChangeDutyCycle(speed_right)
		rm2.ChangeDutyCycle(speed_right)

try:
	setup()
    loop()
except:
    GPIO.cleanup()

