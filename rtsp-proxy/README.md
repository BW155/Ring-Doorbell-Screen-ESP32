# rtsp-proxy

This folder contains the project files for the rtsp proxy.

# Setup

## Step 1: Install node packages

```
npm install
```

## Step 2: Generate access token for the ring api

This can be done using the cli of the ring-client-api:

```
npx -p ring-client-api ring-auth-cli
```

make sure the outcome file is saved as `ring_token.cache`

## Step 3: Start

Before starting. make sure the rtsp server is running. else the ffmpeg part will crash.

run using:

```
node index.js
```
