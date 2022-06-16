# Badger: `embedded`

## Summary

ToDo

## Hardware

### Material

- [Arduino MKR WiFi 1010](https://docs.arduino.cc/hardware/mkr-wifi-1010)
- [AdaFruit PN532 NFC/RFID controller breakout board](https://www.adafruit.com/product/364)
- [AdaFruit Assembled Standard LCD 16x2](https://www.adafruit.com/product/1447)
- Piezo Buzzer
- Push Button
- Potentiometer

### Wiring

<img width="1524" alt="Badger" src="https://user-images.githubusercontent.com/16177499/172823822-bb1925d0-d1c0-4e64-81d3-928273e0b057.png">


## Software

### Downloaded libraries
-   Adafruit_busIO
-   WiFiNINA
-   Adafruit_PN532
-   LiquidCrystal
-   ArduinoJson

### Setup

- Create a secrets file:
```sh
$ touch badger/arduino_secrets.h
```
- Populate it with the following template:
```c
#define SECRET_SSID ""
#define SECRET_PASS ""
#define IPADDRESS_SERVER ""
#define PORT
#define SCAN_URL ""
#define INIT_URL ""
#define TOKEN_POST ""
#define 
```

## Description of the system

### Setup method

- At the launch of the arduino, it sets up the NFC READER. If the set up failed it will stay blocked in an infinite loop.  
&emsp; So You need to relaunch the arduino.
A message is printed on the LCD screen.  
✅ : NFC Reader OK!  
❎ : NFC Reader KO!  
  
- Once the NFC READER is ok, it will try to connect to the Wifi with `SECRET_SSID` and `SECRET_PASS` which are respectively the name of the wifi and the password of the wifi.
&emsp; ➡️ If the connection failed, it will try to reconnect indefinitely.  
A message is printed on the LCD screen.  
✅ : Wifi connect. OK!  
❎ : Wifi connect. KO!  
 
- Once the Wifi connection is setup it tries to connect to the server. It uses the `IPADDRESS_SERVER` and `PORT` to connect.
&emsp; ➡️ If the connection failed, it will try to reconnect indefinitely.
A message is printed on the LCD screen.  
✅ : Server connect. OK!  
❎ : Server connect. KO!  

- Once all is connected, it tries to get all the modes. It sends a `HTTP request` to the server on the `INIT_URL` page. It gets all the modes and put it in variables.
A message is printed on the LCD screen.  
✅ : Init. mode OK!  
❎ : No Event... Then a countdown is displayed for the retry.  

- After the init, we will attach an interrupt by `attachInterrupt()` method. In this way, we are able to change the mode anywhere we are in the code.


### Loop method

- If the client isn't connected, we will try to reconnect it indefinitely. 
- The program is waiting for a card to read.
- Reading card ✅  
➡️ Create the HTTP request with the `uid` of the card and the current `mode` to the server on the `SCAN_PAGE`.  
- Reading card ❎   
➡️ Do nothing and go to the top of the loop function.
- Response from webapp ✅ (`201 CREATED`) : We get data from the server. Data will be in `JSON` form so we need to deserialize them.  
&emsp;using ArduinoJSON library.  
- Response from webapp ❎ : we disconnect the client and we try to reconnect.   
&emsp;This prevent us to read data from the response we don't want to.

- Deserialization ✅ : We get the `color` of the led, the `boolean` for the buzzer and the `message` to display.
- Deserialization ❎ : We do nothing.
- Display : the `color` is set on the LED, the `boolean` sound is played on the buzzer and the `message` is displayed on the LCD Screen.
Check if the Wifi is OK. If it's not the case try to reconnect indefinitely. It does the same after with the client. During those reconnections, the `interrupt` is disabled to prevent us from changing the mode involuntarily.
