import RPi.GPIO as GPIO
import time

SENSOR_PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def onMovement(channel):
    print('Movement detected!')

try:
    print "PIR setting up.."
    time.sleep(5)
    # subscribe motion event listener
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=onMovement)
    print "Sensing.."
    # keep code running
    while 1:
        time.sleep(10)
except KeyboardInterrupt:
    print "Exiting.."

GPIO.cleanup()
