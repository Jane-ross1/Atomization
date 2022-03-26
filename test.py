import RPi.GPIO as GPIO
import time
import os
import sys
from subprocess import Popen


movie1 = ("/home/pi/Videos/low_side_view.mp4")

GPIO.setmode(GPIO.BOARD)
#configure pinout
button = 13
valveA = 29
valveB = 31
#valveC = 33
pump = 37

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#configure valves (2 out of 3)
GPIO.setup(valveA, GPIO.OUT) #valve 1
GPIO.setup(valveB, GPIO.OUT) #valve 2
# GPIO.setup(valveC, GPIO.OUT) #valve 3
GPIO.setup(pump, GPIO.OUT) #pump

if button == high:
omxc = Popen(['omxplayer', '-b', movie1])

def lowPressure(channel):
    print ("falling edge on 11")
    print ("pump on")
    GPIO.output(16,GPIO.HIGH)#close valve
    GPIO.output(18,GPIO.HIGH)#close valve
    GPIO.output(22,GPIO.LOW)#turn on pump
    omxc = Popen(['omxplayer', '-b', movie1])
    time.sleep(13)
    os.system('killall omxplayer')
    GPIO.output(22,GPIO.HIGH)#turn off pump
    print ("pump off")
    
    
   

def mediumPressure(channel):
    print ("falling edge on 13")
    print ("pump on")
    GPIO.output(16,GPIO.HIGH)#close valve
    GPIO.output(18,GPIO.LOW)#open valve
    GPIO.output(22,GPIO.LOW)#turn on pump
    omxc = Popen(['omxplayer', '-b', movie2])
    time.sleep(13)
    os.system('killall omxplayer')
    GPIO.output(22,GPIO.HIGH)#turn off pump
    GPIO.output(16,GPIO.HIGH)#close valve
    GPIO.output(18,GPIO.HIGH)#close valve
    print ("pump off")


def highPressure(channel):
    print ("falling edge on 15")
    print ("pump on")
    GPIO.output(16,GPIO.LOW)#open valve
    GPIO.output(18,GPIO.LOW)#open valve
    GPIO.output(22,GPIO.LOW)#turn on pump
    omxc = Popen(['omxplayer', '-b', movie3])
    time.sleep(13)
    os.system('killall omxplayer')
    GPIO.output(22,GPIO.HIGH)#turn off pump
    GPIO.output(16,GPIO.HIGH)#close valve
    GPIO.output(18,GPIO.HIGH)#close valve
    print ("pump off")

GPIO.output(pump,GPIO.HIGH)#turn off pump
GPIO.output(valveA,GPIO.HIGH)#close valve
GPIO.output(valveB,GPIO.HIGH)#close valve
# GPIO.output(valveC, GPIO.HIGH) #close valve
GPIO.add_event_detect(11, GPIO.RISING, callback=lowPressure, bouncetime=300)
GPIO.add_event_detect(13, GPIO.RISING, callback=mediumPressure, bouncetime=300)
GPIO.add_event_detect(15, GPIO.RISING, callback=highPressure, bouncetime=300)

#while 1:
 #   time.sleep(0.1)

GPIO.cleanup()
