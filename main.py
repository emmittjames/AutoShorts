from moviepy.editor import *
import reddit, screenshot, time, subprocess, random, configparser, sys, math, pyperclip
from os import listdir
from os.path import isfile, join

def createVideo():

    config = configparser.ConfigParser()
    config.read('config.ini')
    outputDir = config["General"]["OutputDirectory"]

    startTime = time.time()

    postOptionCount = int(config["Reddit"]["NumberOfPostsToSelectFrom"])
    script, postId, read_comments = reddit.getContent(outputDir, postOptionCount)

    fileName = script.getFileName()

    # Create screenshots
    screenshot.getPostScreenshots(fileName, script, postId, read_comments)


    # Setup background clip
    bgDir = config["General"]["BackgroundDirectory"]
    bgPrefix = config["General"]["BackgroundFilePrefix"]
    bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f)) and f.lower().endswith('.mp4')]
    bgCount = len(bgFiles)
    print(f"Found {bgCount} background files")
    bgIndex = random.randint(0, bgCount-1)

    backgroundVideo = VideoFileClip(
        filename=join(bgDir, bgFiles[bgIndex]),
        audio=False)
    
    background_video_start_time = random.randint(0, math.floor(backgroundVideo.duration - script.getDuration()) - 30)
    
    backgroundVideo = backgroundVideo.subclip(background_video_start_time, background_video_start_time + script.getDuration())

    w, h = backgroundVideo.size

    # Set the desired aspect ratio (9:16)
    desired_aspect_ratio = 9 / 16

    # Calculate the width based on the background's height
    bg_height = backgroundVideo.size[1]
    desired_width = int(bg_height * desired_aspect_ratio)

    def __createClip(screenShotFile, audioClip, marginSize):
        imageClip = ImageClip(
            screenShotFile,
            duration=audioClip.duration
            ).set_position(("center", "center"))
        imageClip = imageClip.resize(width=desired_width - marginSize)
        videoClip = imageClip.set_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    marginSize = int(config["Video"]["MarginSize"])
    print("titleSCFile: " + script.titleSCFile)
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    for comment in script.frames:
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize))

    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))


    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo.set_position(("center", "center")), contentOverlay],
        size=(desired_width, bg_height)).set_audio(contentOverlay.audio)
    final.duration = script.getDuration()
    final.set_fps(backgroundVideo.fps)

    final = final.fx(vfx.speedx, 1.1) # Speed up video

    tags = ["#redditstories", "#reddit", "#redditposts"]
    fileName = script.title
    fileName = fileName.replace("/", " or ")
    if(len(fileName) > 100):
        fileName = fileName[:100]
        last_space_index = fileName.rfind(' ')
        fileName = fileName[:last_space_index]
    else:
        for tag in tags:
            if(len(fileName) + len(tag) < 100):
                fileName += tag + " "
    fileName = fileName[:100]

    # Write output to file
    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    outputFile = f"{outputDir}/{fileName}.mp4"
    if(final.duration > 60):
        final_clip = final.subclip(0, 60) 
    final_clip.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )

    print(f"Video completed in {time.time() - startTime}")
    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")

    description = "Engaging posts originating from all around Reddit! Make sure to check out my channel and subscribe for more awesome Reddit clips."
    keywords = "reddit, redditpost, redditstories, redditstory, askreddit, aita, tifu"
    category = "24"
    privacy_status = "private"

    upload_video(outputFile, fileName, description, keywords, category, privacy_status)

def upload_video(file, title, description, keywords, category, privacy_status):
    command = [
        "python3", "upload_video.py",
        "--file", file,
        "--title", title,
        "--description", description,
        "--keywords", keywords,
        "--category", category,
        "--privacyStatus", privacy_status
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == "__main__":
    createVideo()