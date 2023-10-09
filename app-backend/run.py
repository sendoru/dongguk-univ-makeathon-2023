import json
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

picam2 = picamera2.Picamera2()

camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)
picam2.start()

app = Flask()

GPIO.setup(gpio_control.OUT_CH, GPIO.OUT)
GPIO.setup(gpio_control.IN_CH, GPIO.IN)

@app.route('/capture_images', methods=['GET'])
async def capture_images():
    img_list = []

    def add_image_to_list(img_list: list):
        frame = np.array(picam2.capture_image())
        img_list.append(frame)
    GPIO.output(gpio_control.OUT_CH, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(gpio_control.OUT_CH, GPIO.LOW)
    for i in range(8):
        signal_received = GPIO.wait_for_edge(gpio_control.IN_CH, GPIO.RISING, timeout=5000, bouncetime=1)
        add_image_to_list(img_list)

    # 이거 좀 async하게 처리할 순 없을까
    # TODO image process
    response_list = []
    for img in img_list:
        response_list.append({})
        response_list[-1]["img"] = cv2.imencode('.jpg', img)
        response_list[-1]["count"] = 0
        response_list[-1] = json.dump(response_list[-1])

    
    return make_response(response_list, 200)

if __name__ == "__main__":
    app.run(host='localhost', port=1234, debug=True)
    