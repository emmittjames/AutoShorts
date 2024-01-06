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

    # Write output to file
    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    fileName = f"{script.title} #redditstories #reddit #redditposts"
    fileName = fileName.replace("/", " or ")
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )

    if final.duration > 60:
        partOne = final.subclip(0, 59)
        fileName = f"{script.title} part 1 #redditstories #reddit #redditposts"
        outputFile = f"{outputDir}/{fileName}.mp4"
        partOne.write_videofile(
            outputFile, 
            codec='mpeg4',
            threads=threads, 
            bitrate=bitrate
        )
    """
        if final.duration > 120:
            partTwo = final.subclip(60, 119)
            outputFile = f"{outputDir}/{fileName} part 2.mp4"
            partTwo.write_videofile(
                outputFile, 
                codec='mpeg4',
                threads=threads, 
                bitrate=bitrate
            )
            partThree = final.subclip(120, final.duration)
            outputFile = f"{outputDir}/{fileName} part 3.mp4"
            partThree.write_videofile(
                outputFile, 
                codec='mpeg4',
                threads=threads, 
                bitrate=bitrate
            )
        else:
            partTwo = final.subclip(59, final.duration)
            outputFile = f"{outputDir}/{fileName} part 2.mp4"
            partTwo.write_videofile(
                outputFile, 
                codec='mpeg4',
                threads=threads, 
                bitrate=bitrate
            )
    """

    print(f"Video completed in {time.time() - startTime}")

    """
    # Preview in VLC for approval before uploading
    if (config["General"].getboolean("PreviewBeforeUpload")):
        vlcPath = config["General"]["VLCPath"]
        p = subprocess.Popen([vlcPath, outputFile])
        print("Waiting for video review. Type anything to continue")
        wait = input()
    """

    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")

if __name__ == "__main__":
    createVideo()