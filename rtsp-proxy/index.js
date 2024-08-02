const dotenv = require("dotenv");
const path = require("path");
const { RingApi } = require("ring-client-api");
const { mkdir, rm } = require("fs").promises;
const { join } = require("path");
const RtspServer = require("rtsp-streaming-server").default;
const { spawn } = require("child_process");

// Initialize dotenv to load environment variables
dotenv.config();

const outputDirectory = join(__dirname, "output");

async function cleanOutputDirectory() {
  await rm(outputDirectory, {
    force: true,
    recursive: true,
  });
  await mkdir(outputDirectory);
}

async function startRtspServer() {
  /*const server = new RtspServer({
    serverPort: 8554,
    clientPort: 7554,
    rtpPortStart: 10000,
    rtpPortCount: 10000,
    debug: true,
  });

  await server.start();
  console.log("RTSP server started at rtsp://localhost:8554");

  return server;*/
}

async function startRingStream() {
  const config = {
    refreshToken: process.env.REFRESH_TOKEN,
    debug: true,
  };

  const ringApi = new RingApi(config);

  const locations = await ringApi.getLocations();
  const location = locations[0];
  const camera = location.cameras[0];

  console.log("Got camera called:", camera.data.description);

  /*camera.onMotionDetected.subscribe((data) => {
    console.log("You got motion data:");
    console.log(data);
  });*/

  if (!camera) {
    console.log("No cameras found");
    return;
  }

  await cleanOutputDirectory();

  console.log("Starting Video...");
  const call = await camera.streamVideo({
    video: ["-filter:v", "scale=320:240", "-c:v", "libx264", "-bf", "0"],
    output: ["-report", "-f", "rtsp", "rtsp://localhost:8554/live"],
  });

  console.log("Video started, streaming to RTSP server...");

  call.onCallEnded.subscribe(() => {
    console.log("Call has ended");
    process.exit();
  });

  /*setTimeout(function () {
    console.log("Stopping call...");
    call.stop();
  }, 60 * 1000); // Stop after 1 minute*/
}

async function main() {
  try {
    await startRtspServer();
    await startRingStream();
  } catch (err) {
    console.error("Error:", err);
  }
}

main();
