// Programa : Projeto de sensor hall para catracas
// Autor : Raphael Pontes Santana
#include <ArduinoJson.h> 
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
WiFiClient WiFiClient;
PubSubClient client(WiFiClient);

StaticJsonDocument<200> doc;
int count = 0;
int pinosinal= 2;
// define a porta para o acionamento do led
int pinoled = 6;      
// Porta ligada ao pino SINAL do sensor

// Nome do wifi e senha
#define ssid "aula-ic3"
#define password "iotic@2019"

#define SERVER "mqtt.demo.konkerlabs.net"
#define SERVERPORT 1883

#define username "bsrpd5lh126i"
#define passwordmqtt "FDbsQ8Bh921F"

#define userID "raphael"

// topicos

// ultima parte de topico eh o nome do usuario
#define TOPIC1 "data/bsrpd5lh126i/pub/1"


unsigned long int actualTime = 0;
unsigned long int lastTime = 0;

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
}

void loop()
{
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
      doc["sensor"] = "hall";
      doc["time"] = 1351824120;
      doc["data"] = count;
      char buffer[512];
      size_t n = serializeJson(doc, buffer);
      client.publish(TOPIC1, buffer, n);
    }
    lastTime = actualTime;
  }
}
