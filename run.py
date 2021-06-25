import os
import random
import subprocess

import twitter


# video path  & etc.
directory = "/PATH/TO/VIDEO/FOLDER/"
tmpfilename = "out.jpg"

# twitter keys
CONSUMER_KEY_INPUT = 'ENTER_CONSUMER_KEY_INPUT'
CONSUMER_SECRET_INPUT = 'ENTER_CONSUMER_SECRET_INPUT'
ACCESS_TOKEN_KEY_INPUT = 'ENTER_ACCESS_TOKEN_KEY_INPUT'
ACCESS_TOKEN_SECRET_INPUT = 'ENTER_ACCESS_TOKEN_SECRET_INPUT'


# randomly select an mkv video from input directory
def getRandomVideoFilePath(directory):
    outdir = ''
    while not outdir.endswith("mkv"):
        out1 = random.choice(os.listdir(directory))
        if out1.endswith('mkv'):
            outdir = out1
            break
        out2 = random.choice(os.listdir(directory + out1))
        outdir = out1 + '/' + out2
    return outdir


# use ffmpeg to generate screenshot at timestamp
def generateRandomScreenShotLocally(filepath):
    randomTime = random.uniform(0.00, getLength(filepath))
    command_img = [
        'ffmpeg', '-y',
        '-ss', str(randomTime),
        '-i', filepath,
        '-vframes', '1',
        '-vf', 'scale=1920:1080',
        '-q:v', '1',
        '-qmin', '1',
        tmpfilename
    ]
    subprocess.call(command_img)


# use ffprobe to get the length of the video
def getLength(filepath):
    command_info = [
        'ffprobe',
        '-i', filepath,
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=%s' % "p=0"
    ]
    duration = subprocess.check_output(command_info)
    return float(duration)


def postImage():
    api = twitter.Api(consumer_key=CONSUMER_KEY_INPUT,
                      consumer_secret=CONSUMER_SECRET_INPUT,
                      access_token_key=ACCESS_TOKEN_KEY_INPUT,
                      access_token_secret=ACCESS_TOKEN_SECRET_INPUT)
    return api.PostUpdate("", tmpfilename)


if __name__ == '__main__':
    filepath = directory + getRandomVideoFilePath(directory)
    generateRandomScreenShotLocally(filepath)
    postImage()
