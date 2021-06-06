import sys
import os
import signal
import time
import RPi.GPIO as GPIO

CLOCK_PIN = 27
PULSE_PIN = 22
BOUNCE_TIME = 30
sqwave=True


def isr(channel):
    if channel != CLOCK_PIN:
        return
    print("isr called!")
    sqwave = not GPIO.input(PULSE_PIN)

    # set pulse pin low before changing it to input to look for shutdown signal
    GPIO.output(PULSE_PIN, False)
    GPIO.setup(PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if not GPIO.input(PULSE_PIN):
        print("Pulse pin high")
        print("Lost power supply, Pi will shutdown")
        time.sleep(2)
        os.system('/sbin/shutdown -h now')
    else:
        print("pulse pin low")
    GPIO.setup(PULSE_PIN, GPIO.OUT, initial=sqwave)



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CLOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PULSE_PIN, GPIO.OUT, initial=sqwave)
GPIO.add_event_detect(CLOCK_PIN, GPIO.FALLING, callback=isr, bouncetime=BOUNCE_TIME)

while True:
    try:
        time.sleep(1)
    except:
        exit(0)
