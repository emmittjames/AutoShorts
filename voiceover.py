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

import tiktok_tts, random, subprocess

voiceoverDir = "Voiceovers"

# voices = ['en_us_001', 'en_us_006', 'en_us_007', 'en_us_009']

# voices = ['en_us_006']
# voices = ['en_male_funny']

voices = [  
            'en_au_001', 'en_au_002', 'en_uk_001', 'en_uk_003', 'en_us_001', 'en_us_006', 'en_us_007', 'en_us_009', 'en_us_010', 
            'en_male_funny', 'en_male_pirate', 'en_female_madam_leota', 'en_us_rocket'
            ]

# voices = ['en_us_rocket', 'en_male_pirate', 'en_female_madam_leota']

def create_voice_over(fileName, script_path):
    voice = random.choice(voices)
    file_path = f"{voiceoverDir}/{fileName}.mp3"

    command = [
        'python3',
        'tiktok_tts.py',
        '-v', voice,
        '-f', script_path,
        '-n', file_path,
        '--session', '00453c9bbd7ea65b290bfa2656f7bd08',
    ]

    subprocess.run(command)

    return file_path