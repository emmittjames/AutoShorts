import argparse
from moviepy.editor import *
import reddit, screenshot, time, subprocess, random, configparser, math
from os import listdir
from os.path import isfile, join
import sys

def createVideo(upload = False, docker_compose = False):
    config = configparser.ConfigParser()
    config.read('config.ini')
    outputDir = config["General"]["OutputDirectory"]

    startTime = time.time()

    postOptionCount = int(config["Reddit"]["NumberOfPostsToSelectFrom"])
    script, postId, read_comments = reddit.getContent(outputDir, postOptionCount)

    print("file name:", fileName)

    # Create screenshots
    screenshot.getPostScreenshots(fileName, script, postId, read_comments, docker_compose)


    # Setup background clip
    bgDir = config["General"]["BackgroundVideoDirectory"]
    bgPrefix = config["General"]["BackgroundFilePrefix"]
    bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f)) and f.lower().endswith('.mp4')]
    bgCount = len(bgFiles)
    print(f"Found {bgCount} background files")
    bgIndex = random.randint(0, bgCount-1)

    backgroundVideo = VideoFileClip(
        filename=join(bgDir, bgFiles[bgIndex]),
        audio=False)
    
    background_video_start_time = random.randint(0, math.floor(backgroundVideo.duration - script.getDuration()) - 1)
    
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
    
    def __addBackgroundMusic(existingClip):
        music_dir= config["General"]["BackgroundMusicDirectory"]
        mp3_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
        if not mp3_files:
            return existingClip
        random_file = random.choice(mp3_files)
        backgroundMusic = AudioFileClip(os.path.join(music_dir, random_file))

        start_time = random.uniform(0, 15)
        backgroundMusic = backgroundMusic.subclip(start_time, start_time+existingClip.duration+2)
        backgroundMusic = backgroundMusic.volumex(0.05)

        combinedAudio = CompositeAudioClip([existingClip.audio, backgroundMusic])
        newClip = existingClip.set_audio(combinedAudio)
        return newClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    marginSize = int(config["Video"]["MarginSize"])
    print("titleSCFile: " + script.titleSCFile)
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    for comment in script.frames:
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize))

    new_clips = []
    for i, clip in enumerate(clips):
        shaved_clip = clip.subclip(0, clip.duration - 0.1)
        new_clips.append(shaved_clip)
    clips = new_clips

    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))
    contentOverlay = __addBackgroundMusic(contentOverlay)

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo.set_position(("center", "center")), contentOverlay],
        size=(desired_width, bg_height)).set_audio(contentOverlay.audio)
    final.duration = script.getDuration()
    final.set_fps(backgroundVideo.fps)

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
                fileName += " " + tag
    fileName = fileName[:100]

    # Write output to file
    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    outputFile = f"{outputDir}/{fileName}.mp4"
    if(final.duration >= 60):
        final = final.subclip(0, 59) 
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate,
    )

    print(f"Video completed in {time.time() - startTime}")
    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")

    description = (
        "Engaging posts originating from all around Reddit! Make sure to check out my channel and subscribe for more awesome Reddit clips.\n\n"
        "Music:\n"
        "LEMMiNO - Cipher\n"
        "https://www.youtube.com/watch?v=b0q5PR1xpA0\n"
        "CC BY-SA 4.0"
    )
    keywords = "reddit, redditpost, redditstories, redditstory, askreddit, aita, tifu"
    category = "24"
    privacy_status = "public"

    if upload:
        upload_video(outputFile, fileName, description, keywords, category, privacy_status)

def upload_video(file, title, description, keywords, category, privacy_status):
    subprocess.run(['python3', 'refresh_oauth_token.py'])

    upload_command = [
        "python3", "upload_video.py",
        "--file", file,
        "--title", title,
        "--description", description,
        "--keywords", keywords,
        "--category", category,
        "--privacyStatus", privacy_status
    ]

    result = subprocess.run(upload_command, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    subprocess.run(['python3', 'clear.py'], capture_output=True, text=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', action='store_true')
    parser.add_argument('--docker-compose', action='store_true')
    args = parser.parse_args()

    for i in range(3):
        try:
            createVideo(upload=args.upload, docker_compose=args.docker_compose)
            break
        except Exception as e:
            print(e, "\nSomething went wrong. Retrying in 5 seconds...")
            if i == 2:
                sys.exit(1)
            time.sleep(5)
