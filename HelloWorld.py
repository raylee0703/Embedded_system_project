from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import dht11
import time
import datetime
from mq import *
import sys
from gtts import gTTS
import os


sys.path.insert(1, '../function_tests/object_detection')
# import newObject_detection_picamera

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

speaker_pin = 12
alarm_port = 15 # from security cam
web_port = 18 # from self

GPIO.setmode(GPIO.BOARD)
GPIO.setup(speaker_pin,GPIO.OUT)
GPIO.setup(web_port,GPIO.OUT)
GPIO.setup(alarm_port, GPIO.IN)

# read data using pin 
instance = dht11.DHT11(pin=7)
app = Flask(__name__)

hum = 0
temp = 0

mq = MQ()

co = 0
co2 = 0
alcohol = 0
alr = 0
botton = 'activate'

@app.route('/', methods=['GET'])
def index():
    #global hum, temp
    #global alarm_port
    #alr = GPIO.input(alarm_port)
    #global mq
    #global alr
    global botton

    #now = datetime.datetime.now()
    #timeString = now.strftime("%Y-%m-%d %H:%M:%S")

    #### TEMPERATURE + HUMIDITY
    #result = instance.read()
    #alr = GPIO.input(alarm_port)
    #if result.humidity != 0:
    #  hum = result.humidity
    #  temp = result.temperature
    #hum = 0.1
    #temp = 0.1

    #### AIR QUALITY PART
    #perc = mq.MQPercentage()
    #co2 = round(perc["GAS_CO2"], 4)
    #co = round(perc["CO"], 4)
    #alcohol = round(perc["ALCOHOL"], 4)

    #### SECURITY SYSTEM PART
    bottonn = request.values.get('act')
    print(botton)
    if bottonn == 'activate':
        botton = 'deactivate'
        GPIO.output(web_port, GPIO.HIGH)
    elif bottonn == 'deactivate':
        botton = 'activate'
        GPIO.output(web_port, GPIO.LOW)
        #alr = 0

    #alrm = ""
    #if alr:
        #alrm = 'alert("Intruder detected")'


    #### VOICE ASSISTANT
    # request.form['make_report']

    #### INFORMATION BUNDLE FOR BACKEND
    templateData = {
        #'time' : timeString,
        #'humidity' : hum,
        #'temperature': temp,
        #'co2': co2,
        #'co': co,
        #'alcohol': alcohol,
        'activate' : botton,
        #'alarm' : alr
      }
    return render_template('iot.html', **templateData)

# @app.route('/audio_report')
# def audio_report():
#     print("Received button click")
@app.route('/audio_report')
def audio_report():
    report_string = "The temperature is now " + str(temp) + " degrees" + "The humidity is now" + str(hum) + "percent"
    tts = gTTS(text=report_string, lang='en')
    tts.save('weather.mp3')
    os.system('mpg123 weather.mp3 > /dev/null 2>&1')
    print("Hello")
    return ("nothing")

@app.route('/time_page')
def timefunc():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M:%S")
    return timeString

@app.route('/humidity')
def humfunc():
    global hum
    return str(hum)

@app.route('/temperature')
def tempfunc():
    global hum, temp
    result = instance.read()
    #alr = GPIO.input(alarm_port)
    if result.humidity != 0:
        hum = result.humidity
        temp = result.temperature
    return str(temp)

@app.route('/co')
def cofunc():
    global co
    return str(co)

@app.route('/co2')
def co2func():
    global co2
    return str(co2)

@app.route('/alch')
def alfunc():
    global mq, co, co2, alcohol
    perc = mq.MQPercentage()
    co2 = round(perc["GAS_CO2"], 4)
    co = round(perc["CO"], 4)
    alcohol = round(perc["ALCOHOL"], 4)
    return str(alcohol)

btstate = False
@app.route('/alarm_page')
def alrfunc():
    global alarm_port, botton, btstate
    alr = GPIO.input(alarm_port)
    print(alr)
    print(botton)
    if botton == 'activate':
        btstate = False
    elif botton == 'deactivate':
        btstate = True
    if not btstate:
        alr = 0

    print(btstate)
    return str(alr)

if __name__ == '__main__':
    #hum = 0
    #temp = 0
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(debug=True, port=80, host='0.0.0.0')