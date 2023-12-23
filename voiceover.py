"""
import pyttsx3

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text):
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    engine = pyttsx3.init()
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath
"""

"""
from gtts import gTTS

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text):
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filePath)
    return filePath
"""

import tiktok_tts, random

voiceoverDir = "Voiceovers"

voices = [
    'en_us_006', 'en_us_007', 'en_us_009'
]

def create_voice_over(fileName, text):
    session_id = "00453c9bbd7ea65b290bfa2656f7bd08"
    random_voice = random.choice(voices)
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    tiktok_tts.main(random_voice, text, session_id, filePath, False)
    return filePath