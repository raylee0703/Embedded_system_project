from gtts import gTTS
import os
import dht11
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

instance = dht11.DHT11(pin=7)
result = instance.read()


hum = result.humidity
temp = result.temperature

report_string = "The temperature is now " + str(temp) + " degrees"

tts = gTTS(text=report_string, lang='en')
tts.save('weather.flac')

os.system('omxplayer -o local -p weather.flac > /dev/null 2>&1')
