# ESP Proxy

The `esp-proxy` component acts as an intermediary server that converts the RTSP stream to a format suitable for the ESP32 to display. It captures frames from the RTSP stream, compresses them into JPEG format, and serves them to the ESP32 over a TCP connection.

## Setup and Configuration

### Prerequisites

Ensure you have Python 3.9 or higher installed on your system. The `esp-proxy` uses `poetry` for dependency management.

### Installing Poetry

You can install `poetry` by following the instructions on the [official website](https://python-poetry.org/docs/#installation).

### Installing Dependencies

Navigate to the `esp-proxy` directory and install the dependencies:

```sh
poetry install
```

## Run the esp proxy

```sh
poetry run python udp_server.py
```
