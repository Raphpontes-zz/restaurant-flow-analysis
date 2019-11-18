// Programa : Projeto de sensor hall para catracas
// Autor : Raphael Pontes Santana
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

WiFiClient WiFiClient;
PubSubClient client(WiFiClient);

StaticJsonDocument<256> doc;
int count = 0;
int pinosinal= 2;
// define a porta para o acionamento do led
int pinoled = 6;
// Porta ligada ao pino SINAL do sensor

// Nome do wifi e senha
#define ssid "aula-ic3"
#define password "iotic@2019"
//#define ssid "MyASUSR"
//#define password "12345678"
 

#define SERVER "mqtt.demo.konkerlabs.net"
#define SERVERPORT 1883

//ESP 1
#define username "bsrpd5lh126i"
#define passwordmqtt "FDbsQ8Bh921F"
//ESP 2
//#define username "5u0pkst320l4"
//#define passwordmqtt "C3qQKvumhgXD"


#define userID "raphael"

// topicos

// ultima parte de topico eh o nome do usuario
#define TOPIC1 "data/bsrpd5lh126i/pub/1"
#define TOPIC2 "data/5u0pkst320l4/pub/1"

const long utcOffsetInSeconds = -10600;
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "south-america.pool.ntp.org", utcOffsetInSeconds);

unsigned long int actualTime = 0;
unsigned long int lastTime = 0;
unsigned long int lastCount = 0;

// Armazena informações sobre a leitura do sensor
int leitura;
// Armazena o estado do led (ligado/desligado)
int estadoled = 0;

void setup()
{
  Serial.begin(9600);
  //Define o pino do led como saida
  //pinMode(pinoled, OUTPUT);

  //Define o pino do sensor hall como entrada
  pinMode(pinosinal, INPUT);
  delay(10);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("Connected to Wifi!");
  client.setServer(SERVER, SERVERPORT);
  lastTime = millis();
  timeClient.begin();
}

void loop()
{
  StaticJsonDocument<256> doc;
  leitura = digitalRead(pinosinal);

  if (leitura != 1)
  {
    while(digitalRead(pinosinal) != 1)
    {
      delay(100);
    }
    // Inverte o estado
    estadoled = !estadoled;
    Serial.println("Lido sinal magnetico");
    count++;
    Serial.println(count);
  }
  actualTime = millis();
  if(actualTime - lastTime > 30000){
    if(client.connect(userID, username, passwordmqtt)){
      JsonObject root = doc.to<JsonObject>();
      Serial.println("Enviando pacote para o servidor");
      while(!timeClient.update()) {
        timeClient.forceUpdate();
      }
      String dateTime = timeClient.getFormattedTime();
      Serial.println(dateTime);
      root["sensor"] = "hall";
      root["time"] = dateTime;
      root["people"] = count;
      root["difference"] = count - lastCount;
      char buffer[512];
      size_t n = serializeJson(root, buffer);
      client.publish(TOPIC1, buffer, n);
      lastCount = count;
    }
    lastTime = actualTime;
  }
}
