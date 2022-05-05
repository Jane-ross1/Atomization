#! /usr/bin/env python

# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk

# Import necessary libraries for communication and display use
import RPi.GPIO as GPIO
import drivers
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import Popen
import Adafruit_ADS1x15
import os
import sys
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)


# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()
movie1 = ("/home/pi/lcd/Spray_demonstration.mp4")
GAIN = 2/3

# Main body of code
bp = bool(False)
# Configure
button = 17
pump = 27
valve1 = 6
valve2 = 26
valve3 = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button
GPIO.setup(valve3,GPIO.OUT) #Valve3
GPIO.setup(valve2,GPIO.OUT) #Valve2
GPIO.setup(valve1,GPIO.OUT) #Valve1
GPIO.setup(pump,GPIO.OUT) #Pump

def ReadDispPressure(): #This Function reads and displays the pressure in the pipes
        display.lcd_clear()
        value = [0]
        value[0] = adc.read_adc(0, gain=GAIN)
        volts = value[0]/32767.0*6.144
        psi = 50.0*volts-25.0
        if(psi<0):
            psi = 0
        bar = psi * 0.0689475729
        # Remember that your sentences can only be 16 characters long!
        #print(psi, "psi")
        print("{:.2f} psi".format(psi))
        display.lcd_display_string("Spray Pressure:", 1)  # Write line of text to first line of display
        display.lcd_display_string("{:.2f} psi".format(psi), 2)
        
try:
    while True:
        GPIO.output(pump, GPIO.HIGH) #turn off pump
        display.lcd_backlight(0)     # Turn backlight off

        #ReadDispPressure()
           
        if(GPIO.input(button) == GPIO.LOW):
           bp = bool(True)
           print("\n button pressed")
        while(bp == True):
           display.lcd_backlight(1) # Turn backlight on
           omxc = Popen(['omxplayer', '-b', movie1])    
           sleep(38)
           os.system('killall omxplayer')
           GPIO.output(pump,GPIO.LOW) #turn on pump
           GPIO.output(valve1,GPIO.HIGH) #injector A high pressure?
           GPIO.output(valve2,GPIO.LOW)
           GPIO.output(valve3,GPIO.HIGH)
           sleep(1)
           ReadDispPressure()
           sleep(20)
           GPIO.output(valve1,GPIO.LOW) #injector A low pressure
           sleep(1)
           ReadDispPressure()
           sleep(18) 
           #GPIO.output(valve2,GPIO.HIGH) #delay for switch
           
           sleep(3)
           
           
           # Nozzle 2 Sprays
           GPIO.output(valve1,GPIO.HIGH) #injector B high pressure
           GPIO.output(valve2,GPIO.HIGH)
           GPIO.output(valve3,GPIO.LOW)
           sleep(1)
           #display.lcd_clear()
           ReadDispPressure()
           sleep(20)
           GPIO.output(valve1,GPIO.LOW) #injector B low pressure
           sleep(1)
           #display.lcd_clear()
           ReadDispPressure()
           sleep(20)
           GPIO.output(pump,GPIO.HIGH) #turn pump off
           sleep(1)
           display.lcd_clear()
           sleep(76)
           
           bp = bool(False)
        
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
    os.system('killall omxplayer')
    GPIO.output(pump,GPIO.HIGH) #turn pump off
