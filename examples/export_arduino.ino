#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoHttpClient.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED }; // Replace with your own MAC address
IPAddress ip(192, 168, 1, 140); // Define the desired static IP address
IPAddress gateway(192, 168, 1, 1); // Define your gateway IP address
IPAddress subnet(255, 255, 255, 0); // Define your subnet mask

char serverAddress[] = "192.168.1.7";  // Pushgateway server address
int serverPort = 9091; // Pushgateway port

EthernetClient ethClient;
HttpClient client = HttpClient(ethClient, serverAddress, serverPort);

void setup() {
  Serial.begin(9600);

  // Start Ethernet connection with static IP settings
  Ethernet.begin(mac, ip, gateway, subnet);

  // Allow time for Ethernet to initialize
  delay(1000);
}

void loop() {
  // Prepare metrics data
  String metricsData;
  for (int i = 0; i < 4; i++) {
    int value = analogRead(A0 + i);
    metricsData += "arduino_analog_" + String(i + 1) + " " + String(value) + "\n";
    delay(100); // Adjust delay as needed to prevent flooding the network
  }

  // Send all metrics in one request
  sendAllMetrics(metricsData);

  delay(250);
}

void sendAllMetrics(String data) {
  client.beginRequest();
  client.post("/metrics/job/arduino/instance/1");
  client.sendHeader("Content-Type", "text/plain; version=0.0.4");
  client.sendHeader("Content-Length", data.length());
  client.beginBody();
  client.print(data);
  client.endRequest();

  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);
}
