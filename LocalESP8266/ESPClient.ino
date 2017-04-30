/* This is the ESP8266 #spaceapps software
* Team Flash
* Author: <stein.vinicius2@gmail.com>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 2 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/ 
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <SocketIoClient.h>
#include <String.h>
#include <DHT.h>

#define USE_SERIAL Serial
#define DHTPIN D2
#define DHTTYPE DHT11

char IPSERVER[] = "192.168.1.104";
int PORTSERVER = 8775;

DHT dht(DHTPIN, DHTTYPE);
ESP8266WiFiMulti WiFiMulti;
SocketIoClient webSocket;

boolean MANDA = 1;
String jsonsend;
char jsonchar[255];

// Trigger to recive event.
void evento(const char * payload, size_t length) {
  USE_SERIAL.printf("Mensagem: %s\n", payload);
  MANDA = 1;
}

// Create Json String and Get sensor data.
void CreateStr(){
    jsonsend = "{\"data\":\"{";
    String MACAD = WiFi.macAddress(); // capture MacAddress to use for device ID
    MACAD.replace(":","");            // Remove :
    int SIGNAL = WiFi.RSSI();         // capture radio RX power
    float humi = dht.readHumidity();  
    float temp = dht.readTemperature();
    // Create String
    jsonsend += "'ID':";
    jsonsend += "'"+MACAD+"',";
    jsonsend += "'data':[";
    jsonsend += "{'name':'temp','value':'"+(String)temp+"','unit':'Celsius'},";
    jsonsend += "{'name':'humid','value':'"+(String)humi+"','unit':'Percent'},";
    jsonsend += "{'name':'pluv','value':'0','unit':'mm'},"; // Dont have Sensor now
    jsonsend += "{'name':'Signal','value':'"+(String)SIGNAL+"','unit':'dBm'}";
    jsonsend += "]}\"}";
}


void setup() {
    USE_SERIAL.begin(115200);
    WiFi.mode(WIFI_STA);
    //USE_SERIAL.println("AGUARDANDO WPS");
    //USE_SERIAL.println(WiFi.beginWPSConfig() ? "Conectado VIA WPS" : "WPS FALHOU");

    USE_SERIAL.setDebugOutput(false);

    dht.begin();

    WiFiMulti.addAP("qualquer uma", "87654321");

    while(WiFiMulti.run() != WL_CONNECTED) {
        delay(100);
    }

    webSocket.on("getdata", evento); // Create trigger to event
    webSocket.begin(IPSERVER, PORTSERVER, "/socket.io/?transport=websocket"); // open tcp connection
}

void loop() {
    webSocket.loop(); // check new event and make keepalive
        
        if(MANDA){ // Send data.
          MANDA = 0;
          CreateStr();
          jsonsend.toCharArray(jsonchar, 255);
          webSocket.emit("my micro data",jsonchar);
          webSocket.loop();
        }
}

