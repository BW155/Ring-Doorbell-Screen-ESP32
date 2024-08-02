# ESP Display

This part of the project is responsible for rendering the live feed from the Ring doorbell on the ESP32's TFT display. The display gathers individual frames from the ESP-proxy server and renders them. Due to the limited heap space, a compressed JPEG format is used.

## Setup and Configuration

The `esp-display` component uses PlatformIO for development and deployment.

### PlatformIO

PlatformIO is an open-source ecosystem for IoT development. It supports multiple development platforms, including the ESP32.

1. **Installation**:

   - You can install PlatformIO as an extension in Visual Studio Code or download it from the [PlatformIO website](https://platformio.org/install).

2. **Project Initialization**:
   - Initialize the project by navigating to the `esp-display` folder and opening it with PlatformIO.

### Secrets Configuration

The WiFi details and server IP/port need to be configured for the ESP32 to connect to the network and the proxy server. These details are stored in `src/secrets.h`.

1. **Creating `secrets.h`**:

   - Create a file named `secrets.h` in the `src` directory of the `esp-display` project.

2. **Configuring WiFi and Server Details**:
   - Add your WiFi credentials and server IP/port details to `secrets.h` as follows:

```cpp
// src/secrets.h

#ifndef SECRETS_H
#define SECRETS_H

// WiFi credentials
#define SSID_NAME "SSID"
#define SSID_PASS "SSID_PASS"

// Server details
#define SERVER_ADDRESS "1.2.3.4"
#define SERVER_PORT 5005

#endif // SECRETS_H
```
