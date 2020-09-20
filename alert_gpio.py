import RPi.GPIO as GPIO
import time 
import os


speaker_pin = 12
control_pin = 15
web_pin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(speaker_pin,GPIO.OUT)
GPIO.setup(control_pin, GPIO.IN)
GPIO.setup(web_pin, GPIO.IN)

is_shout = False

try:
	while True:
		#a = GPIO.input(control_pin)
		#if a == 1:
		#   GPIO.output(speaker_pin, GPIO.HIGH)
		#else:
		#   GPIO.output(speaker_pin, GPIO.LOW)
		if GPIO.input(control_pin):
			is_shout = True
		if not GPIO.input(web_pin):
			is_shout = False

		if is_shout:
			os.system('omxplayer -o local -p hello.mp3 > /dev/null 2>&1')
		print(GPIO.input(control_pin), is_shout, GPIO.input(web_pin))
		GPIO.output(speaker_pin, (GPIO.input(control_pin) or is_shout) and GPIO.input(web_pin))
		time.sleep(0.0001)
		GPIO.output(speaker_pin, GPIO.LOW)
		time.sleep(0.0001)
		
except KeyboardInterrupt:
	print("Cleanup")
	
finally:
	GPIO.cleanup()