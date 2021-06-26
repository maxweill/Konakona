import os
import random
import subprocess

import twitter


# video path & etc.
directory = '/PATH/TO/VIDEO/FOLDER/'
tmpfile_img = 'out.jpg'
tmpfile_vid = 'out.mp4'
clip_length = '5'
video_chance = 0.5

# twitter keys
CONSUMER_KEY_INPUT = 'ENTER_CONSUMER_KEY_INPUT'
CONSUMER_SECRET_INPUT = 'ENTER_CONSUMER_SECRET_INPUT'
ACCESS_TOKEN_KEY_INPUT = 'ENTER_ACCESS_TOKEN_KEY_INPUT'
ACCESS_TOKEN_SECRET_INPUT = 'ENTER_ACCESS_TOKEN_SECRET_INPUT'


# randomly select an mkv video from input directory
def get_random_video_filepath(directory):
    outdir = ''
    while not outdir.endswith('mkv'):
        out1 = random.choice(os.listdir(directory))
        if out1.endswith('mkv'):
            outdir = out1
            break
        out2 = random.choice(os.listdir(directory + out1))
        outdir = out1 + '/' + out2
    return outdir


# use ffmpeg to generate screenshot at timestamp
def generate_random_screenshot_locally(filepath):
    random_time = random.uniform(0.00, get_length(filepath))
    command_img = [
        'ffmpeg', '-y',
        '-ss', str(random_time),
        '-i', filepath,
        '-vframes', '1',
        '-vf', 'scale=1920:1080',
        '-q:v', '1',
        '-qmin', '1',
        tmpfile_img
    ]
    subprocess.call(command_img)


# use ffmpeg to generate 5 sec video at timestamp
def generate_random_gif_locally(filepath):
    random_time = random.uniform(0.00, get_length(filepath)-float(clip_length))
    command_vid = [
        'ffmpeg', '-y',
        '-ss', str(random_time),
        '-i', filepath,
        '-t', str(clip_length),
        '-ac', '2',
        '-sn',
        '-map_chapters', '-1',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-vf', 'scale=720:1280',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        tmpfile_vid
    ]
    subprocess.call(command_vid)


# use ffprobe to get the length of the video
def get_length(filepath):
    command_info = [
        'ffprobe',
        '-i', filepath,
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=%s' % 'p=0'
    ]
    duration = subprocess.check_output(command_info)
    return float(duration)


# uploads the screenshot to twitter
def post_image(tmpfile):
    api = twitter.Api(consumer_key=CONSUMER_KEY_INPUT,
                      consumer_secret=CONSUMER_SECRET_INPUT,
                      access_token_key=ACCESS_TOKEN_KEY_INPUT,
                      access_token_secret=ACCESS_TOKEN_SECRET_INPUT)
    return api.PostUpdate('', tmpfile)


# checks is it's a screenshot or gif
def check_video():
    filepath = directory + get_random_video_filepath(directory)
    r = random.random()
    if r <= video_chance:
        generate_random_gif_locally(filepath)
        return tmpfile_vid
    else:
        generate_random_screenshot_locally(filepath)
        return tmpfile_img


if __name__ == '__main__':
    post_image(check_video())
