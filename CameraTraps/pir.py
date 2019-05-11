import RPi.GPIO as GPIO
import time

SENSOR_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def onMovement(channel):
    print('Movement detected!')

try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=onMovement)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print "Exiting.."
GPIO.cleanup()