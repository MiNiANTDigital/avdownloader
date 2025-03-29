# Audio / Video Downloader

- A simple web application for downloading YouTube videos using `yt-dlp`, built with Flask.

## Default deployment: Local Python environment

- Note: ffmpeg installation is required if you wish to combine best quality audio and video and convert into single file such as .mp4

## Optional deployment: Dockerfile is available for deploying on Google Cloud Run.

- Note: Audio / Video platforms might require authentication and block the app, you'll need to extract a cookies.txt file to bypass the bot detection, this is not included in this app. You can reference

## Features

- Download Audio/Video in the best available format.
- User-friendly web interface.
- Default local deployment or optional Google Cloud Run deployment with Dockerfile available.

## Credit

- https://github.com/yt-dlp/yt-dlp

## License

- MIT License
