import time
import RPi.GPIO as GPIO
import cv2
import picamera2
import numpy as np
from PIL import Image

# Initialize the webcam. 0 indicates the default camera (usually the built-in webcam).
# You can specify a different camera by changing the index.
picam2 = picamera2.Picamera2()

camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)
picam2.start()

OUT_CH = 17
IN_CH = 27

# watch https://www.raspberrypi.com/documentation/computers/raspberry-pi.html for gpio pin mapping
GPIO.setup(OUT_CH, GPIO.OUT)
GPIO.setup(IN_CH, GPIO.IN)

def debounce(last_status: bool):
    curr_status = bool(GPIO.input())
    if (curr_status != last_status):
        time.sleep(5 * 1e-3)
        curr_status = bool(GPIO.input())
    return curr_status

# When RPi gets signal from OpenRC that motor is moved to target angle
# this callback function is called so that RPi captures image from its camera

def add_image_to_list(img_list: list):
    frame = np.array(picam2.capture_image())
    img_list.append(frame)

GPIO.add_event_detect(IN_CH, GPIO.RISING, callback=add_image_to_list)