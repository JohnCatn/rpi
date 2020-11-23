#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
from time import sleep
import pygame.mixer

# SETUP
MIN_DIST = 50.00 ## The distance from the sensor the LED should be brightest
MAX_DIST = 100.00 # The distance from the sensor the LED should be on

GPIO.setmode(GPIO.BCM) # Use board numbers

PIN_TRIGGER = 4
PIN_ECHO = 17
PIN_NOSE = 18

# Set up distanc sensor
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)

# Set up nose LED
GPIO.setup(PIN_NOSE, GPIO.OUT) 
nose_led = GPIO.PWM(PIN_NOSE, 100) # create object white for PWM on GPIO port 25 (pin 22) at 100 Hertz
nose_led.start(0)              # start white led on 0 percent duty cycle (off)
# now the fun starts, we'll vary the duty cycle to   
# dim/brighten the led  

# Set up Audio
said_hello = False
playing = False

pygame.mixer.init(44100,-16,2,1024)
pygame.mixer.music.set_volume(1.0)
name = "rudolph.mp3"
pygame.mixer.music.load(name)
print("Loaded track - "+ str(name))

# Sets the brightness of the nose LED
def set_nose_brightness(dist_in_cm):
      if dist_in_cm < MAX_DIST:
            say_hello()
            if dist_in_cm < MIN_DIST:
                  nose_led.ChangeDutyCycle(100)
            else:
                  # Value can be between 0 and 100, we want 100 when it is at the min distance so use percentage calc
                  duty_cycle = (1 - ((dist_in_cm - MIN_DIST) / (MAX_DIST - MIN_DIST))) * 100
                  print("Duty Cycle: ",duty_cycle)
                  nose_led.ChangeDutyCycle(duty_cycle)
      else: # too far away turn LED Off
            print("nothing in range - LED off")
            nose_led.ChangeDutyCycle(0)  

def say_hello():
      global said_hello, playing
      if said_hello == False and playing == False:
            playing=True
            pygame.mixer.music.play()
            said_hello=True
            playing=False
      
def distance()
      print ("Calculating distance")

      GPIO.output(PIN_TRIGGER, GPIO.HIGH)
      sleep(0.00001)
      GPIO.output(PIN_TRIGGER, GPIO.LOW)
      pulse_end_time = 0
      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      distance = round(pulse_duration * 17150, 2)

      return distance

if __name__ == '__main__':
      # INITIALIZE
      print ("Waiting for sensor to settle")

      sleep(2)

      try:
            while True:
                  dist = distance()
                  print ("Measured Distance = %.1f cm" % dist)
                  set_nose_brightness(distance)
                  say_hello()
                  time.sleep(1)
      
            # Reset by pressing CTRL + C
      except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
