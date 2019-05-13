import gphoto2 as gp
import RPi.GPIO as GPIO
import time
import os

# kill any existing gphoto2 processes
os.system('pkill -f gphoto2')

# connect to camera
context = gp.gp_context_new()
camera = gp.check_result(gp.gp_camera_new())
print('Connecting to camera..')
while True:
    try:
        camera.init(context)
    except gp.GPhoto2Error as ex:
        print('Please connect and switch on your camera')
        if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
            # no camera, try again in 2 seconds
            time.sleep(2)
            continue
        # some other error we can't handle here
        raise
    # operation completed successfully so exit loop
    break

# handle on movement event, triggering the camera
def onMovement(channel):
    print('Movement detected')
    gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE)

# setup GPIO listener triggering the camera when PIR senses movement
SENSOR_PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

try:
    print("PIR setting up..")
    time.sleep(5)
    # subscribe motion event listener
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=onMovement)
    print("Sensing..")
    # keep code running
    while 1:
        time.sleep(10)
except KeyboardInterrupt:
    print("Exiting..")

GPIO.cleanup()
