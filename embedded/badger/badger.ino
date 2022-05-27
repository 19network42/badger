//  Librairies : Adafruint_PN532, Adafruit_busIO, WiFiNINA

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include <WiFiNINA.h>
#include <ArduinoJson.h>

#include "arduino_secrets.h" 


WiFiClient client;
int status = WL_IDLE_STATUS;

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
	
  //  Identifying nfc reader
  setupNfcReader();
  
	//	Connecting to wifi network
  setupAndConnectWifi();

	//	Connecting to webapp
	connectToWebApp();
}

void loop() {
	int len = 0;
	char id[20];
  String uid;
  const char * login;
  
   uid = readCardUID();
   if (strcmp("ERROR", uid.c_str()) == 0)
   {
      Serial.println("ERROR reading card");
   }
   else
   {
      createAndSendHTTPRequest(String(uid));
      if (isResponseFromWebAppOK())
      {
          login = getDataFromWebApp();
          if (login)
          {
              Serial.println(login);
          }
      }
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
  delay(3000);
}

const char * getDataFromWebApp(void)
{
  //Change the capacity if more or less data are added or deleted
  int capacity = 16 + 60;
  
  DynamicJsonDocument doc(capacity);
  DeserializationError error = deserializeJson(doc, client);
  
  if (error)
  {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return (NULL);
  }
  return (doc["login"]);
}

/*
 * Check if the response from the webApp is good to continue
 * process of the program.
 * @return bool : true if the response is correct, False otherwise.
 */
bool  isResponseFromWebAppOK()
{
  char status[32] = {0};
    client.readBytesUntil('\r', status, sizeof(status));
    // It should be "HTTP/1.1 201 CREATED"
    if (strcmp(status + 9, "201 Created") != 0) {
      Serial.print(F("Unexpected response: "));
      Serial.println(status);
//      client.stop();
      return (false);
    }
    char endOfHeaders[] = "\r\n\r\n";
    if (!client.find(endOfHeaders)) {
      Serial.println(F("Invalid response"));
//      client.stop();
      return (false);
    }
    return (true);
}

/*
 * Send HTTP POST request to the webApp using a JSON object to send data.
 * @param String uid ; the uid of the card scanned
 */
void  createAndSendHTTPRequest(String uid)
{
  String postData = "{\"id\":\"" + uid + "\"}";
  client.print(
    String("POST ") + TARGET_URL + " HTTP/1.1\r\n" +
    "Content-Type: application/json\r\n" +
    "Content-Length: " + postData.length() + "\r\n" +
    "X-Secret: " + TOKEN_POST + "\r\n" +
    "\r\n" +
    postData
    );
}

/*
 * Try to connect to the server.
 * @Error : infinite loop to force turn off the arduino.
 */
void  connectToWebApp(void)
{
  Serial.println("\nStarting connection to server...");
  if (client.connect(IPADDRESS_SERVER, PORT))
  {
    Serial.println("Connected to server");
  }
  else
  {
    Serial.println("Failed to connect to the server");
    while(1);
  }
  delay(1000);
}

/*
 * Setup and connect To the wifi which is define in arduinoSecret.h
 * It will die and try until the connection is established.
 */
void  setupAndConnectWifi(void)
{
  char ssid[] = SECRET_SSID;
  char pass[] = SECRET_PASS;

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }
  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);
    delay(100);
  }
  Serial.println("Connected to WiFi");
  playSuccessBuzzer();
  printWiFiStatus();
}

/*
 * Setup the NFC Reader for the setup() function.
 * @error : infinite loop to force unplugged the arduino.
 */
void setupNfcReader(void)
{
  nfc.begin();
  uint32_t versiondata = 0;
  int tries = 0;

  Serial.println("Looking for PN53x board ...");
  while (!versiondata && tries++ < 5) {
    versiondata = nfc.getFirmwareVersion();
  }

  if (!versiondata) {
    Serial.println("Failed to find PN53x board.");
    while(1);
  }

  //Print data of chip PN5
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
}


/*
 * Print the informations of the current wifi connection ofthe Arduino.
 */
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

/*
 * Play a success sound on the piezzo buzzer
 */
void  playSuccessBuzzer(void)
{
  tone(BUZZER, 100);
  delay(100);
  tone(BUZZER, 1000);
  delay(600);
  noTone(BUZZER);
}

/*
 * Read card and return into a String the UID of it.
 * @return : String corresponding to the UID of the card
 * @error : Return "ERROR" if something went wrong with the NFC Reader (PN532)
 */
String  readCardUID(void)
{
  boolean success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  int len = 0;
  char id[20];
  
  //  Waiting for a card to be scanned
  delay(1000);
  Serial.println("Waiting for an ISO14443A card");
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
  if (success) {
    Serial.println("Found a card!");
    for (uint8_t i=0; i < uidLength - 1; i++) 
    {
      len += sprintf(id + len, "%X:", uid[i]);
    }
    sprintf(id + len, "%X", uid[uidLength - 1]);
    Serial.print("UID Value: ");
    Serial.println(id);
    return (String(id));
  }
  return ("ERROR");
}
