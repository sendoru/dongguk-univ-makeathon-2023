import time
import RPi.GPIO as GPIO
import cv2
import numpy as np
from PIL import Image
import board
import neopixel
from liquidcrystal_i2c import LCD

OUT_GPIO_CH = 22
IN_GPIO_CH = 23

# watch https://www.raspberrypi.com/documentation/computers/raspberry-pi.html for gpio pin mapping
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(OUT_GPIO_CH, GPIO.OUT)
GPIO.setup(IN_GPIO_CH, GPIO.IN)

# https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring
pixel_pin = board.D18
num_pixels = 4
pixels = neopixel.NeoPixel(
pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.RGB
)

# https://pypi.org/project/liquidcrystal-i2c-linux/
# GROUND, 5V는 핀맵보고 알아서 꽃으면 됨
# SDA는 3번, SCL은 5번 핀
lcd = LCD(bus=1, addr=0x27, cols=16, rows=2)

def debounce(last_status: bool):
    curr_status = bool(GPIO.input())
    if (curr_status != last_status):
        time.sleep(5 * 1e-3)
        curr_status = bool(GPIO.input())
    return curr_status

# When RPi gets signal from OpenRC that motor is moved to target angle
# this callback function is called so that RPi captures image from its camera