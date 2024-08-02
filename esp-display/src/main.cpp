#include <TFT_eSPI.h>
#include <TJpg_Decoder.h>
#include <WiFi.h>
#include <WiFiClient.h>

#include "secrets.h"  // Insert secrets like SSID and Server address here

const char* ssid = SSID_NAME;                // your SSID (network name) here
const char* password = SSID_PASS;            // your WiFi password here
const char* serverAddress = SERVER_ADDRESS;  // Replace with your server IP
const int tcpPort = SERVER_PORT;

TFT_eSPI tft = TFT_eSPI();
WiFiClient client;

#define BUFFER_SIZE 4096       // Adjusted buffer size for chunking
#define MAX_IMAGE_SIZE 100000  // Maximum size for the JPEG image

unsigned long lastMillis = 0;
unsigned long frameCount = 0;
float fps = 0.0;

uint8_t* jpegBuffer;  // Buffer for JPEG data
int totalBytesRead = 0;

// Function to display status on TFT
void displayStatus(float fps) {
  String local_ip = WiFi.localIP().toString();
  int rssi = WiFi.RSSI();

  int rect_width = 120;
  int rect_height = 40;
  tft.fillRect(320 - rect_width, 0, rect_width, rect_height, TFT_RED);
  tft.setTextColor(TFT_WHITE, TFT_RED);
  int x = 320 - rect_width + 5;
  int y = 5;
  tft.drawString(local_ip, x, y, 1);
  y += 10;
  tft.drawString(String(rssi) + " dBm", x, y, 1);
  y += 10;
  tft.drawString(String(fps) + " FPS", x, y, 1);
}

// Function to display WiFi setup message on TFT
void displayWifiSetup() {
  tft.fillScreen(TFT_WHITE);
  tft.setTextColor(TFT_BLACK, TFT_WHITE);
  tft.drawString("Connecting WiFi...", 320 / 3, 240 / 2);
}

// JPEG output callback for TJpg_Decoder
bool tft_output(int16_t x, int16_t y, uint16_t w, uint16_t h,
                uint16_t* bitmap) {
  tft.pushImage(x, y, w, h, bitmap);
  return true;
}

// Function to check if the JPEG end marker is present
bool isJpegComplete(uint8_t* buffer, int length) {
  if (length < 2) return false;
  return buffer[length - 2] == 0xFF && buffer[length - 1] == 0xD9;
}

void connectToWiFi() {
  WiFi.begin(ssid, password);  // WiFi.begin turns on WiFi on the ESP32
  displayWifiSetup();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void setup() {
  Serial.begin(115200);
  tft.init();
  tft.setRotation(1);  // This is the display in landscape
  tft.fillScreen(TFT_BLACK);

  connectToWiFi();

  TJpgDec.setJpgScale(1);  // Scale 1 means full size
  TJpgDec.setCallback(tft_output);
  TJpgDec.setSwapBytes(true);  // Ensure correct byte order for RGB565

  // Allocate buffer for the JPEG data once
  jpegBuffer = (uint8_t*)malloc(MAX_IMAGE_SIZE);
  if (jpegBuffer == nullptr) {
    Serial.println("Failed to allocate memory for JPEG buffer");
    while (true);  // Stop execution if allocation fails
  }
}

void requestImage() {
  if (!client.connect(serverAddress, tcpPort)) {
    Serial.println("Connection to server failed");
    delay(1000);  // Wait before retrying
    return;
  }
  client.print("GET_IMAGE");
  Serial.println("Requested image from server");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected, reconnecting...");
    connectToWiFi();
  }

  requestImage();

  totalBytesRead = 0;
  bool imageReceived = false;

  while (client.connected()) {
    while (client.available()) {
      int bytesRead = client.read(jpegBuffer + totalBytesRead, BUFFER_SIZE);
      totalBytesRead += bytesRead;

      Serial.printf("Read %d bytes, Total: %d bytes\n", bytesRead,
                    totalBytesRead);

      if (isJpegComplete(jpegBuffer, totalBytesRead)) {
        Serial.println("JPEG end marker found, stopping read.");
        imageReceived = true;
        break;
      }
    }

    if (imageReceived) {
      break;
    }
  }

  if (imageReceived) {
    Serial.printf("Finished reading data from server. Total: %d bytes\n",
                  totalBytesRead);
    Serial.printf("Drawing JPEG image, total size: %d bytes\n", totalBytesRead);
    TJpgDec.drawJpg(0, 0, jpegBuffer, totalBytesRead);

    // Calculate FPS
    frameCount++;
    unsigned long currentMillis = millis();
    if (currentMillis - lastMillis >= 1000) {
      fps = frameCount * 1000.0 / (currentMillis - lastMillis);
      frameCount = 0;
      lastMillis = currentMillis;
    }

    // Draw status box after image
    displayStatus(fps);
  } else {
    Serial.println("No data received from server or connection timed out.");
  }

  client.stop();

  delay(100);  // Wait before requesting the next image
}