from machine import I2C, Pin, ADC
from umqtt.simple import MQTTClient

import ujson as json
import utime as time
import machine
import network

# get the library from  https://github.com/micropython-IMU/micropython-bmp180
from bmp180 import BMP180

# Usually, almost every ESP32-based devboard uses 21 & 22 as SDA & SCL pin
SDA_PIN = 21
SCL_PIN = 22

# I use this pin to read analog data from a phototransistor
ADC_PIN = 36

# Fill these with your WiFi access point SSID and password
WIFI_SSID = ""
WIFI_PASS = ""

# Fill this variable with the hostname or IP of your MQTT broker
BROKER_HOST = ""

# Fill this variable with a topic that you use to publish data
PUBLISH_TOPIC = ""

def main():
    net = network.WLAN(network.STA_IF)
    net.active(True)
    net.connect(WIFI_SSID, WIFI_PASS)

    while not net.isconnected():
        pass

    # Connecting to MQTT broker
    print("Initializing MQTT client")
    mqtt_client = MQTTClient("micropy_client", BROKER_HOST, 1883)
    mqtt_client.connect()

    # Start reading data from sensors
    print("Initializing I2C for BMP180")
    i2c_bus = I2C(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN))
    bmp180 = BMP180(i2c_bus)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

    print("Initializing phototransistor ADC")
    photo_transistor = ADC(Pin(ADC_PIN))

    while True:
        time.sleep(2)

        data = {
            'temperature': bmp180.temperature,
            'pressure': bmp180.pressure,
            'light': photo_transistor.read(),
        }

        serialized = json.dumps(data)
        print("Will publish {}".format(serialized))

        # publish data to broker
        mqtt_client.publish(bytearray(PUBLISH_TOPIC), bytearray(serialized))

main()
