# RTSP Server

This component sets up an RTSP server to handle the live feed from the Ring doorbell and make it accessible for further processing.

## Step 1: Download the Server

First, download the MediaMTX server files suitable for your machine from the following link:

- **Download Link**: [MediaMTX Releases](https://github.com/bluenviron/mediamtx/releases)

Choose the appropriate version for your operating system (e.g., Windows, macOS, Linux) and download the package.

## Step 2: Configure the Server

The configuration file `mediamtx.yml` is provided in this repository. Ensure you have this file in the same directory where you downloaded the server.

## Step 3: Run the Server

Open a terminal or command prompt and navigate to the directory where you downloaded the MediaMTX server and the configuration file.

Run the server using the following command:

```sh
./mediamtx -config mediamtx.yml
```

If you're on Windows, the command might be:

```sh
mediamtx.exe -config mediamtx.yml
```

Ensure that the server is running and listening on the configured port.

## Verifying the Setup

To verify that the server is running correctly, you can use an RTSP client such as VLC media player. Open VLC, go to `Media` > `Open Network Stream`, and enter the following URL:

```
rtsp://localhost:8554/live
```

If everything is set up correctly, you should be able to see the live feed from the Ring doorbell.

## Troubleshooting

- Ensure that the RTSP server address and port match the configuration in other parts of the project.
- Check for any firewall or network issues that might be blocking the RTSP stream.

For more detailed information and advanced configuration options, refer to the [MediaMTX documentation](https://github.com/bluenviron/mediamtx).
