import pyttsx3
import os

engine = pyttsx3.init()
engine.save_to_file('hello', 'test.mp3')
engine.startLoop()
engine.iterate()
engine.endLoop()

os.rename("test.mp3", "newName.mp3")
