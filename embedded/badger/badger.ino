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
#define BUTTON 0
#define NBR_MODE 10
int				maxMode;
String			modes[NBR_MODE] = {};
volatile int	currentMode = 0;

LiquidCrystal lcd(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7);

Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

void	setup() {

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

	//Initialize mode for the current event.
	initModes();

	//Attach interrupt to use the button for changing mode.
	attachInterrupt(digitalPinToInterrupt(BUTTON), changeMode, FALLING);
}

void	loop() {
	int		len = 0;
	char	id[20];
	String	uid;

	clientIsConnected(false);

	uid = readCardUID(modes, currentMode);
	//If Error reading card do nothing
	if (strcmp("ERROR", uid.c_str()) == 0)  {}
	else
	{
		createAndSendHttpRequestUser(uid, modes[currentMode]);
	if (isResponseFromWebAppOK())
	{
		getDataFromWebAppUser();
	}
	else
	{
		//Need to stop the client to retrieve a good request and response.
		//If not ; we'll get informations we don't want.
		client.stop();
	}
}
	//If there isn't wifi connection try to reconnect.
	isConnectedToWifi();

	// if the server's disconnected, try to reconnect
	clientIsConnected(true);
}

/*
 * Send a basic HTTP request with no body to get the initial modes.
 */
void	createAndSendHttpRequestInit(void)
{
	client.print(
	String("POST ") + INIT_URL + " HTTP/1.1\r\n" +
	"Content-Type: application/json\r\n" +
	"X-Secret: " + TOKEN_POST + "\r\n" +
	"\r\n"
	);
}

/*
 * Initialise the global modes and the number of mode
 *  with the response got by server. Retry until a event is found.
 */
void	initModes(void)
{
	//Used for time after retrying init mode.
	int i = 20;
	createAndSendHttpRequestInit();
	if (isResponseFromWebAppOK())
	{
		getInitDataFromWebApp();
		lcd.clear();
		lcd.print("Init. mode");
		lcd.setCursor(0,1);
		lcd.print("ok");
	}
	else
	{
		lcd.clear();
		lcd.print("No Event...");
		delay(2000);
		while (i-- > 0)
		{
			lcd.clear();
			lcd.print("Retry init. in ");
			lcd.setCursor(0,1);
			lcd.print((String)i + " sec");
			delay(1000); 
		}
		//If an error occured we need to stop the connection with the client
		//to get a proper response. If not ; we'll get information from response we don't want.
		client.stop();
		connectToWebApp();
		//Retry init mode until it's good.
		initModes();
	}
}

/*
 * Get the reponse from the server to initialise mode.
 * The response is deserialize from JSON and put in global variables.
 */
void	getInitDataFromWebApp(void)
{
	int					capacity = 256;
	JsonArray			modesFromApp;
	const char			*tmp;
	DynamicJsonDocument	doc(capacity);

	DeserializationError error = deserializeJson(doc, client);

	if (error){}
	else
	{
		modesFromApp = doc["mode"];
		maxMode = doc["mode_amount"];
		for (int i = 0; i < maxMode; i++)
		{
			tmp = modesFromApp[i];
			modes[i] = tmp;
		}
	}
}

/*
 * Change the current mode by launching interrupt.
 */
void	changeMode()
{
	static unsigned long	last_interrupt_time = 0;
	unsigned long			interrupt_time = millis();

	// If interrupts come faster than 310ms, assume it's a bounce and ignore
	if (interrupt_time - last_interrupt_time > 310)
	{
		if (currentMode == maxMode - 1)
		{
			currentMode = 0;
		}
		else
		{
			currentMode++;
		}
		lcd.clear();
		lcd.print("Scan a badge...");
		lcd.setCursor(0,1);
		lcd.print("mode = " + modes[currentMode]);
	}
	last_interrupt_time = interrupt_time;
}

/*
 * Check if there is a wifi connection anymore.
 * If it's not the case try to reconnect to the wifi every 5 seconds.
 */
