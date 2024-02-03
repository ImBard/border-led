#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#define GREEN_PIN D1
#define RED_PIN D2
#define BLUE_PIN D3

const char *ssid = "CASA 153";
const char *password = "talison1";

WiFiServer server(3000);

void setup() {
  Serial.begin(115200);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String message = client.readStringUntil('\n');
    message.trim();

    int separatorIndex = message.indexOf(';');
    String left_color_str = message.substring(0, separatorIndex);
    String right_color_str = message.substring(separatorIndex + 1);

    int r1 = left_color_str.substring(0, left_color_str.indexOf(',')).toInt();
    left_color_str = left_color_str.substring(left_color_str.indexOf(',') + 1);
    int g1 = left_color_str.substring(0, left_color_str.indexOf(',')).toInt();
    int b1 = left_color_str.substring(left_color_str.indexOf(',') + 1).toInt();

    int r2 = right_color_str.substring(0, right_color_str.indexOf(',')).toInt();
    right_color_str = right_color_str.substring(right_color_str.indexOf(',') + 1);
    int g2 = right_color_str.substring(0, right_color_str.indexOf(',')).toInt();
    int b2 = right_color_str.substring(right_color_str.indexOf(',') + 1).toInt();

    // Agora você tem as cores RGB para a esquerda (r1, g1, b1) e direita (r2, g2, b2)
    // Você pode usar essas cores para controlar seus LEDs
    // Por exemplo, aqui estamos usando a cor da esquerda para definir a cor do LED
    analogWrite(RED_PIN, r1);
    analogWrite(GREEN_PIN, g1);
    analogWrite(BLUE_PIN, b1);
  }
}
