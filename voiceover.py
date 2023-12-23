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


from gtts import gTTS

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text):
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filePath)
    return filePath


"""
from tiktok_tts import main as tts

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text):
    # Set your TikTok session ID and other parameters
    session_id = "57b7d8b3e04228a24cc1e6d25387603a"
    voice_code = "en_us_002"
    filePath = f"{voiceoverDir}/{fileName}.mp3"

    # Call the main function with the specified parameters
    tts(["-v", voice_code, "-f", "testtext.txt", "-s", session_id, "-n", filePath])

create_voice_over("test", "This is a test")
"""