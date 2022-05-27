# Badger Protocol
Communication protocol between the embedded reader and the web application.

## Definitions
- `reader`: microcontroller with an internet connection that sends requests to the webapp.
- `webapp`: web application serving an API enpoint to the internet through HTTPS to receive requests from the reader.

## Support
Communication will be done through HTTP**S** `POST` requests from the reader to the webapp.

## Launch

### Launch description
The microcontroller verify the connection with the reader, connects to the wifi and the webapp's server.
When connected, it sends a first request to get the different mode depending on the current event
(Exemples; mode 1 : Presence, mode 2 : Drinks, ...).

## Request

### Authentication
The reader will prove its identity by sending a secret token in a custom HTTP Header called `X-Secret`.

### Content
The content of the request will be formated in JSON.
The request will send the following JSON values:
- `uid`: string

4 bytes UID of a badge, in uppercase hexadecimal, each bytes separated by a semicolon.
- `timestamp`: int

Epoch time of the request, in seconds.

- `mode`: int

Current Arduino's mode, matching the Webapp modes requested at launch.

### Example

```
POST /api/endpoint HTTP/1.1
Host: example.org
X-Secret: Uc=tL.0Qxha0cWe
Content-Type: application/json

{
    "uid": "ED:40:9A:F8",
    "mode": "1",
    "timestamp": 1653032868233
}
```

## Response

### Return code
If the server could process the request, it will return the `200 OK` status code.

### Content
The content of the response will be formated in JSON.
The response will send the following JSON values:
- `message`: string

String message to output on the LCD screen.
- `sound`: int

Code of the sound to play with the piezo buzzer.

### Example
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "message": "hello marvin",
    "sound": 1
}
```

