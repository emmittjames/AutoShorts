"""
import pyttsx3, os

engine = pyttsx3.init()
# engine.say("Hello, this is pyttsx3.")
engine.save_to_file('hello', 'test.mp3')
engine.say("Hello, this is pyttsx3.")
engine.runAndWait()
"""

from gtts import gTTS
import os

def text_to_speech(text, language='en', filename='output.mp3'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the generated speech to a file
    tts.save(filename)
    print(f'Text converted to speech and saved as {filename}')

    # Play the generated speech (optional)
    os.system(f"start {filename}")  # This works on Windows

text = "hello"
# Example usage
text_to_speech(text, language='en', filename='output.mp3')
