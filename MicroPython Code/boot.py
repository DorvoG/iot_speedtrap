# boot.py -- run on boot-up

import lidarlib
import event
import struct
import binascii
import time
import utime
from LoRaWAN import lora
from machine import UART, Pin
from servolib import Servo


print("boot")
# Turn on LED during boot setup
led = Pin("LED", Pin.OUT)
led.value(1)

# Configure Lidar
lidar = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))  # Define receiving interface of Lidar 
print(lidar)
utime.sleep_ms(100)

# Configure LoRaWAN
lora = lora()

DEV_EUI = "PLACEHOLDER1234"
APP_EUI = "0000000000001234"
APP_KEY = "PLACEHOLDER1234PLACEHOLDER1234"

lora.configure(DEV_EUI, APP_EUI, APP_KEY)

lora.startJoin()
print("Start Join.....")
while not lora.checkJoinStatus():
  print("Joining....")
  time.sleep(1)
print("Join success!")

# Initalize Servo and move to resting position (6 degrees)
from servolib import Servo
sg90_servo = Servo(pin=6)
sg90_servo.move(6)

# Initialize PIR-sensors
pir1 = Pin(16, Pin.IN)
pir2 = Pin(17, Pin.IN)

# Blink LED to indicate boot complete
led.toggle()
utime.sleep_ms(200)
led.toggle()
utime.sleep_ms(200)
led.toggle()
utime.sleep_ms(200)
led.toggle()
utime.sleep_ms(200)
led.toggle()
utime.sleep_ms(200),
