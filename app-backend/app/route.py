from app import app
from utils import gpio_control
from flask import (
    Flask, request, make_response, Blueprint, flash
)

import time
import RPi.GPIO as GPIO
import cv2
import picamera2
import numpy as np
from PIL import Image

@app.route('/capture_images', methods=['GET'])
def capture_images():
    images = []
    def add_image_to_list(img_list: list):
        frame = np.array(picam2.capture_image())
        img_list.append(frame)
    GPIO.output(gpio_control.OUT_CH, GPIO.HIGH)
    GPIO.add_event_detect(gpio_control.IN_CH, GPIO.RISING, callback=add_image_to_list)
    time.sleep(0.01)

    return make_response("Not implemented", 501)