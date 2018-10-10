import sys
import time
import RPi.GPIO as GPIO

en1 = 7
m1f = 5
lm1b = 3

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
GPIO.setup([en1, m1f, lm1b, en2, m2f, m2b, en3, m3f, m3b, en4, m4f, m4b], GPIO.OUT) 
GPIO.setup([mid,left,right], GPIO.IN) 

lm1 = GPIO.PWM(m1f, 100)
lm2 = GPIO.PWM(m3f, 100)

rm1 = GPIO.PWM(m2f, 100)
rm2 = GPIO.PWM(m4f, 100)

lm1.start(100)
rm1.start(100)

lm2.start(100)
rm2.start(100)

max_speed = 65

speed_left = max_speed
speed_right = max_speed

def c_left(x=0):
	global speed_left
	global speed_right
	speed_left = max_speed

	while GPIO.input(left):
		speed_right = max_speed if not GPIO.input(mid) else 0

	speed_left = max_speed//1.4

def c_right(x=0):
	global speed_left
	global speed_right

	speed_right = max_speed

	while GPIO.input(right):
		speed_left = max_speed if not GPIO.input(mid) else 0

	speed_right = max_speed//1.4


def loop():
	global speed_left
	global speed_right

	GPIO.output([en1, en2, en3, en4], 1)
	GPIO.add_event_detect(left, GPIO.RISING, callback=c_left, bouncetime=1)
	GPIO.add_event_detect(right, GPIO.RISING, callback=c_right, bouncetime=1)

	while True:
		lm1.ChangeDutyCycle(speed_left)
		rm1.ChangeDutyCycle(speed_right)
		lm2.ChangeDutyCycle(speed_left)
		rm2.ChangeDutyCycle(speed_right)

try:
    loop()
except:
    GPIO.cleanup()

