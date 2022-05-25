//  Librairies : Adafruint_PN532, Adafruit_busIO, WiFiNINA

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include <WiFiNINA.h>
#include <ArduinoJson.h>
#include <utility/wifi_drv.h>
#include <LiquidCrystal.h>

#include "arduino_secrets.h" 


WiFiClient client;
int status = WL_IDLE_STATUS;

#define PN532_SCK  2
#define PN532_MOSI 3
#define PN532_SS   4
#define PN532_MISO 5
#define BUZZER A1
#define RED 25
#define GREEN 26
#define BLUE 27
#define LCD_RS 7
#define LCD_EN 8
#define LCD_D4 9
#define LCD_D5 10
#define LCD_D6 11
#define LCD_D7 12

LiquidCrystal lcd(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7);

Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

void setup() {

	Serial.begin(9600);
	while (!Serial) {
		; // Wait for serial port to connect. Needed for native USB port only
	}

  //  Setup pin for hardware use.
  setupPin();
  
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
  
   uid = readCardUID();
   if (strcmp("ERROR", uid.c_str()) == 0)
   {
      Serial.println("ERROR reading card");
      lcd.print("Error card");
   }
   else
   {
      createAndSendHTTPRequest(String(uid));
      if (isResponseFromWebAppOK())
      {
          getDataFromWebApp();
      }
   }
	  // if the server's disconnected, stop the client:
	  clientIsConnected();
  delay(3000);
}

/*
 * Check if the client is connected.
 * @error : If the client isn't connected anymore : infinite loop
 * to restart the arduino and server.
 */
void  clientIsConnected(void)
{
  if (!client.connected()) {
		  Serial.println();
		  Serial.println("Disconnected from server.");
      lcd.clear();
      lcd.print("Server connect.");
      lcd.setCursor(0,1);
      lcd.print("lost...");
		  client.stop();

		  // do nothing forevermore:
		  while (true)
			;
	  }
}


/*
 * Setup pin to use method and hardware.
 */
void  setupPin(void)
{
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2); 
  //Initialize pins
  pinMode(BUZZER, OUTPUT);
	WiFiDrv::pinMode(GREEN, OUTPUT);
  WiFiDrv::pinMode(RED, OUTPUT);
  WiFiDrv::pinMode(BLUE, OUTPUT);
}

/*
 * Retrieve the JSON object and return the message to print. Turn on the led and make a sound
 * with the buzzer.
 * @return const char * : the message to print on the screen.
 */
const char * getDataFromWebApp(void)
{
  //Change the capacity if more or less data are added or deleted
  int capacity = 128;
  uint8_t red, green, blue;
  const char *msg;
  JsonArray led;
  DynamicJsonDocument doc(capacity);
  
  DeserializationError error = deserializeJson(doc, client);
  
  if (error)
  {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return (NULL);
  }
  led = doc["led"];
  red = led[0];
  green = led[1];
  blue = led[2];
  turnOnLed(red,green,blue);
  bool buzzer = doc["buzzer"];
  if (buzzer)
    playSuccessBuzzer();
  else
    playFailureBuzzer();
  delay(200);
  turnOnLed(0,0,255);
  msg = doc["msg"];
  Serial.println(msg);
  lcd.print(msg);
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
    Serial.println(status);
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
    lcd.print("Connect. server");
    lcd.setCursor(0,1);
    lcd.print("OK!");
    
  }
  else
  {
    Serial.println("Failed to connect to the server");
    lcd.print("Connect. server");
    lcd.setCursor(0,1);
    lcd.print("KO!");
    while(1);
  }
  delay(1500);
  lcd.clear();
  turnOnLed(0,0,255);
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
  lcd.print("Wifi connect.");
  lcd.setCursor(0,1);
  lcd.print("OK!");
  delay(1500);
  lcd.clear();
//  playSuccessBuzzer();
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
    lcd.print("NFC Reader");
    lcd.setCursor(0,1);
    lcd.print("KO!");
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
  lcd.print("NFC reader");
  lcd.setCursor(0,1);
  lcd.print("OK!");
  delay(1500);
  lcd.clear();
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
 * Turn on the builtin led.
 * @param uint8_t, uint8_t, uint8_t : red color, green color, blue color
 */
void  turnOnLed(uint8_t red, uint8_t green, uint8_t blue)
{
  WiFiDrv::analogWrite(RED, red);
  WiFiDrv::analogWrite(GREEN, green);
  WiFiDrv::analogWrite(BLUE, blue);
}

/*
 * Play a success sound on the piezzo buzzer
 */
void  playSuccessBuzzer(void)
{
  tone(BUZZER, 987);
  delay(100);
  tone(BUZZER, 1318);
  delay(300);
  noTone(BUZZER);
}

/*
 * Play a fail sound on the piezzo buzzer.
 */
void  playFailureBuzzer(void)
{
  tone(BUZZER, 100);
  delay(200);
  noTone(BUZZER);
  delay(100);
  tone(BUZZER, 100);
  delay(200);
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
  lcd.clear();
  lcd.print("Scan a badge...");
  lcd.setCursor(0,1);
  lcd.print("mode = default");
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
    lcd.clear();
    return (String(id));
  }
  turnOnLed(255,0,0);
  delay(200);
  turnOnLed(0,0,255);
  return ("ERROR");
}
