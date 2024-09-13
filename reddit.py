import os
import random
import re
import praw
import markdown_to_text
import time
from videoscript import VideoScript
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')
CLIENT_ID = config["Reddit"]["CLIENT_ID"]
CLIENT_SECRET = config["Reddit"]["CLIENT_SECRET"]
USER_AGENT = config["Reddit"]["USER_AGENT"]

RECENT_SELECTIONS_FILE = 'recent_selections.json'
def is_recent_selection(video_title):
    print("is_recent_selection", video_title)
    recent_selections = load_recent_selections()
    return video_title in recent_selections

def load_recent_selections():
    print("Loading recent selections")
    if os.path.exists(RECENT_SELECTIONS_FILE):
        with open(RECENT_SELECTIONS_FILE, 'r') as file:
            data = json.load(file)
            print("return 1")
            return data.get('recent_selections', [])
    print("return 2")
    return []

def save_recent_selections(recent_selections):
    print("Saving recent selections", recent_selections)
    with open(RECENT_SELECTIONS_FILE, 'w') as file:
        json.dump({"recent_selections": recent_selections}, file)

def add_to_recent_selections(video_title):
    print("Adding to recent selections")
    recent_selections = load_recent_selections()
    print("zzzz", video_title, recent_selections)
    recent_selections.append(video_title.id)
    print("zxszfgf", recent_selections)
    if len(recent_selections) > 3:
        recent_selections = recent_selections[-3:]
    save_recent_selections(recent_selections)

def getContent(outputDir, postOptionCount) -> VideoScript:
    reddit = __getReddit()
    existingPostIds = __getExistingPostIds(outputDir)

    while True:
        now = int(time.time())
        posts = []

        read_comments = True
        subreddit_mapping = {
            0: "askreddit",
            1: "amitheasshole",
            2: "tifu",
            3: "offmychest",
        }
        for key, value in subreddit_mapping.items():
            print(f"[{key}] {value}")
        tries = 0
        while True:
            population = [0, 1, 2, 3]
            weights = [0.4, 0.2, 0.2, 0.2]
            random_number = random.choices(population, weights)[0]
            SUBREDDIT = subreddit_mapping[random_number]
            number_of_posts = len(list(reddit.subreddit(SUBREDDIT).top(time_filter="day", limit=postOptionCount*3)))
            if tries>10 or number_of_posts >= 1:
                break
            tries += 1

        if SUBREDDIT == "amitheasshole" or SUBREDDIT == "offmychest" or SUBREDDIT == "tifu":
            read_comments = False

        for submission in reddit.subreddit(SUBREDDIT).top(time_filter="day", limit=postOptionCount*3):
            if (f"{submission.id}.mp4" in existingPostIds or submission.over_18):
                continue
            hoursAgoPosted = (now - submission.created_utc) / 3600
            paragraph_count = submission.selftext.count('\n') + 1
            word_count = len(submission.selftext.split())
            word_to_paragraph_ratio = word_count / paragraph_count
            if (word_count > 240 or word_to_paragraph_ratio>70 or word_count < 100) and SUBREDDIT != "askreddit":
                continue
            print(f"[{len(posts)}] {submission.title} | Word Count: {word_count} | Paragraph Count: {paragraph_count} | Upvotes: {submission.score} | {'{:.1f}'.format(hoursAgoPosted)} hours ago")
            posts.append(submission)
            if (len(posts) >= postOptionCount):
                break

        postSelection = random.randint(0, len(posts)-1)
        selectedPost = posts[postSelection]
        if is_recent_selection(selectedPost.title):
            continue
        break
    
    add_to_recent_selections(selectedPost)

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