void	isConnectedToWifi(void)
{
	char	ssid[] = SECRET_SSID;
	char	pass[] = SECRET_PASS;

	//If everything's good do nothing.
	if (WiFi.status() == WL_CONNECTED) return;
	detachInterrupt(BUTTON);
	lcd.clear();
	lcd.print("Wifi connect.");
	lcd.setCursor(0,1);
	lcd.print("lost...");
	delay(1000);
	lcd.clear();
	lcd.print("Reconnect. to");
	lcd.setCursor(0,1);
	lcd.print("wifi");
	while (WiFi.status() != WL_CONNECTED) {
		status = WiFi.begin(ssid, pass);
		delay(5000);
	}
	lcd.clear();
	lcd.print("Wifi connect.");
	lcd.setCursor(0,1);
	lcd.print("OK!");
	delay(1500);
	lcd.clear();
	attachInterrupt(digitalPinToInterrupt(BUTTON), changeMode, FALLING);
}

/*
 * Check if the client is connected and try to reconnect every 5 seconds 
 *  if it's not the case. Interruptions are disabled at the beginning and 
 *  enabled at the end of the function (Button does nothing).
 *  
 * @param bool reconnection : true if it's a reconnection, false otherwise.
 * 
 */
void	clientIsConnected(bool reconnection)
{
	//Avoid the use of the button while reconnecting.
	detachInterrupt(BUTTON);
	if (reconnection && !client.connected())
	{
		lcd.clear();
		lcd.print("Server connect.");
		lcd.setCursor(0,1);
		lcd.print("lost...");
		delay(1000);
		client.stop();
	}
	while (!client.connected())
	{
		lcd.clear();
		lcd.print("Retry connect.");
		lcd.setCursor(0,1);
		lcd.print("to server...");
		connectToWebApp();
		if (!client.connected())
		{
			lcd.print("Retry connect.");
			lcd.setCursor(0,1);
			lcd.print("to server...");
			delay(5000);
		}
	}
	//enable the use of the button
	attachInterrupt(digitalPinToInterrupt(BUTTON), changeMode, FALLING);
}

/*
 * Setup pin to use method and hardware.
 */
void	setupPin(void)
{
	// set up the LCD's number of columns and rows:
	lcd.begin(16, 2); 
	//Initialize pins
	pinMode(BUZZER, OUTPUT);
	pinMode(BUTTON, INPUT_PULLUP);

	//Builtin led pin
	WiFiDrv::pinMode(GREEN, OUTPUT);
	WiFiDrv::pinMode(RED, OUTPUT);
	WiFiDrv::pinMode(BLUE, OUTPUT);
}

/*
 * Retrieve the JSON object and return the message to print. Turn on the led and make a sound
 * with the buzzer.
 */
void	getDataFromWebAppUser(void)
{
	//Change the capacity if more or less data are added or deleted
	int			capacity = 256;
	uint8_t		red, green, blue;
	const char	*msg;
	JsonArray			led;
	DynamicJsonDocument doc(capacity);

	DeserializationError error = deserializeJson(doc, client);

	if (error){}
	else
	{
		led = doc["led"];
		red = led[0];
		green = led[1];
		blue = led[2];
		turnOnLed(red,green,blue);
		bool buzzer = doc["buzzer"];
		if (buzzer)
		{
			playSuccessBuzzer();
		}
		else
		{
			playFailureBuzzer();
		}
		delay(200);
		turnOnLed(red,green,blue);
		delay(300);
		turnOnLed(0,0,255);
		msg = doc["msg"];
		lcd.clear();
		scrollingMessage(msg);
		delay(500);
	}
}


/*
 * Utils method to display a message with scrolling view.
 */
void	scrollingMessage(const char * msg)
{
	uint8_t messageLength;
	uint8_t lcdLength = 15;
	uint8_t totalScroll;

	lcd.print(msg);
	delay(300);
	messageLength = strlen(msg);
	totalScroll = messageLength - lcdLength;
	detachInterrupt(BUTTON);
	for (int i = totalScroll; i >= 0; i--)
	{
		lcd.scrollDisplayLeft();
		delay(250);
	}
	attachInterrupt(digitalPinToInterrupt(BUTTON), changeMode, FALLING);
}

/*
 * Check if the response from the webApp is good to continue
 * process of the program.
 * @return bool : true if the response is correct, False otherwise.
 */
bool	isResponseFromWebAppOK()
{
	char status[64] = {0};
	client.readBytesUntil('\r', status, sizeof(status));
	// It should be "HTTP/1.1 201 CREATED"
	if (strcmp(status + 9, "201 Created") != 0)
	{
		return (false);
	}
	char endOfHeaders[] = "\r\n\r\n";
	if (!client.find(endOfHeaders))
	{
		return (false);
	}
	return (true);
}

