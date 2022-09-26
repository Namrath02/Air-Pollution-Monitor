#include "Adafruit_SHT4x.h"
#include <Wire.h>
#include "Adafruit_SGP40.h"
#include "WiFi.h"
#include "ThingSpeak.h"
#include  <ArduinoJson.h>
#include "HTTPClient.h"

#define WIFI_NETWORK "esw-m19@iiith"
#define WIFI_PASSWORD "e5W-eMai@3!20hOct"
//-----------------------------------------------------------------------
String cse_ip = "192.168.137.148";        // YOUR IP from ipconfig/ifconfig
String cse_port = "8080";
String server = "http://" + cse_ip + ":" + cse_port + "/~/in-cse/in-name/";
String ae = "Indoor-Air-Pollution";
String cnt = "Data";
//-----------------------------------------------------------------------

unsigned long myChannelNumber =  1847325;
const char * myWriteAPIKey = "0UOR6TD4FQA2GU03";

void ConnectToWifi(){
  Serial.println("Connecting To wifi!!");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_NETWORK,WIFI_PASSWORD);
  int start = millis();
  while(WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(100);
  }
  Serial.println("Connected to Wifi");
  Serial.println(WiFi.localIP());
}

void CreateContentInstance(String& val)
{
  HTTPClient http;
  http.begin(server + ae + "/" + cnt + "/");
  http.addHeader("X-M2M-Origin", "admin:admin");
  http.addHeader("Content-Type", "application/json;ty=4");
  int code = http.POST("{\"m2m:cin\": {\"cnf\":\"application/json\",\"con\": " + String(val) + "}}");
  Serial.println(code);
  if (code == -1) {
    Serial.println("UNABLE TO CONNECT TO THE SERVER");
  }
  http.end();
}

WiFiClient  client;

//------------------------------------------------CO2 Sensing-----------------------------------------------------
#define PIN 4
unsigned long duration, th, tl;
int ppm;

void CO2_Monitor(String& val){
  th = pulseIn(PIN, HIGH, 2008000) / 1000;
  tl = 1004 - th;
  ppm = 2000 * (th - 2) / (th + tl - 4);

  if(ppm > 1000){
    Serial.println(ppm);
    ThingSpeak.setField(1,ppm);
  }
  else{
//    Serial.print(" Co2 Concentration: ");
//    Serial.println(ppm);
    ThingSpeak.setField(1,ppm);
    val+=(String)ppm+",";
    //    Serial.println(" ppm");
  }
}

//--------------------------------------------------SHT4x---------------------------------------------------------------------------------------------------------------------------------------
Adafruit_SHT4x sht4 = Adafruit_SHT4x();

void SHT_setup(){
  if (! sht4.begin()) {
    Serial.println("Couldn't find SHT4x");
    while (! sht4.begin()) delay(1);
  }
  sht4.setPrecision(SHT4X_HIGH_PRECISION);
  sht4.setHeater(SHT4X_NO_HEATER);

}

void SHT_Reading(String& val){
  sensors_event_t humidity, temp;
  
  uint32_t timestamp = millis();
  sht4.getEvent(&humidity, &temp);// populate temp and humidity objects with fresh data
  timestamp = millis() - timestamp;

    val=val+(String)temp.temperature+","+(String)humidity.relative_humidity+",";

  delay(1000);
}

//-------------------------------------------------SGP-------------------------------------------------------------------------------------------------------------------------------------------
Adafruit_SGP40 sgp;

void SGP_setup(){
  Serial.println("SGP40 test");

  if (! sgp.begin()){
    Serial.println("Sensor not found :(");
    while (1);
  }
//  Serial.print("Found SGP40 serial #");
//  Serial.print(sgp.serialnumber[0], HEX);
//  Serial.print(sgp.serialnumber[1], HEX);
//  Serial.println(sgp.serialnumber[2], HEX);
}

void SGP_Reading(String& val){
  uint16_t raw;
  int voc_index;
  raw = sgp.measureRaw();
  Serial.println("VOC: ");
  voc_index = sgp.measureVocIndex();
  Serial.println(voc_index);
//  Serial.print("VOC: ");
  ThingSpeak.setField(2, voc_index);
  val+=(String)voc_index+",";
//  Serial.println(raw);
  delay(1000);
}

//------------------------------------------------------Particulate Matter----------------------------------------------------------------------------------------------------------------------

unsigned long previous_loop, previous_10, previous_25, prev_time;

int pm2;
int pm10;
byte command_frame[9] = {0xAA, 0x02, 0x00, 0x00, 0x00, 0x00, 0x01, 0x67, 0xBB};
byte received_data[9];
int sum = 0;

void send_command(byte command)
{
  command_frame[1] = command;
  int sum = command_frame[0] + command_frame[1] + command_frame[2] + command_frame[3] + command_frame[4] + command_frame[5] + command_frame[8];
  int rem = sum % 256;
  command_frame[6] = (sum - rem) / 256;
  command_frame[7] = rem;
  delay(5000);
  Serial.write(command_frame, 9);

}

bool checksum()
{
  sum = int(received_data[0]) + int(received_data[1]) + int(received_data[2]) + int(received_data[3]) + int(received_data[4]) + int(received_data[5]) + int(received_data[8]);
  if (sum == ((int(received_data[6]) * 256) + int(received_data[7])))
  {
    return true;
  }
  else
    return false;
}
void calculate_pm(String &val)
{
  int pm2 = int(received_data[4]) * 256 + int(received_data[5]);
  delay(5000);
  int pm10 = int(received_data[2]) * 256 + int(received_data[3]);
  ThingSpeak.setField(3, pm2);
  ThingSpeak.setField(4, pm10);
  val+=(String)pm2+","+(String)pm10+"]";
//  Serial.println("PM2.5 "); Serial.println(pm2);
//  Serial.println("PM10 "); Serial.println(pm10);
}

void PM_setup(){
  send_command(0x01);
}

void PM_Reading(String& val){
  delay(5000);
  if (millis() - prev_time > 5000)
  {
    send_command(0x02);
    prev_time = millis();
  }
  if (Serial.available())
  {
    Serial.readBytes(received_data, 9);
    if (checksum())
    {
      calculate_pm(val);
    }
  }
}

//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

void setup() {
  Serial.begin(9600);  
  delay(5000);
  ConnectToWifi();
  ThingSpeak.begin(client);
  SHT_setup();
  SGP_setup();
  PM_setup();
}

int counter = 0;
int start=millis();
String val="";
void loop() {

    String ans;
    val="";
    SHT_Reading(val);
    Serial.println("Humidity and Temperature: ");
    Serial.print(val);
    ans+=val;
    val="";
    Serial.println("CO2: ");
    CO2_Monitor(val);
     Serial.print(val);
     ans+=val;
    val="";
    Serial.println("VOC: ");
    SGP_Reading(val);
     Serial.print(val); ans+=val;
    val="";
    Serial.println("PM2.5 and PM10: ");
    PM_Reading(val);
     Serial.print(val); ans+=val;
//    CreateContentInstance(ans);
    ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
    start=millis();
  
 
  Serial.println();
//  Serial.println(val);
}
