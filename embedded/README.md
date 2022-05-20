# Badger: `embedded`

## Summary

ToDo

## Hardware

### Material

- [Arduino MKR WiFi 1010](https://docs.arduino.cc/hardware/mkr-wifi-1010)
- [AdaFruit PN532 NFC/RFID controller breakout board](https://www.adafruit.com/product/364)
- [AdaFruit Assembled Standard LCD 16x2](https://www.adafruit.com/product/1447)
- Piezo Buzzer

### Wiring

TODO

## Software

### Setup

- Create a secrets file:
```sh
$ touch badger/arduino_secrets.h
```
- Populate it with the following template:
```c
#define WIFI_SSID ""
#define WIFI_PASS ""
#define API_URL ""
#define API_TOKEN ""
```