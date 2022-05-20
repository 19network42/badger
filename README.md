# Badger

## Summary

This repository contains the result of a project between the staff of [19](https://s19.be) and some of its students.
The project's goals is to build and develop a badge reader that would help the staff know the list of students who participate in an event.
This repository is divided in two parts: `embedded` and `webapp`.

### [embedded](/embedded)
This directory contains the code to run the physical reader, which as an `Arduino MKK WiFi 1010` connected to an `Adafruit PN532 NFC/RFID controller breakout board`.

### [webapp](/webapp)
This directory contains a Django web application which communicates with the physical reader through an HTTP API and can be configured through a web panel.

## Authors

- Aleksandr Buzdin (student)
- Antoine Coulon (staff)
- Jérémy Vander Motte (student)
- Louise Rondia (student)
- Nathan Colin (student)
- Romain Van Der Vennet (staff)

# Setup

### `webapp`:
- Create and activate a python3 virtual environement:
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```
- Install the dependencies:
```sh
$ pip install -r webapp/requirements.txt
```
- Create and populate a `.env` file from the template:
```sh
$ cp webapp/.env.template webapp/.env
```

## License

This project is distributed under the [MIT License](/LICENSE).
