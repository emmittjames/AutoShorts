from datetime import datetime
from moviepy.editor import AudioFileClip
import voiceover, re

MAX_WORDS_PER_COMMENT = 300
MIN_COMMENTS_FOR_FINISH = 4
MIN_DURATION = 30
MAX_DURATION = 59

class VideoScript:
    title = ""
    fileName = ""
    titleSCFile = ""
    url = ""
    totalDuration = 0
    frames = []

    def __init__(self, url, title, fileId) -> None:
        self.fileName = f"{datetime.today().strftime('%Y-%m-%d')}-{fileId}"
        self.url = url
        self.title = title
        self.titleAudioClip = self.__createVoiceOver("title", title)
        print("done")

    def canBeFinished(self) -> bool:
        return (len(self.frames) > 0) and (self.totalDuration > MIN_DURATION)

    def canQuickFinish(self) -> bool:
        return (len(self.frames) >= MIN_COMMENTS_FOR_FINISH) and (self.totalDuration > MIN_DURATION)

    def addCommentScene(self, text, commentId) -> None:
        wordCount = len(text.split())
        if (wordCount > MAX_WORDS_PER_COMMENT):
            return True
        frame = ScreenshotScene(text, commentId)
        frame.audioClip = self.__createVoiceOver(commentId, text)
        if (frame.audioClip == None):
            return True
        self.frames.append(frame)

    def getDuration(self):
        return self.totalDuration

    def getFileName(self):
        return self.fileName
    
    def remove_any_links(self, text):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        cleaned_text = url_pattern.sub('', text)
        return cleaned_text

    def __createVoiceOver(self, name, text):
        text = self.remove_any_links(text)
        script_path = f"Scripts/{self.fileName}"
        with open(script_path, 'w') as file:
            file.write(text)
        
        special_voice = False
        if text.len < 10 and name != "title":
            special_voice = True

        file_path = voiceover.create_voice_over(f"{self.fileName}-{name}", script_path, special_voice)
        print(f"Created voice over: {file_path}")
        audioClip = AudioFileClip(file_path)
        if (self.totalDuration + audioClip.duration > MAX_DURATION):
            return None
        self.totalDuration += audioClip.duration
        return audioClip


class ScreenshotScene:
    text = ""
    screenShotFile = ""
    commentId = ""

    def __init__(self, text, commentId) -> None:
        self.text = text
        self.commentId = commentId