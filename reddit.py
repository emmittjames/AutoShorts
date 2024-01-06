import os
import re
import praw
import markdown_to_text
import time
from videoscript import VideoScript
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
CLIENT_ID = config["Reddit"]["CLIENT_ID"]
CLIENT_SECRET = config["Reddit"]["CLIENT_SECRET"]
USER_AGENT = config["Reddit"]["USER_AGENT"]
# SUBREDDIT = config["Reddit"]["SUBREDDIT"]

def getContent(outputDir, postOptionCount) -> VideoScript:
    reddit = __getReddit()
    existingPostIds = __getExistingPostIds(outputDir)

    now = int(time.time())
    posts = []

    read_comments = True
    subreddit_mapping = {
        0: "askreddit",
        1: "amitheasshole",
    }
    for key, value in subreddit_mapping.items():
        print(f"[{key}] {value}")
    SUBREDDIT = subreddit_mapping[int(input("Input: "))]

    if SUBREDDIT == "amitheasshole":
        read_comments = False

    for submission in reddit.subreddit(SUBREDDIT).top(time_filter="day", limit=postOptionCount*3):
        if (f"{submission.id}.mp4" in existingPostIds or submission.over_18):
            continue
        hoursAgoPosted = (now - submission.created_utc) / 3600
        print(f"[{len(posts)}] {submission.title}     {submission.score}    {'{:.1f}'.format(hoursAgoPosted)} hours ago")
        posts.append(submission)
        if (len(posts) >= postOptionCount):
            break

    postSelection = int(input("Input: "))
    selectedPost = posts[postSelection]
    return __getContentFromPost(selectedPost, read_comments), selectedPost.id, read_comments

def __getReddit():
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )

def __getContentFromPost(submission, read_comments) -> VideoScript:
    content = VideoScript(submission.url, submission.title, submission.id, read_comments)
    print(f"Creating video for post: {submission.title}")
    print(f"Url: {submission.url}")
    print(f"Id: {submission.id}")

    if read_comments:
        failedAttempts = 0
        for comment in submission.comments:
            if (comment.author == None or comment.author == '[deleted]' or comment.author == 'AutoModerator'):
                continue
            elif(content.addCommentScene(markdown_to_text.markdown_to_text(comment.body), comment.id)):
                failedAttempts += 1
            if (content.canQuickFinish() or (failedAttempts > 4 and content.canBeFinished())):
                break
    else:
        paragraphs = submission.selftext.split('\n')
        filtered_paragraphs = []
        for paragraph in paragraphs:
            stripped_paragraph = paragraph.strip()
            if stripped_paragraph.lower().startswith('tl;dr'):
                break
            """
            if stripped_paragraph.lower().startswith('edit') or stripped_paragraph.lower().startswith('update'):
                break
            """
            if(not (len(stripped_paragraph) == 0 or stripped_paragraph.isspace())):
                filtered_paragraphs.append(stripped_paragraph)
        paragraph_number = 0
        for paragraph in filtered_paragraphs:
            content.addStoryScene(paragraph, f"paragraph{paragraph_number}")
            paragraph_number += 1
    return content

def __getExistingPostIds(outputDir):
    files = os.listdir(outputDir)
    files = [f for f in files if os.path.isfile(outputDir+'/'+f)]
    return [re.sub(r'.*?-', '', file) for file in files]
