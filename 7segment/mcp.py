from gpiozero import MCP3008
import RPi.GPIO as GPIO
from time import sleep

# BOARD: 37 35 33 31 

#MODE BCM
a1, b1 ,c1, d1 = 26, 19 ,13 ,6
a2, b2, c2, d2 = 0, 0, 0, 0

GPIO.setwarnings(False)

GPIO.setup([a1, b1, c1, d1], GPIO.OUT)
GPIO.setup([a2, b2, c2, d2], GPIO.OUT)

outp = {'00':[1,1,1,1],
	0: [0,0,0,0],
	1: [1,0,0,0],
	2: [0,1,0,0],
	3: [1,1,0,0],
	4: [0,0,1,0],
	5: [1,0,1,0],
	6: [0,1,1,0],
	7: [1,1,1,0],
	8: [0,0,0,1],
	9: [1,0,0,1]}
	
vref = 5
ch = 0
ch0 = 0

while True:
	with MCP3008(channel=ch) as reading:
		ch0 = reading.value * vref
		
	decimals = int(str(ch0)[2:])		
	x = 12
	xr = (74-12)/99
	if decimals >= x:
		for i in range(1,100):
			if((decimals - x)<0.1):
				if i > 9:
					digit1, digit12 = outp[(i//10)], outp[(i%10)]
				else if i < 10:
					digit1, digit12 = outp[0], outp[i]
				else:
					digit1 = digit12 = outp[9]
				break
			x += xr
	else:
		digit1 = digit12 = outp[0]
		
	print(ch0)
	
	GPIO.output([a1, b1, c1, d1], outp[digit1])
	GPIO.output([a2, b2, c2, d2], outp[digit12])
