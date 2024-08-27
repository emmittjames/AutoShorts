# Short-form Video Generator

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)

## General Info
#### YouTube channel link: [youtube.com/@DashofReddit](https://www.youtube.com/@DashofReddit)
This project is a short-form video generator, designed to automate the creation and upload of short-form videos to YouTube. Content is sourced from Reddit using PRAW, screenshots are captured using Selenium, speech is generated from text using Amazon Polly, and everything is stitched together and overlayed on top of a background video. These videos are then automatically uploaded to YouTube via the YouTube Data API.
	
## Technologies
Project created with:
* Python
* ~~[TikTok TTS API](https://github.com/oscie57/tiktok-voice)~~
* [Amazon Polly](https://aws.amazon.com/polly/) - Text to speech
* [PRAW](https://praw.readthedocs.io/en/stable/) - Reddit API
* [Selenium](https://www.selenium.dev/) via [Selenium Grid container for Firefox](https://hub.docker.com/r/selenium/standalone-firefox) - Screenshots
* [YouTube Data API](https://developers.google.com/youtube/v3) - Uploading

Project hosted with: 
* Raspberry Pi 5 - Runs Docker container of Autoshorts once a day signaled by a cron job

## Getting Started
Start Selenium Grid container: `docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" --name selenium selenium/standalone-firefox:latest`