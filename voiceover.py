import random, subprocess

voiceoverDir = "Voiceovers"

voices = [  
            'en_au_001', 'en_au_002', 'en_uk_001', 'en_uk_003', 'en_us_001', 'en_us_006', 'en_us_007', 'en_us_009', 'en_us_010', 
            'en_male_funny'
        ]

special_voices = ['en_male_pirate', 'en_female_madam_leota', 'en_us_rocket']

story_voices = ['en_us_006']

def create_voice_over(fileName, script_path, special=False, read_comments=True):
    global special_voices, voices
    if read_comments:
        if (special and len(special_voices) > 0 and random.random() < 0.5):
            voice = random.choice(special_voices)
            special_voices.remove(voice)
            if(special_voices == []):
                special_voices = ['en_male_pirate', 'en_female_madam_leota']
        else:
            voice = random.choice(voices)
            voices.remove(voice)
            if(voices == []):
                voices = [  
                    'en_au_001', 'en_au_002', 'en_uk_001', 'en_uk_003', 'en_us_001', 'en_us_006', 'en_us_007', 'en_us_009', 'en_us_010', 
                    'en_male_funny', 'en_us_rocket'
                ]
    else:
        voice = random.choice(story_voices)

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