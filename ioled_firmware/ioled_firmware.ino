#include <Adafruit_NeoPixel.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define STRIP_PIN 5
Adafruit_NeoPixel strip = Adafruit_NeoPixel(12, STRIP_PIN, NEO_GRB + NEO_KHZ800);

const char* ssid      = "SSID";
const char* password  = "PASSWORD";

WiFiUDP Udp;
unsigned int localUdpPort = 2712;
char incomingPacket[255];


void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");

  Udp.begin(localUdpPort);
  Serial.printf("Listening IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

  strip.begin();
  strip.show();
}


void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    // Receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;
    }
    Serial.printf("Packet: %s\n", incomingPacket);

    // {ACTION};{LED_S}-{LED_F}:{R},{G},{B};...
    // Actions: broadcast, light
    String packet = String(incomingPacket);
    char action = packet.charAt(0);
    //packet.remove(0);
    packet = packet.substring(1, packet.length());

    if (action == 'b') {
      // Send the cool reply to the IP and Port
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      Udp.write(WiFi.localIP().toString().c_str());
      Udp.endPacket();

    }
    if (action == 'l') {
      // Get LEDs info
      int i = 0, j = 0;
      for (j = 0; j < packet.length(); j++) {
        if (packet.charAt(j) == ';') {
          setLed(packet.substring(i, j));
          i = j + 1;
        }
      }
    }
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write("true");
    Udp.endPacket();
  }
}

void setLed(String led_config) {
  int range_s, range_f;
  int r = -1, g = -1, b = -1;

  int i = 0, j = 0;
  for (j = 0; j < led_config.length(); j++) {
    //Get range start number
    if (led_config.charAt(j) == '-') {
      range_s = led_config.substring(i, j).toInt();
      i = j + 1;
    }

    if (led_config.charAt(j) == ':') {
      range_f = led_config.substring(i, j).toInt();
      i = j + 1;
    }

    if (led_config.charAt(j) == ',') {
      if (r == -1) {
        r = led_config.substring(i, j).toInt();
        i = j + 1;
      } else {
        g = led_config.substring(i, j).toInt();
        i = j + 1;
      }
    }
  }
  b = led_config.substring(i, led_config.length()).toInt();
  printf("l_s: %d, l_f: %d, r: %d, g: %d, b: %d\n", range_s, range_f, r, g, b);

  for (i = range_s; i < range_f; i++) {
    strip.setPixelColor(i, strip.Color(r, g, b));
    strip.show();
  }
}
