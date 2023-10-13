import base64
import json
from flask import (
    Flask, request, make_response, Blueprint, flash
)
import time
import RPi.GPIO as GPIO
import cv2
import picamera2
import numpy as np
import socket
from PIL import Image

from utils import gpio_control, image_process

app = Flask(__name__)
picam2 = picamera2.Picamera2()

PORT = 1234

def main():

    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080), "format": "RGB888"})
    picam2.configure(camera_config)
    picam2.set_controls({"ExposureTime": 5000, "AnalogueGain": 0.1})
    picam2.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]

    gpio_control.lcd.setCursor(0, 0)
    gpio_control.lcd.print(ip_address)
    gpio_control.lcd.setCursor(0, 1)
    gpio_control.lcd.print("PORT: " + str(PORT))
    gpio_control.lcd.display()
    app.run(host='192.168.0.20', port=PORT)

@app.route('/capture_images')
def capture_images():
    img_list = []

    def add_image_to_list(img_list: list):
        frame = np.array(picam2.capture_image())
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_list.append(frame)

    # 불키기
    gpio_control.pixels.fill((0, 255, 0))
    gpio_control.pixels.show()
    GPIO.output(gpio_control.OUT_GPIO_CH, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(gpio_control.OUT_GPIO_CH, GPIO.LOW)

    for i in range(6):
        signal_received = GPIO.wait_for_edge(gpio_control.IN_GPIO_CH, GPIO.RISING, timeout=2500, bouncetime=5)
        if signal_received is None:
            # 불끄기
            gpio_control.pixels.fill((0, 0, 0))
            gpio_control.pixels.show()
            return make_response("Couldn't receive signal from OpenRC board", 408)
        add_image_to_list(img_list)
        cv2.imwrite(f"{i+1}.jpg", img_list[-1])

    gpio_control.pixels.fill((0, 0, 0))
    gpio_control.pixels.show()
    # 이거 좀 async하게 처리할 순 없을까
    # TODO image process
    response_list = []
    for img in img_list:
        response_list.append({})
        response_list[-1]["img"] = image_process.encode_image_to_jpg_base64(img)
        response_list[-1]["count"] = 0

    response_list = json.dumps(response_list)
    GPIO.output(gpio_control.OUT_GPIO_CH, GPIO.LOW)
    return make_response("Done!", 200)

@app.route('/')
def hello():
    return "Hello, world!"

if __name__ == "__main__":
    main()