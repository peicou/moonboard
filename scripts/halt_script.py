#!/usr/bin/env python3

#to install:
#sudo cp halt.py /usr/local/bin/
#sudo chmod +x /usr/local/bin/halt.py

import RPi.GPIO as GPIO
import subprocess
from bibliopixel import Strip
from bibliopixel.drivers.SPI.WS2801 import  WS2801
from bibliopixel.drivers.spi_interfaces import SPI_INTERFACES
from bibliopixel.colors.colors import COLORS
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(3, GPIO.FALLING)

driver = WS2801(198, dev='/dev/spidev0.1',spi_interface= SPI_INTERFACES.PERIPHERY,spi_speed=1)
layout = Strip(driver,  brightness=100)
layout.all_off()
layout.update()
layout.set(100, COLORS.red)
layout.update()
sleep(2)
layout.all_off()
layout.update()

subprocess.call(['shutdown', '-h', 'now'], shell=False)
