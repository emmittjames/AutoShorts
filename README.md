# Short-form Video Generator

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)

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
* Raspberry Pi 5 - Runs Docker container of AutoShorts 2 times a day signaled by a cron job

## Getting Started
Start Selenium Grid container: `docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" --name selenium selenium/standalone-firefox:latest`