/*
 * Send HTTP POST request to the webApp using a JSON object to send data.
 * @param String uid : the uid of the card scanned.
 * @param String mode : the actual mode for drinks.
 */
void	createAndSendHttpRequestUser(String uid, String mode)
{
	String postData = "{\"id\":\"" + uid + "\",\"mode\":\"" + mode + "\"}";
	client.print(
		String("POST ") + SCAN_URL + " HTTP/1.1\r\n" +
		"Content-Type: application/json\r\n" +
		"Content-Length: " + postData.length() + "\r\n" +
		"X-Secret: " + TOKEN_POST + "\r\n" +
		"\r\n" +
		postData
	);
}

/*
 * Try to connect to the server.
 */
void	connectToWebApp()
{
	if (client.connect(IPADDRESS_SERVER, PORT))
	{
		lcd.clear();
		lcd.print("Connect. server");
		lcd.setCursor(0,1);
		lcd.print("OK!");
		turnOnLed(0,0,255);
	}
	else
	{
		lcd.clear();
		lcd.print("Connect. server");
		lcd.setCursor(0,1);
		lcd.print("KO!");
	}
	delay(1500);
	lcd.clear();
}

/*
 * Setup and connect To the wifi which is define in arduinoSecret.h
 * It will try every 5 seconds until the connection is established.
 */
void	setupAndConnectWifi(void)
{
	char ssid[] = SECRET_SSID;
	char pass[] = SECRET_PASS;
	String fv = WiFi.firmwareVersion();

	if (fv < WIFI_FIRMWARE_LATEST_VERSION)
	{
		lcd.clear();
		lcd.print("Please upgrade");
		lcd.setCursor(0,1);
		lcd.print("the firmware");
	}
	while (status != WL_CONNECTED)
	{
		status = WiFi.begin(ssid, pass);
		delay(100);
	}
	lcd.print("Wifi connect.");
	lcd.setCursor(0,1);
	lcd.print("OK!");
	delay(1500);
	lcd.clear();
}

/*
 * Setup the NFC Reader. If it's not connected after 10 tries.
 *  throw an infinite loop to force to restart the arduino.
 */
void	setupNfcReader(void)
{
	nfc.begin();
	uint32_t versiondata = 0;
	int tries = 0;

	while (!versiondata && tries++ < 10)
	{
		versiondata = nfc.getFirmwareVersion();
	}
	while (!versiondata)
	{
		lcd.print("NFC Reader");
		lcd.setCursor(0,1);
		lcd.print("KO!");
		while(1);
	}

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
 * Turn on the builtin led with RGB code.
 * @param uint8_t red : red color.
 * @param uint8_t green : green color.
 * @param uint8_t blue : blue color.
 */
void	turnOnLed(uint8_t red, uint8_t green, uint8_t blue)
{
	WiFiDrv::analogWrite(RED, red);
	WiFiDrv::analogWrite(GREEN, green);
	WiFiDrv::analogWrite(BLUE, blue);
}

/*
 * Play a success sound on the piezzo buzzer
 */
void	playSuccessBuzzer(void)
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
void	playFailureBuzzer(void)
{
	tone(BUZZER, 100);
	delay(200);
	tone(BUZZER, 100);
	delay(200);
	noTone(BUZZER);
}
 

/*
 * Read card and return into a String the UID of it.
 * @param : String [] : All the mode available for the event.
 * @param : int : The current mode.
 * @return : String : the UID of the card or ERROR if something 
 *  went wrong (error reading card or timeout).
 */
String	readCardUID(String modes[], int currentMode)
{
	boolean success;
	uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
	uint8_t uidLength;        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
	int len = 0;
	char id[20];

	//Waiting for a card to be scanned
	lcd.clear();
	lcd.print("Scan a badge...");
	lcd.setCursor(0,1);
	lcd.print("mode = " + modes[currentMode]);
	delay(1000);
	success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
	if (success)
	{
		for (uint8_t i=0; i < uidLength - 1; i++)
		{
			len += sprintf(id + len, "%X:", uid[i]);
		}
		sprintf(id + len, "%X", uid[uidLength - 1]);
		return (String(id));
	}
	turnOnLed(0,0,0);
	delay(200);
	turnOnLed(0,0,255);
	return ("ERROR");
}
