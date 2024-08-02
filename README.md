# Ring Doorbell Screen ESP32

This project is a POC of showing a live feed of a ring doorbell to a ESP32 with TFT display.

![image](./pics/image.png)

## Parts

To make this all work a couple of parts are needed:

### Part 1: Ring API interface

Folder: [rtsp-proxy](./rtsp-proxy)

While ring doesn't provide a public API interface. There are multiple projects that try to provide this through reverse engineering.\
The best one I found was a nodejs library [ring-client-api](https://github.com/dgreif/ring/tree/main/packages/ring-client-api). This library provides a way to get a livestream to be processed using `ffmpeg`. While this isn't the most ideal. it allows us to stream to different formats and/or locations. like an RTSP server.

### Part 2: RTSP Server

Folder: [rtsp-server](./rtsp-server)

I wanted to use an RTSP server in the middle because it makes it easier to process through existing technologies. For the RTSP server I used mediamtx.

### Part 3: ESP-proxy server

Folder: [esp-proxy](./esp-proxy)

To make the esp display as fast as possible I wanted to make a proxy server in between that converts the rtsp stream to a more esp friendly format.

### Part 4: ESP display

Folder: [esp-display](./esp-display)

The display gathers the individual frames from the esp-proxy and renders them on the screen. Due to the limited heap space a compressed jpeg is used.
