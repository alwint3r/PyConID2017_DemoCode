PyCon ID 2017 Live Demo Code
============================

This code was shown during my talk at PyCon Indonesia 2017 on December 9th 2017 in Surabaya, Indonesia.

## What I used for demo

* ESPectro32 development board, an ESP32-based development board by DycodeX
* esptool.py, for dealing with ESP32 flash
* Adafruit ampy, for dealing with MicroPython vfs
* Latest MicroPython for ESP32 firmware
* BMP180 barometric pressure sensor

## How to run the code?

Download the latest MicroPython firmware, you can get the link from [here](https://micropython.org/download/#esp32)

```bash
wget -c http://micropython.org/resources/firmware/esp32-20171210-v1.9.2-445-g84035f0f.bin
```

Before flashing the firmware to the board, erase the flash first.

```
esptool.py --port /dev/ttyUSB0 --baud 921600 erase_flash
```

Then, flash the firmware to the board.

```
esptool.py --port /dev/ttyUSB0 --baud 921600 write_flash 0x1000 esp32-20171210-v1.9.2-445-g84035f0f.bin
```

Reset the board by pressing reset button.

Now, install Adafruit's ampy by using pip

```bash
sudo pip install adafruit-ampy --upgrade
```

Get the bmp180.py file from the repository and upload the file to the board's filesystem.

```
ampy --port /dev/ttyUSB0 put bmp180.py
```

Then, open the serial monitor to install `umqtt.simple` module from the package index.

```
screen /dev/ttyUSB0 115200
```

Connect to the internet using WiFi to download the `umqtt.simple` module for sending data through MQTT protocol.

```python
# connect to the wireless network
import network as nwk
net = nwk.WLAN(nwk.STA_IF)
net.active(True)
net.connect("WIFI_SSID", "WIFI_PASSWORD")
```

```python
# download the module
import upip as pip
pip.install('micropython-umqtt.simple')
```

If the module installation is failed, you have to reset the board and repeat the wifi connection setup and `umqtt.simple` installation procedure.

Detach and kill the screen session or you can simply unplug then plug the USB cable back to your computer.

Then, upload the `main.py` from this repository to the board using the same step when we uploaded the `bmp180.py` file.

Note that you should edit some variable value inside the file before uploading the file.

```
ampy -p /dev/ttyUSB0 put main.py
```

And you're done! You can check the serial monitor just to be sure.


**Things to note here**
* I use `/dev/ttyUSB0` as the serial port, you may change it if you're not using `/dev/ttyUSB0`.
* If you have ESP-IDF installed but you don't have esptool.py on the shell path, then you can run this command `export PATH=$PATH:$IDF_PATH/components/esptool_py/esptool` before running `esptool.py` command.
* When flashing the firmware, you can use maximum baud rate (2Mb) but it is safe to use 921600 as some board may be doesn't support 2Mb baud rate.

