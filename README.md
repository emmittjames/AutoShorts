# Short-form Video Generator

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)

## General Info
#### YouTube channel link: [youtube.com/@DashofReddit](https://www.youtube.com/@DashofReddit)
This project is a short-form video generator designed to automate the creation and upload of videos to YouTube. Content is sourced from Reddit using PRAW, screenshots are captured via Selenium, and speech is generated from text using Amazon Polly. The elements are then stitched together and overlaid on a background video. Finally, the videos are automatically uploaded to YouTube using the YouTube Data API.
	
## Technologies
Project created with:
* Python
* ~~[TikTok TTS API](https://github.com/oscie57/tiktok-voice)~~
* [Amazon Polly](https://aws.amazon.com/polly/) - Text to speech
* [PRAW](https://praw.readthedocs.io/en/stable/) - Reddit API
* [Selenium](https://www.selenium.dev/) via [Selenium Grid container for Firefox](https://hub.docker.com/r/selenium/standalone-firefox) - Screenshots
* [YouTube Data API](https://developers.google.com/youtube/v3) - Uploading

Project hosted with: 
* Raspberry Pi 5 - Runs Docker container of AutoShorts 0-2 times a day signaled by a cron job (still experimenting with optimal upload schedule)

## Prerequisites

* Python 3.11+
* Docker (for Selenium Firefox container)
* Reddit API app credentials
* AWS credentials with Polly access
* Google Cloud OAuth client + YouTube Data API enabled

## Getting Started

### 1. Clone and install

```
git clone https://github.com/emmittjames/AutoShorts.git
cd AutoShorts

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create required working directories

```
mkdir -p OutputVideos Scripts Voiceovers Screenshots
```

### 3. Add background assets

Put your media files in:

* BackgroundVideos/  (mp4 files)
* BackgroundMusic/  (mp3 files)

### 4. Configure  config.ini 

#### Create/update  config.ini  with your own values:

```
[General]
PreviewBeforeUpload = yes
VLCPath = /path/to/vlc
OutputDirectory = OutputVideos
BackgroundVideoDirectory = BackgroundVideos
BackgroundMusicDirectory = BackgroundMusic
BackgroundFilePrefix = ShortTemplate_

[Video]
MarginSize = 100
Bitrate = 8000k
Threads = 12

[Reddit]
NumberOfPostsToSelectFrom = 5
CLIENT_ID = your_reddit_client_id
CLIENT_SECRET = your_reddit_client_secret
USER_AGENT = platform:autoshorts:v1.0 by your_username
SUBREDDIT = askreddit

[Email]
SenderEmail =
SenderPassword =
RecipientEmail =

[AWS]
aws_access_key_id = your_aws_access_key_id
aws_secret_access_key = your_aws_secret_access_key
```

### 5. Add YouTube OAuth client file

Place `client_secrets.json` in the repo root.

This must be an installed app OAuth client config from Google Cloud.

### 6. Start Selenium Firefox container

```
docker run -d \
  -p 4444:4444 \
  -p 7900:7900 \
  --shm-size="2g" \
  --name selenium \
  selenium/standalone-firefox:latest
```

### 7. Run the project

#### Generate video only:

`python3 main.py`

#### Generate + upload to YouTube:

`python3 main.py --upload`

#### If running inside a container:

`python3 main.py --docker-compose`
( the docker-compose flag makes Selenium use  http://firefox:4444/wd/hub  instead of localhost)