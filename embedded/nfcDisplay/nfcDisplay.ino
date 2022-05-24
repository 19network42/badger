//  Librairies : Adafruint_PN532, Adafruit_busIO, WiFiNINA

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include <WiFiNINA.h>

#include "arduino_secrets.h" 


////	Wifi setup
//	SECRET variables are defined in arduino_secret.h

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;

WiFiClient client;

////	Server setup

IPAddress server(10,40,3,104); 
int port = 8000;

int status = WL_IDLE_STATUS;

////	NFC setup

#define PN532_SCK  2
#define PN532_MOSI 3
#define PN532_SS   4
#define PN532_MISO 5
#define BUZZER A1

Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

void setup() {

	Serial.begin(9600);
	while (!Serial) {
		; // Wait for serial port to connect. Needed for native USB port only
	}
  pinMode(BUZZER, OUTPUT);
	String fv = WiFi.firmwareVersion();
	if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
		Serial.println("Please upgrade the firmware");
	}

	//	Identifying nfc reader

	nfc.begin();

	uint32_t versiondata = 0;
	int	tries = 0;

	Serial.println("Looking for PN53x board ...");
	while (!versiondata && tries++ < 5) {
		versiondata = nfc.getFirmwareVersion();
	}

	if (!versiondata) {
		Serial.println("Failed to find PN53x board.");
		while (1) {
			;
		}
	}

	//	Found reader, printing data

	Serial.print("Found chip PN5");
	Serial.println((versiondata>>24) & 0xFF, HEX); 
	Serial.print("Firmware ver. ");
	Serial.print((versiondata>>16) & 0xFF, DEC); 
	Serial.print('.');
	Serial.println((versiondata>>8) & 0xFF, DEC);

	// Set the max number of retry attempts to read from a card
	// This prevents us from waiting forever for a card, which is
	// the default behaviour of the PN532.
	nfc.setPassiveActivationRetries(0xFF);

	// configure board to read RFID tags
	nfc.SAMConfig();


	//	Connecting to wifi network

	Serial.print("Attempting to connect to SSID: ");
	Serial.println(ssid);

	while (status != WL_CONNECTED) {
		status = WiFi.begin(ssid, pass);
		delay(100);
	}

	Serial.println("Connected to WiFi");
  tone(BUZZER, 100);
  delay(100);
  tone(BUZZER, 1000);
  delay(600);
  noTone(BUZZER);
	printWiFiStatus();

	//	Connecting to webapp
	Serial.println("\nStarting connection to server...");
	if (client.connect(server, port)) {
	  Serial.println("connected to server");
	  // Make a HTTP request: 
	}
	else
		Serial.println("Failed to connect to the server");
}

void loop() {
	boolean success;
	uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
	uint8_t uidLength;        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)

	//	Waiting for a card to be scanned
	Serial.println("Waiting for an ISO14443A card");
	success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);

	int len = 0;
	char id[20];

	if (success) {
		Serial.println("Found a card!");
		for (uint8_t i=0; i < uidLength - 1; i++) 
		{
			len += sprintf(id + len, "%X:", uid[i]);
		}
		sprintf(id + len, "%X", uid[uidLength - 1]);
		Serial.print("UID Value: ");
		Serial.println(id);
		// if you get a connection, report back via serial:
    String postData = "{\"id\":\"" + String(id) + "\"}";
//		String jsonObject = "{\"id\":\"";
//		client.println("POST /scan HTTP/1.1");
//		client.println("Host: 10.40.3.104");
//		client.println("Content-Type: application/json");
//		client.println("Connection: keep-alive");
//		//BODY
//    client.println("{");
//    client.print("\"id\":\"");
//		client.print(id);
//		client.println("\"");
//		client.println("}");
    client.print(
      String("POST ") + "/scan/" + " HTTP/1.1\r\n" +
      "Content-Type: application/json\r\n" +
      "Content-Length: " + postData.length() + "\r\n" +
      "\r\n" +
      postData
      );
		//	wait 3 seconds for connection:
		delay(3000);

		//	Read response from server
		while (client.available()) {
			char c = client.read();
			Serial.write(c);
		}
	}
	else {
		// PN532 probably timed out waiting for a card
		Serial.println("Timed out waiting for a card");
	}

	// if the server's disconnected, stop the client:
	if (!client.connected()) {
		Serial.println();
		Serial.println("Disconnected from server.");
		client.stop();

		// do nothing forevermore:
		while (true)
			;
	}
}

void printWiFiStatus() {
	// print the SSID of the network you're attached to:
	Serial.print("SSID: ");
	Serial.println(WiFi.SSID());

	// print your board's IP address:
	IPAddress ip = WiFi.localIP();
	Serial.print("IP Address: ");
	Serial.println(ip);

	// print the received signal strength:
	long rssi = WiFi.RSSI();
	Serial.print("signal strength (RSSI):");
	Serial.print(rssi);
	Serial.println(" dBm");
}
