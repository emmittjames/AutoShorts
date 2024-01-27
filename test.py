import subprocess

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


file = "example.mp4"
title = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjkkkkk"
description = "Engaging posts originating from all around Reddit! Make sure to check out my channel and subscribe for more awesome Reddit clips."
keywords = "reddit, redditpost, redditstories, redditstory, askreddit, aita, tifu"
category = "24"
privacy_status = "private"

upload_video(file, title, description, keywords, category, privacy_status)
