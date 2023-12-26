import subprocess

random_voice = 'en_us_006'
voiceoverDir = "Voiceovers"
fileName = "testingggg"
script_path = "Scripts/testingggg.txt"
file_path = f"{voiceoverDir}/{fileName}.mp3"

command = [
    'python3',
    'tiktok_tts.py',
    '-v', random_voice,
    '-f', script_path,
    '-n', file_path,
    '--session', '00453c9bbd7ea65b290bfa2656f7bd08',
]

subprocess.run(command)