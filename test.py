"""Getting Started Example for Python 2.7+/3.3+"""
import configparser
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir


config = configparser.ConfigParser()
config.read('config.ini')

aws_access_key_id = config.get('AWS', 'aws_access_key_id')
aws_secret_access_key = config.get('AWS', 'aws_secret_access_key')

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-1'
)

polly = session.client("polly")

text = """<speak><prosody rate="fast">Google Cloud Text-to-Speech enables developers to synthesize natural-sounding speech with 100+ voices. </prosody></speak>"""

try:
    # Request speech synthesis
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                        VoiceId="Stephen", Engine="neural", TextType="ssml")
except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
    # Note: Closing the stream is important because the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
           fileName = "Asdfasdfv"
           output = f"Voiceovers/{fileName}.mp3"

           try:
            # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                   file.write(stream.read())
           except IOError as error:
              # Could not write to file, exit gracefully
              print(error)
              sys.exit(-1)

else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)