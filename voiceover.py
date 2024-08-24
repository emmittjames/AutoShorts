import configparser
import re
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def convert_to_ssml(text):
    text_with_breaks = re.sub(r',+', '<break time="20ms"/>', text)
    text_with_breaks = re.sub(r'\.+', '<break time="40ms"/>', text_with_breaks)
    ssml_template = f"""
    <speak>
        <prosody rate="fast">
            {text_with_breaks}
        </prosody>
    </speak>
    """
    return ssml_template.strip()

def create_voice_over(fileName, script_path, special=False, read_comments=True):
    file_path = f"Voiceovers/{fileName}.mp3"
    config = configparser.ConfigParser()
    config.read('config.ini')
    aws_access_key_id = config.get('AWS', 'aws_access_key_id')
    aws_secret_access_key = config.get('AWS', 'aws_secret_access_key')

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-east-1'
    )

    polly = session.client("polly")

    text = read_text_file(script_path)
    ssml_text = convert_to_ssml(text)

    try:
        response = polly.synthesize_speech(Text=ssml_text, OutputFormat="mp3", VoiceId="Stephen", Engine="neural", TextType="ssml")
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            try:
                with open(file_path, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
        return file_path
    else:
        print("Could not stream audio")
        sys.exit(-1)