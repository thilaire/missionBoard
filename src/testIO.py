import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

inputs = [2,3,4,17,22,27,5,6,14,15,18,7,12]
for gpio in inputs:
	GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	#GPIO.add_event_detect(gpio, GPIO.BOTH, callback=lambda x: print(x,gpio))

while True:
	print({gpio: GPIO.input(gpio) for gpio in inputs})
	sleep(0.2)
